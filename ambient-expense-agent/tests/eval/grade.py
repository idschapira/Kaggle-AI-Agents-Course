# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Scorer standalone que substitui `agents-cli eval grade`.

Por que nao usar o `agents-cli eval grade`? Investigamos o codigo-fonte
instalado do SDK (`vertexai/_genai/_evals_metric_handlers.py`,
`_METRIC_HANDLER_MAPPING`) e confirmamos um bug/incompatibilidade: QUALQUER
metrica do tipo `CodeExecutionMetric` - mesmo com `execution: "local"` - e
roteada para `CustomCodeExecutionMetricHandler`, que SEMPRE faz uma chamada
HTTP `:evaluateInstances` para o backend gerenciado da Vertex AI. A unica
rota que executa a funcao Python de verdade em processo, sem rede
(`CustomMetricHandler`), so e usada para um `types.Metric` generico cujo
`custom_function` ja seja um Callable - nunca para `CodeExecutionMetric`.
Resultado: `cmd_grade.py` chama `vertexai.Client(project=None,
location=None)` e a chamada remota falha (sem projeto/regiao validos),
caindo no `except Exception` generico que o CLI imprime como "Evaluation
failed." sem mais detalhes. A doc da skill (`metrics-guide.md`, "execucao
local, sem projeto GCP") nao reflete o comportamento real desta versao do
SDK.

Em vez de depender do SDK da Vertex AI (que exigiria GCP/ADC, contrariando
a decisao do Dia 3 de usar so a GOOGLE_API_KEY do AI Studio), este script
faz o que o `agents-cli eval grade` deveria fazer para metricas locais:
1. Le `eval_config.yaml` e `exec()` cada `custom_function` (mesmo codigo,
   mesma logica ja validada isoladamente em `debug_metric.py`).
2. Junta cada trace gerado por `generate_traces.py` com o `prompt` original
   do dataset (o arquivo de traces so guarda `agent_data`, nao o prompt).
3. Roda `evaluate(instance)` de cada metrica para cada caso, agrega a
   media de score por metrica, e salva o resultado em
   `artifacts/grade_results/results_<timestamp>.json` (mais um resumo
   `.md` legivel), no mesmo espirito do `generated_traces.json`.

Uso: uv run python tests/eval/grade.py
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent

CONFIG_PATH = HERE / "eval_config.yaml"
DATASET_PATH = HERE / "datasets" / "basic-dataset.json"
TRACES_PATH = PROJECT_ROOT / "artifacts" / "traces" / "generated_traces.json"
RESULTS_DIR = PROJECT_ROOT / "artifacts" / "grade_results"


def _load_metric_functions(config: dict[str, Any]) -> dict[str, Any]:
    """Compila cada `custom_function` (string de codigo) numa funcao Python real."""
    metric_fns: dict[str, Any] = {}
    for metric in config["custom_metrics"]:
        namespace: dict[str, Any] = {}
        exec(metric["custom_function"], namespace)  # noqa: S102 - mesmo padrao do debug_metric.py
        metric_fns[metric["name"]] = namespace["evaluate"]
    return metric_fns


def _build_instances(dataset: dict[str, Any], traces: dict[str, Any]) -> list[dict[str, Any]]:
    """Junta o `prompt` do dataset original com o `agent_data` do trace gerado.

    `generated_traces.json` so guarda `eval_case_id` + `agent_data` (ver
    generate_traces.py); o `prompt` (o JSON da despesa submetida) vive no
    dataset. Cada `custom_function` espera os dois juntos num so dict, do
    mesmo jeito que `agents-cli` monta o `EvaluationInstance`.
    """
    prompts_by_id = {case["eval_case_id"]: case["prompt"] for case in dataset["eval_cases"]}
    instances = []
    for trace_case in traces["eval_cases"]:
        case_id = trace_case["eval_case_id"]
        instances.append(
            {
                "eval_case_id": case_id,
                "prompt": prompts_by_id.get(case_id),
                "agent_data": trace_case["agent_data"],
            }
        )
    return instances


def main() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    traces = json.loads(TRACES_PATH.read_text(encoding="utf-8"))

    metrics_to_run: list[str] = config["metrics_to_run"]
    metric_fns = _load_metric_functions(config)
    instances = _build_instances(dataset, traces)

    # case_id -> metric_name -> {"score":..., "explanation":...}
    per_case_results: dict[str, dict[str, dict[str, Any]]] = {}

    for instance in instances:
        case_id = instance["eval_case_id"]
        print(f"Avaliando '{case_id}'...")
        per_case_results[case_id] = {}
        for metric_name in metrics_to_run:
            evaluate_fn = metric_fns[metric_name]
            result = evaluate_fn(instance)
            per_case_results[case_id][metric_name] = result
            print(f"  {metric_name}: score={result.get('score')}")

    # Agrega a media de score por metrica, em todos os casos.
    aggregates: dict[str, float] = {}
    for metric_name in metrics_to_run:
        scores = [per_case_results[cid][metric_name]["score"] for cid in per_case_results]
        aggregates[metric_name] = sum(scores) / len(scores) if scores else 0.0

    print("\n=== Medias por metrica ===")
    for metric_name, avg in aggregates.items():
        print(f"{metric_name}: {avg:.2f} / 5")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metrics_to_run": metrics_to_run,
        "aggregates": aggregates,
        "per_case_results": per_case_results,
    }

    json_path = RESULTS_DIR / f"results_{timestamp}.json"
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = ["# Resultado do grade", "", f"Gerado em: {output['generated_at']}", ""]
    md_lines.append("| Caso | " + " | ".join(metrics_to_run) + " |")
    md_lines.append("|---" * (len(metrics_to_run) + 1) + "|")
    for case_id, metrics in per_case_results.items():
        row = [case_id] + [str(metrics[m]["score"]) for m in metrics_to_run]
        md_lines.append("| " + " | ".join(row) + " |")
    md_lines.append("")
    md_lines.append("## Medias")
    for metric_name, avg in aggregates.items():
        md_lines.append(f"- **{metric_name}**: {avg:.2f} / 5")
    md_lines.append("")
    md_lines.append("## Explicacoes detalhadas")
    for case_id, metrics in per_case_results.items():
        md_lines.append(f"\n### {case_id}")
        for metric_name in metrics_to_run:
            md_lines.append(f"- **{metric_name}** (score {metrics[metric_name]['score']}): {metrics[metric_name]['explanation']}")

    md_path = RESULTS_DIR / f"results_{timestamp}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\nResultados salvos em:\n  {json_path}\n  {md_path}")


if __name__ == "__main__":
    main()

# Diário de Aprendizado — 5-Day AI Agents (Kaggle)

> Registro de progresso do curso, mantido sessão a sessão pelo Tutor de Engenharia de Dados.

## Sobre este projeto
- **Curso:** 5-Day AI Agents (Kaggle)
- **Aluno:** Ilan (MBA em curso)
- **Objetivo:** Aprender conceitos de AI Agents e Engenharia de Dados na prática, documentando tudo aqui e versionando no GitHub.

**Recursos do curso:**
- Playlist das lives (YouTube): https://www.youtube.com/playlist?list=PLqFaTIg4myu8AFXUjrVhDkUGp0A9kK8CX

---

## Dia 0 — Setup do Ambiente

**Data:** 2026-06-16

**Objetivo da tarefa:** Configurar a estrutura de diretórios do projeto e inicializar o controle de versão (Git) antes de iniciar o conteúdo do Dia 1.

**O que foi feito:**
- Criada estrutura de diretórios (`notebooks/`, `data/raw/`, `data/processed/`, `scripts/`, `docs/`).
- Criado o arquivo `Diário_Aprendizado.md` (este arquivo).
- Criado `.gitignore` e `README.md`.
- Repositório Git local inicializado (instruções fornecidas).

**Conceitos novos:**
- *(a preencher conforme avançamos)*

**Glossário do dia:**
- **Repositório (repo):** pasta onde o Git guarda o histórico de versões do projeto.
- **Commit:** um "snapshot" salvo do estado do código em um momento específico.
- **.gitignore:** arquivo que diz ao Git quais arquivos/pastas ignorar (não versionar).

---

## Dia 1 — Criar app no Google AI Studio e Deploy no Cloud Run

**Data:** 2026-06-16

**Objetivo da tarefa:** Construir um app simples usando o Google AI Studio (integrado ao Gemini) e publicá-lo via Cloud Run, depois versionar o código no GitHub.

**O que foi feito:**
- Criado o app **PokéAsset Manager** (portfólio de cards Pokémon) no Google AI Studio, usando o SDK `@google/genai` para chamadas ao Gemini.
- Deploy feito direto pelo AI Studio no **Cloud Run**: https://pokeasset-manager-126303862772.us-east1.run.app/
- Exportado o código-fonte (.zip) do AI Studio e organizado em `apps/dia1_pokeasset_manager/` no repositório.
- Atualizado `.gitignore` para ignorar `node_modules/`, `dist/`, `build/` e os `.zip` de export.
- Confirmado que `.env.example` só contém placeholders (sem chaves reais expostas).

**Conceitos novos:**
- **Google AI Studio:** ambiente da Google para prototipar apps com modelos Gemini, com deploy integrado.
- **Cloud Run:** serviço da Google Cloud que executa containers sem precisar gerenciar servidores (serverless).
- **Export/Download (AI Studio):** gera o código-fonte do app (separado do link público já publicado).
- **Stack do app:** React + Vite + TypeScript, com `@google/genai` como SDK de IA.

**Glossário do dia:**
- **Deploy:** publicar uma versão do app para que fique acessível publicamente.
- **Serverless:** modelo de execução em que a infraestrutura (servidores) é gerenciada automaticamente pelo provedor de nuvem.
- **SDK:** conjunto de ferramentas/bibliotecas que facilita a integração com uma API (aqui, a API do Gemini).
- **.env / variáveis de ambiente:** arquivo usado para guardar segredos (como API Keys) fora do código-fonte.

---

## Dia 2 — Agent Tools & Interoperability + Antigravity CLI + MCP Server

**Data:** 2026-06-16

**Objetivo da tarefa:** Ler o whitepaper "Agent Tools & Interoperability" e completar dois codelabs práticos: instalar/usar o **Antigravity CLI** e conectar o **Google Developer Knowledge MCP server**.

**O que foi feito:**
- Lido o whitepaper *Agent Tools & Interoperability* (Kaggle, Dia 2): conceitos de MCP (consumo de servidores, descoberta/configuração/conexão, problema NxM, debugging), A2A (Agent-to-Agent), Agent Card, e visão geral de A2UI/AP2/UCP.
- Instalado o **Antigravity CLI** (`agy`, versão 1.0.8) via PowerShell, em `apps/agy-cli-projects/`.
- Login feito via Google OAuth; aceitos termos de serviço e permissão de confiança na pasta de trabalho.
- Exploradas configurações (`/config`): Tool Permission, modelos disponíveis (`agy models`), troca de modelo (`agy model "..."`).
- Testado o modo `--dangerously-skip-permissions` (autoaprova todas as ações) comparado ao modo padrão `request-review` (pede aprovação a cada ação) — lição prática de segurança/HITL.
- Criado projeto novo no Google Cloud (`kaggle-dia2-mcp`), habilitada a **Developer Knowledge API**, criada e restringida uma API key.
- Configurado o servidor MCP `google-developer-knowledge` em `~/.gemini/config/mcp_config.json`.
- Validada a conexão via `/mcp` no Antigravity CLI e testado com um prompt real (`Based on the Google Developer Knowledge, does Google Workspace support MCP servers?`), aprovando a permissão de uso da ferramenta na primeira chamada.

**Próximos passos (fora do escopo oficial do Dia 2, aplicação prática planejada):**
- Usar o Antigravity CLI (vibe coding) para implementar melhorias no PokéAsset Manager (Dia 1): fotos reais dos cards, tracker de preços, login de usuários.

**Sessão de aplicação prática (2026-06-17):**
- Obtida a API key da **PokeWallet API** (https://api.pokewallet.io) e lida a documentação completa: autenticação via header `X-API-Key`, endpoint `GET /search?q=...` retorna `tcgplayer.prices[].market_price` e `cardmarket.prices[].avg`, limite gratuito de 100 req/hora e 1.000 req/dia.
- Desenhada a arquitetura segura: rota proxy no backend Express (`GET /api/pokewallet/price?q=`) que guarda a `POKEWALLET_API_KEY` só no `.env` do servidor — o frontend nunca toca na chave.
- Prompt de implementação preparado para o Antigravity CLI, mas sessão bloqueada pela cota gratuita do modelo padrão (Gemini Pro) ter esgotado.
- Tentativa de troca de modelo via comando interno `agy model "Claude Sonnet 4.6 (Thinking)"` não funcionou (comando não reconhecido/erro).
- **Correção encontrada:** a troca de modelo é feita como **flag na inicialização** do CLI, não como comando dentro da sessão: `agy --model "Claude Sonnet 4.6 (Thinking)"`.

**Status:** Implementação da integração com PokeWallet ainda não iniciada (apenas planejada). Resolvido: forma correta de trocar de modelo no Antigravity CLI (`agy --model "..."`). Próxima sessão: rodar o prompt da rota proxy com esse comando.

**Conceitos novos:**
- **MCP (Model Context Protocol):** "USB-C" do agente — conecta um agente a ferramentas externas (arquivos, APIs, bancos de dados) de forma padronizada, evitando integrações sob medida para cada par modelo↔ferramenta (problema NxM).
- **A2A (Agent-to-Agent):** protocolo para um agente delegar tarefas a outro agente especialista, permitindo que o agente pause, negocie e retome (diferente de uma chamada de tool simples e definitiva).
- **Agent Card:** "currículo" machine-readable de um agente A2A — descreve capacidades, políticas de segurança e como se comunicar com ele.
- **Antigravity CLI ("agy"):** ferramenta de terminal do Google para programar com um agente de IA ("vibe coding"), com recursos de raciocínio multi-etapas, edição multi-arquivo e histórico de conversa.
- **Tool Permission (request-review vs. --dangerously-skip-permissions):** controla se o agente pede aprovação antes de executar ações que alteram arquivos/sistema.

**Glossário do dia:**
- **NxM problem:** sem um protocolo padrão, conectar N modelos a M ferramentas exige N×M integrações sob medida; com MCP, o esforço cai para N+M.
- **HITL (Human-in-the-loop):** prática de manter um humano aprovando ações sensíveis do agente antes de executarem.
- **Registry (de MCP ou de Agentes):** catálogo onde servidores MCP ou agentes A2A ficam disponíveis para descoberta (público, de terceiros vetados, ou interno da empresa).
- **stdio / SSE:** dois transportes usados por servidores MCP — stdio roda local como subprocesso; SSE conecta a um endpoint remoto via streaming HTTP.

**Status:** Conteúdo oficial do Dia 2 concluído (whitepaper lido, 2 codelabs feitos). Aplicação prática no PokéAsset Manager planejada como próxima etapa.

---

## Dia 3 — Agent Skills

**Data:** 2026-06-17

**Objetivo da tarefa:** Assistir à live/vídeo-resumo do Dia 3, ler o whitepaper *Agent Skills* e discutir os conceitos centrais via Q&A antes de avançar para os codelabs práticos.

**O que foi feito:**
- Whitepaper *Agent Skills* (Kaggle, Dia 3) anexado ao projeto e lido.
- Vídeo-resumo assistido; destaque pessoal: o "princípio das 8 tentativas consecutivas" (uma skill só deve ser confiável se acertar repetidamente, não só uma vez — ligado à queda real de 20-30% entre pass@1 de benchmark e produção, citada no whitepaper).
- Sessão de Q&A sobre o whitepaper, cobrindo:
  1. Por que "rodou sem erro uma vez" não é suficiente para validar uma Skill (pode ser sorte; precisa de repetição/consistência).
  2. Por que triggers precisam de exemplos positivos **e** negativos (evita falsos positivos por descrição vaga).
  3. O teste prático "se não dá pra escrever 3 casos de teste, a skill está mal definida ou faz coisa demais" — aplicado ao PokéAsset Manager: chamada de API de preço (fácil, determinística) vs. identificar exatamente qual Pokémon/condição (difícil, julgamento subjetivo → precisa de revisão humana).

**Conceitos novos:**
- **Agent Skill:** unidade leve e portátil de capacidade (pasta com `SKILL.md` + scripts opcionais) que ensina um agente a executar uma tarefa específica de forma repetível.
- **Trigger (gatilho da skill):** a descrição que faz o agente decidir quando usar a skill; precisa de casos de teste positivos e negativos para ser precisa.
- **Pass@1 vs. confiabilidade em produção:** taxa de acerto isolada em benchmark tende a cair 20-30% no uso real — por isso testar repetidamente (ex.: "8 tentativas consecutivas") é mais confiável do que um teste único.
- **Tiers de skill (read-only vs. action-allowed):** o nível de risco da skill (só ler dados vs. executar ações) muda o rigor de validação necessário.

**Glossário do dia:**
- **Eval-as-Unit-Test:** padrão de testar uma skill como se fosse um teste de unidade de código — roda automaticamente e bloqueia merge se falhar.
- **Trajectory testing:** validar não só a resposta final do agente, mas o caminho/ferramentas que ele usou para chegar lá.
- **Reviewer & Gate:** verificação automática (determinística) que bloqueia a execução se a validação falhar, em vez de depender só do julgamento do modelo.
- **SKILL.md:** arquivo principal de uma Agent Skill, com frontmatter (metadados) e instruções/descrição de uso.

**Sessão de aplicação prática — Codelab 1: Authoring Google Antigravity Skills (2026-06-19):**
- Clonado o repositório de exemplos [rominirani/antigravity-skills](https://github.com/rominirani/antigravity-skills); descoberta uma divergência entre o codelab e o repo real: das 5 skills descritas no texto, só 4 estavam de fato commitadas (`git-commit-formatter`, `license-header-adder`, `json-to-pydantic`, `database-schema-validator`) — a 5ª (`adk-tool-scaffold`, nível "Composição") não existe no repositório atual. Decisão: seguir só com as 4 disponíveis.
- Skills movidas para `.agent/skills/` na raiz do projeto (escopo **Workspace**, para versionar no GitHub junto com o aprendizado).
- **4 testes realizados no Antigravity, todos com sucesso:**
  1. `git-commit-formatter`: pedido de commit em linguagem natural gerou mensagem no padrão Conventional Commits (`feat(auth): add initial login placeholder`).
  2. `license-header-adder`: header de licença adicionado a `scripts/sample.py`, com o agente convertendo automaticamente a sintaxe de comentário (`/* */` → `#`) por ser arquivo Python.
  3. `json-to-pydantic`: JSON convertido para modelo Pydantic (`Optional[int] = None` inferido corretamente do campo `null`), seguindo o estilo do exemplo da skill. Confirmado que o trigger funciona em prompts **em português** — o matching é semântico, não por palavra-chave.
  4. `database-schema-validator`: ao validar um SQL sem `PRIMARY KEY`, o agente **executou o script** `validate_schema.py` (em vez de avaliar visualmente) e reportou o erro corretamente — validação do padrão "Tool Use" do whitepaper.
- Evidências dos testes organizadas em `docs/dia3_codelab1_tests/`.

**Status:** Codelab 1 (Authoring Skills) **concluído** — todas as 7 seções fechadas (4/5 skills de exemplo testadas, Developer Toolkit do Agents CLI configurado e validado, instalação via `npx skills` confirmada). Codelab 2 ainda não iniciado.

**Sessão de aplicação prática — Codelab 1, Seção 6 (The Developer Toolkit / Agents CLI) — 2026-06-19:**
- Instalada a `google-agents-cli` via `uvx google-agents-cli setup`. **Problema de PATH no Windows:** o `uv` instala binários em `~/.local/bin`, que não estava no PATH do usuário — resolvido com `uv tool ensurepath` + reabertura completa do terminal (mudança de PATH só é lida por sessões abertas *depois* do ajuste).
- Autenticação feita via `agents-cli login -i`, escolhendo **Gemini API Key** (gratuita, via AI Studio) em vez de Google Cloud ADC — alinhado à decisão de evitar billing do Vertex AI.
- Criado projeto de exemplo `weather-assistant` (`agents-cli create weather-assistant --prototype --yes` + `agents-cli install`), com ~121 pacotes instalados via `uv sync` (destaque: `google-adk`, `google-genai`).
- **Bug 1 encontrado:** o template gerado por padrão força o modo Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=True` + `google.auth.default()` em `app/agent.py`), mesmo quando o login foi feito via API Key. Corrigido removendo essas linhas, deixando o agente usar a Gemini API Key diretamente.
- **Bug 2 encontrado:** `app/fast_api_app.py` (servidor local usado por `agents-cli run`/`playground`) também chamava `google.auth.default()` e criava um cliente de **Cloud Logging**, travando o processo sem credenciais GCP. Corrigido trocando por `logging` padrão do Python e desligando `otel_to_cloud` (telemetria para Cloud Trace).
- **Bug 3 (não corrigido, contornado):** `agents-cli playground` falhou no Windows com `Error: Got unexpected extra arguments (app Dockerfile GEMINI.md ...)` — o argumento `.` (diretório atual) está sendo expandido incorretamente em múltiplos argumentos antes de chegar no comando `adk web`. Parece bug genuíno da ferramenta no Windows. **Workaround:** chamar o `adk` diretamente, pulando o wrapper: `uv run adk web app --host 127.0.0.1 --port 8080`.
- Também observado: a flag `--reload` do `adk web` não é suportada no Windows (força `SelectorEventLoop`, incompatível com subprocessos) — o próprio ADK detecta isso e desliga automaticamente (`Forcing --no-reload`), sem ação necessária.
- Playground subiu com sucesso em `http://127.0.0.1:8080`, agente `app` carregado corretamente na interface.
- **Causa raiz do erro 403 identificada:** a API Key usada inicialmente era do projeto `kaggle-dia2-mcp` (criado no Dia 2 para a Developer Knowledge API) — nunca teve a Generative Language API habilitada. **Lição:** nem toda API Key do Google Cloud serve para qualquer API; precisa ser gerada especificamente em aistudio.google.com (projeto `gen-lang-client-...`), que já vem com essa API habilitada por padrão.
- ⚠️ Nota de segurança: a API Key antiga chegou a ser colada em texto puro durante a sessão de debug — gerada uma key nova no AI Studio (boa prática, evita reusar uma chave exposta).
- Teste final de validação no playground: `"How are you?"` → resposta correta do agente. Um erro `503 UNAVAILABLE` (modelo sobrecarregado) apareceu nas perguntas seguintes — confirmado ser instabilidade temporária do lado do Google, não erro de configuração.
- **Seção 7 (Installing Agent Skills using npx skills):** seção informativa, sem passos práticos obrigatórios — alerta que skills instaladas via `npx skills` vão para `~/.agents/skills`, mas o Antigravity CLI só lê de `<projeto>/.agent/skills/` (escopo projeto) ou `~/.gemini/antigravity-cli/skills/` (escopo global). **Já resolvido automaticamente:** o `agents-cli setup` (Seção 6) já linkou as 7 skills instaladas direto em `~/.gemini/antigravity-cli/skills/` — nenhuma cópia manual foi necessária.

**Status final do Codelab 1:** ✅ Concluído (7/7 seções).

**Glossário do dia (sessão prática 2026-06-19):**
- **uv / uvx:** `uv` é um gerenciador de pacotes Python rápido (o "npm do Python"); `uvx` roda uma ferramenta Python sem instalar permanentemente (equivalente ao `npx` do Node).
- **PATH:** lista de pastas onde o sistema operacional procura programas executáveis. Se uma ferramenta foi instalada mas o terminal não a "acha", geralmente é porque a pasta dela não está no PATH.
- **`uv tool ensurepath`:** comando que adiciona automaticamente a pasta de binários do `uv` (`~/.local/bin`) ao PATH do usuário no Windows.
- **ADC (Application Default Credentials):** mecanismo de autenticação do Google Cloud usado por bibliotecas como `google.auth`; diferente de uma API Key — exige login via `gcloud`.
- **npx skills (Vercel Labs):** gerenciador de pacotes para Agent Skills, compatível com várias ferramentas de IA; instala em `~/.agents/skills` por padrão.
- **Escopo de skill (projeto vs. global):** skills podem viver na raiz do projeto (`.agent/skills/`, versionável no Git) ou em pasta global do usuário (`~/.gemini/...`, compartilhada entre todos os projetos).
- **Erro 403 PERMISSION_DENIED vs. 503 UNAVAILABLE:** o 403 indica problema de configuração/permissão (ex.: API desabilitada no projeto da chave) — corrigível pelo usuário; o 503 indica sobrecarga temporária do servidor do provedor (Google) — não é erro de configuração, só tentar novamente depois.

**Sessão de aplicação prática — Codelab 2: Vibe Coding AI Agents (Agents CLI & ADK 2.0 Lifecycle) — 2026-06-19:**
- Codelab: [Vibe Coding AI Agents: Managing the Agent Lifecycle with Agents CLI and ADK 2.0](https://codelabs.developers.google.com/agents-cli-adk-lifecycle).
- Autenticação (Seção 2): reaproveitado o login do `agents-cli` do Codelab 1, mas descoberto que a variável `GEMINI_API_KEY` precisa ser **exportada de novo a cada terminal novo** (não persiste como o login da CLI). No Windows isso é `$env:GEMINI_API_KEY="..."` (PowerShell) — `export` é sintaxe de bash/Git Bash, não funciona direto no PowerShell.
- Projeto `customer-support-agent` criado (Seção 4) via prompt em linguagem natural pro Antigravity, que rodou `agents-cli scaffold create ... --prototype --yes` por trás. Confirmado: o prompt deve ser dado ao **agente do chat do IDE**, não digitado direto no terminal — é esse agente que decide e executa o comando.
- Seção 5 (explicar a estrutura do código): como a cota do Antigravity esgotou no meio da sessão, a explicação do `app/agent.py` (workflow, nodes LlmAgent, FunctionNode, edges condicionais) foi feita diretamente comigo (Claude), lendo o arquivo real do projeto — sem depender de cota de IA nenhuma, já que é só leitura/explicação.
- **Bug real encontrado e corrigido na Seção 4/6 (lint):** o código gerado pelo Antigravity usava a sintaxe de exemplo do codelab (`Edge` com tupla de 3 elementos e `Event(route=...)`), mas a versão instalada do `google-adk` (2.3.0) mudou a API:
  1. `Edge` precisa ser instanciado explicitamente: `Edge(from_node=..., to_node=..., route="...")`, não uma tupla solta.
  2. `route` não é um campo direto de `Event` — fica dentro de `Event.actions`, um objeto `EventActions`: `Event(output=..., actions=EventActions(route=route))`.
  - **Lição:** isso é "API drift" — o material didático foi escrito pra uma versão da lib, mas o `uv`/`pip` instalou uma mais nova com interface diferente. Comum no ecossistema de IA agents, que evolui rápido.
- **Bug de infraestrutura encontrado durante a correção:** uma edição de arquivo deixou bytes nulos (`\x00`) sobrando no final do `agent.py`, quebrando o parser do `ruff`/`ty` com erros de sintaxe confusos ("unexpected token"). Resolvido removendo os bytes nulos do final do arquivo (`data.rstrip(b'\x00')`).
- Lint (Seção 6) validado no final: `ruff check`, `ruff format --check`, `ty check` e `codespell` todos passando, confirmado tanto pela checagem direta quanto pelo `agents-cli lint` do usuário.
- **Cota do Gemini esgotada (`429 RESOURCE_EXHAUSTED`, `limit: 0`) no modelo `gemini-2.0-flash`** usado por padrão no scaffold — não era um limite temporário, e sim esse modelo específico **não tendo cota gratuita habilitada** para o projeto da chave (confirmado consultando o painel de cotas do AI Studio: "Gemini 2 Flash" aparecia como 0/0). **Correção:** trocados os dois `LlmAgent` (`classifier` e `shipping_faq`) para `gemini-3.1-flash-lite` — modelo com a maior cota gratuita disponível (15 RPM / 500 RPD) e que é, coincidentemente, o modelo padrão sugerido no próprio texto do codelab.
- **Lição de cota:** a cota gratuita do Gemini é rastreada **por modelo**, não globalmente — um modelo esgotado/sem cota não significa que a chave está "bloqueada"; outros modelos podem estar livres.
- Seção 7 (Playground) testada com sucesso: pergunta de frete (`"How much is standard shipping?"`) roteou corretamente para `shipping_faq`; pergunta não relacionada (`"What is the weather like?"`) roteou para `decline`. Teste de auto-reload (editar a instrução do `shipping_faq` pra ficar com emojis e destacar o pickup gratuito) foi inconclusivo, pois o usuário recarregou a página antes de testar sem reiniciar o servidor — mas o conteúdo novo funcionou após o reload. Fica em aberto se o `--reload` funciona no Windows pra esse projeto (no Dia 3/Codelab 1 já tinha sido observado que `adk web --reload` é desabilitado automaticamente no Windows).
- Seção 8 (CLI) testada com sucesso usando o comando direto (sem o wrapper `agents-cli run`, que trava com "Local server did not start within 30s" no Windows — mesmo bug já catalogado no Codelab 1): `uv run adk run app "pergunta"`.
- Seção 9 (cleanup/deletar o projeto): **pulada intencionalmente** — o `customer-support-agent` foi mantido no repositório como parte do portfólio de aprendizado, em vez de apagado como sugere o codelab original.

**Status:** Codelab 2 do Dia 3 **concluído** (Seções 1–8 completas; Seção 9 pulada por decisão própria). **Dia 3 (Agent Skills) totalmente concluído** — whitepaper, Q&A, Codelab 1 e Codelab 2.

**Conceitos novos (Codelab 2):**
- **API drift:** quando a documentação/exemplo de uma biblioteca fica desatualizada porque uma versão mais nova mudou a interface — o código de exemplo não funciona mais como escrito.
- **EventActions:** objeto que carrega "efeitos colaterais" de um `Event` no ADK 2.0 (incluindo o campo `route` usado para roteamento condicional no `Workflow`) — separado dos dados de saída (`output`) do evento.
- **Cota por modelo (RPM/TPM/RPD):** o nível gratuito do Gemini limita uso por **modelo específico**, não pela chave como um todo — RPM (requisições/minuto), TPM (tokens/minuto), RPD (requisições/dia).

**Glossário do dia (Codelab 2):**
- **RPM / TPM / RPD:** Requests Per Minute, Tokens Per Minute, Requests Per Day — as três dimensões de cota que o Google mede separadamente por modelo no nível gratuito.
- **Scaffold (revisão):** estrutura de projeto pré-gerada automaticamente, que pode conter bugs de geração caso a versão das libs tenha mudado desde que o template foi escrito — sempre vale lintar/testar antes de confiar.
- **FunctionNode:** wrapper do ADK 2.0 que transforma uma função Python comum em um node válido dentro de um `Workflow` (usado quando o node não é um `LlmAgent`).
- **Hot-reload / `--reload`:** recurso que recarrega o código automaticamente ao detectar uma mudança no arquivo, sem precisar reiniciar o servidor manualmente — no `adk web`, não funciona no Windows.

---

## Dia 4 — Vibe Coding Agent Security and Evaluation

**Data:** 2026-06-19

**Objetivo da tarefa:** Ler o whitepaper *Vibe Coding Agent Security and Evaluation*, discutir os conceitos via Q&A, e completar dois codelabs: (A) construir um agente de aprovação de despesas com human-in-the-loop e avaliações locais via ADK 2.0 + Agents CLI + Antigravity; (B) "Write Secure AI Code" (scans automatizados, guardrails, testes de segurança).

**O que foi feito:**
- Whitepaper *Vibe Coding Agent Security and Evaluation* lido por completo (41 páginas). Sessão de Q&A cobrindo, entre outros: **Intent Drift** (o agente desvia do que foi pedido explicitamente, acumulando pequenos desvios a cada iteração — daí o nome "Trust Decay"), Confused Deputy, Slopsquatting, MCP spoofing, injeção indireta de prompt, "It Works Ship It" (a falácia de considerar um código pronto só porque rodou sem erro uma vez), AgBOM, Vibe Diff, e a arquitetura de segurança de 7 pilares.
- **Bloqueio de cota:** o usuário ficou sem nenhuma requisição de prompt disponível no Antigravity até 22/06. **Adaptação de fluxo de trabalho combinada:** em vez de o usuário colar prompts no Antigravity, ele cola aqui o prompt exato que mandaria — e eu (Claude) ajo como o agente, editando os arquivos do projeto diretamente, e devolvo um **"Vibe Diff"** (resumo em linguagem simples do que foi alterado) para aprovação. Comandos de terminal que exigem a máquina/credenciais do próprio usuário continuam sendo fornecidos pra ele rodar. (Combinado com o usuário: seguir com esse fluxo até o fim dos codelabs do curso; migração para o Claude Code direto no terminal fica planejada para o Capstone.)
- Criado `ambient-expense-agent/docs/dia4_comandos.md` — arquivo centralizando os comandos do dia (toolchain, instalação de skills via `npx skills`, playground, eval).
- Projeto `ambient-expense-agent` criado via `agents-cli scaffold create ambient-expense-agent --prototype --yes` + `uv sync`.
- Instaladas as 7 skills oficiais do ADK (`github.com/google/agents-cli`) no escopo do projeto via `npx skills add ... -y --all` (ficam em `.agent/skills/`, versionável no Git — diferente da instalação global usada no Dia 3).
- **Grounding na API real antes de codar:** em vez de confiar no exemplo do codelab (que já tinha "API drift" conhecido do Dia 3), fui direto na biblioteca instalada (`google-adk==2.3.0`, pasta `google/adk/workflow/`) pra confirmar a API atual do `Workflow` graph:
  - `RequestInput` (pausa para humano) não fica em `google.adk.workflow`, e sim em `google.adk.events.RequestInput`.
  - `Workflow(name=..., edges=[...])` aceita uma lista de arestas em formato "chain" — tuplas como `(nó_a, nó_b)` ou `(nó_a, {"rota1": nó_b, "rota2": nó_c})` (RoutingMap, açúcar sintático pra condicional).
  - Um `LlmAgent` pode ser usado **direto** como nó do grafo (sem wrapper manual) — desde que não esteja em `mode="task"`.
  - O valor de saída (`output`) de um nó se torna o `node_input` do próximo nó na aresta; já o `ctx.state` é compartilhado globalmente entre todos os nós (dois canais de dados diferentes).
  - Padrão correto de human-in-the-loop: a função do nó é **re-executada do zero** quando a pessoa responde (não há "continuar de onde parou" dentro da mesma função) — por isso ela precisa checar `ctx.resume_inputs.get(interrupt_id)` no início pra saber se já tem resposta ou se ainda precisa pausar com `yield RequestInput(...)`.
- **Renomeado `app/` → `expense_agent/`** (nome pedido explicitamente pelo usuário no prompt), com todas as referências atualizadas: `agents-cli-manifest.yaml`, `pyproject.toml` (isort + hatch build), `Dockerfile`, imports internos e os testes de integração.
- Escrito o grafo do agente em `expense_agent/agent.py`: `parse_expense` (extrai o evento, decide a rota em Python puro pelo valor em dólares) → `auto_approve` (caminho barato, sem LLM, para valores abaixo do limite) **ou** `review_agent` (único nó que usa o LLM, só para avaliar risco — nunca decide aprovação) → `human_approval` (pausa o grafo via `RequestInput` até alguém aprovar/rejeitar) → `record_outcome` (ponto de convergência dos dois caminhos). Limite (`$100`) e modelo (`gemini-3.1-flash-lite`) isolados em `expense_agent/config.py`.
- Ativado `resumability_config=ResumabilityConfig(is_resumable=True)` no `App` — necessário para a pausa do `human_approval` sobreviver entre chamadas de API separadas (a pessoa aprova numa requisição que chega bem depois da que disparou a pausa).
- **Codelab A, Seção 5 (segurança): adicionado o nó `security_screen`**, entre `parse_expense` e `review_agent`, rodando em Python puro (sem LLM) para qualquer despesa ≥ $100:
  1. **Redação de PII** — regex detecta sequências de 9–19 dígitos na descrição (cobre SSN de 9 dígitos e cartão de 12–19) e substitui por `[REDACTED-SSN]` / `[REDACTED-CREDIT_CARD]` antes que o texto chegue no LLM ou no log.
  2. **Defesa contra prompt injection** — regex procura frases como "bypass all rules", "auto-approve", "ignore instructions"; se achar, a rota vai para `"injection"` em vez de `"clean"`, pulando o `review_agent` por completo e indo direto para `human_approval`, já com um `risk_assessment` sintético (gerado em Python, não pelo LLM) avisando do evento de segurança.
  - **Lição de mecanismo (via pergunta de verificação):** o `human_approval` consegue ler `risk_assessment` mesmo no caminho de injeção — onde o `review_agent` nunca roda — porque `ctx.state` funciona como um **mural compartilhado** entre todos os nós do grafo, não como um bilhete passado de mão em mão pela aresta. Quem escreve no mural (LLM ou Python puro) não importa para quem lê depois.
- **Codelab A, Seção 6 (testar no ADK Playground):** criados `Makefile` (targets `install`, `playground`, `run`, `lint`, `test` — todos chamando `uv` por trás) e confirmado que `pyproject.toml` já cobria as dependências necessárias (`fastapi`, `uvicorn` vêm transitivamente do `google-adk[gcp]`).
  - **Bug de scaffold (recorrente, igual ao do Dia 3):** `fast_api_app.py` também forçava Vertex AI + cliente de Cloud Logging — corrigido do mesmo jeito que no `customer-support-agent`.
  - **Toolchain do Windows:** `make` não vem instalado por padrão no Windows (diferente de Linux/Mac) — instalado via `winget install GnuWin32.Make`, com PATH atualizado de forma segura (`[Environment]::SetEnvironmentVariable` em vez de `setx`, que tem limite de ~1024 caracteres e pode corromper o PATH inteiro) e terminal reaberto do zero (sessões já abertas não veem PATH atualizado).
  - **Bug 1 real do grafo:** o playground/dev-ui do ADK embrulha qualquer mensagem digitada no chat num objeto `google.genai.types.Content` (o mesmo formato usado para falar com um LLM) — `parse_expense` não sabia lidar com esse formato, só com `dict`/`str`. Corrigido extraindo o texto de `content.parts[*].text` antes de processar como JSON.
  - **Bug 2 real do grafo:** o payload de teste do próprio codelab usa a chave `"amount"`, mas o schema `Expense` esperava `amount_usd` — Pydantic rejeitava com "Field required". Corrigido com `Field(alias="amount")` + `populate_by_name=True`, aceitando as duas formas.
  - **Validado o fluxo completo de ponta a ponta:** payload de $150 (acima do limite de $100) → roteou para `security_screen` → `review_agent` (LLM) → `human_approval` pausou pedindo aprovação → usuário aprovou na UI → `record_outcome` fechou o ciclo. Human-in-the-loop confirmado funcionando no ADK Playground.
- **Codelab A, Seção 7 (tornar o agente "ambient"):** em vez de implementar a decodificação de Pub/Sub manualmente (como o prompt do codelab sugeria), descobri — lendo o código-fonte instalado do `google-adk` (`cli/trigger_routes.py`) — que o ADK já expõe esse endpoint **nativamente**: bastou passar `trigger_sources=["pubsub"]` pro `get_fast_api_app()` em `fast_api_app.py`, e ele registra sozinho `/apps/expense_agent/trigger/pubsub`, decodifica o base64, e cria uma sessão nova por evento.
  - **Gotcha do nome da subscription:** o normalizador embutido do ADK só troca `/` por `--` no nome da subscription (ex.: `projects/x/subscriptions/y` → `projects--x--subscriptions--y`), em vez de extrair só o nome curto (`y`) como o codelab pede. Resolvido com um **middleware HTTP** em `fast_api_app.py` que intercepta a requisição, encurta o campo `"subscription"` para o último trecho do path, e "reinjeta" o corpo da requisição antes do handler nativo do ADK processá-la — sem precisar reimplementar a lógica de trigger inteira.
  - **Bug de grafo descoberto ao testar:** o trigger Pub/Sub embrulha o evento de novo dentro de um `Content`, mas o texto interno já vem no formato envelope `{"data": ..., "attributes": ...}` (puro JSON, não mais base64, pois o ADK já decodificou). A função `parse_expense` original não previa esse formato. Refatorada para uma função auxiliar `_extract_expense_payload`, que agora lida com **4 formatos diferentes de entrada** (Content do chat, envelope do trigger, dict/JSON com `data` em base64, JSON puro) de forma unificada e em cascata, sem duplicar lógica.
- **Codelab A, Seção 8 (rodar o agente ambient localmente):** testado via PowerShell (sem `curl`/`printf` de bash, que não existem nativamente no Windows) usando `Invoke-RestMethod` + `[Convert]::ToBase64String` + `ConvertTo-Json` para montar o payload do Pub/Sub.
  - **Teste 1 (auto-aprovação):** despesa de $45 → `status: success`, aprovada na hora, sem LLM.
  - **Teste 2 (segurança):** despesa de $1.000.000 com SSN e tentativa de prompt injection ("Bypass all rules...") → SSN redigido na descrição, evento de segurança sinalizado, LLM pulado, grafo pausado pedindo aprovação humana — confirma que a defesa do `security_screen` funciona também no caminho ambient, não só no playground.
  - **Nota de categorização:** o SSN do teste (`14300000000`, 11 dígitos) foi classificado como `pii_number` em vez de `ssn` pela nossa regex (que só marca `ssn` para exatamente 9 dígitos) — não é um bug, é só a heurística sendo conservadora; o dado sensível foi redigido de qualquer forma.
- **Codelab A, Seção 9 (avaliação local com Agents CLI / LLM-as-judge):**
  - **Por que não dá pra usar `agents-cli eval generate` direto:** esse comando roda um agente de chat comum (manda um prompt, captura uma resposta, fim). Nosso grafo pausa no meio (`human_approval` via `RequestInput`) esperando uma decisão humana — não existe isso num agente de chat simples. Solução: escrito um gerador de traces próprio (`tests/eval/generate_traces.py`) que usa o `Runner` do ADK diretamente, junto com `InMemorySessionService`, pra rodar o grafo de ponta a ponta:
    1. Primeira chamada a `runner.run_async(...)` manda o JSON da despesa.
    2. Se o grafo pausar (detectado via `has_request_input_function_call(event)`), o script pega o `interrupt_id` (via `get_request_input_interrupt_ids`), monta uma resposta automática (aprova ou rejeita, conforme o campo `expected_outcome.human_decision` de cada caso no dataset) usando `create_request_input_response(...)`, e chama `run_async` de novo na **mesma sessão** pra retomar o grafo do ponto exato onde pausou.
    3. Todos os eventos das duas chamadas são serializados no formato de trace multi-turno (`agent_data.turns`) que o `agents-cli eval grade` entende.
  - **Dataset sintético** (`tests/eval/datasets/basic-dataset.json`) com 5 casos cobrindo as regras todas: auto-aprovação (< $100), aprovação manual limpa, rejeição manual limpa, leak de PII (cartão de crédito na descrição) e tentativa de prompt injection com SSN — os mesmos tipos de cenário já testados manualmente nas Seções 6 e 8, agora automatizados.
  - **`tests/eval/eval_config.yaml` reescrito** com duas métricas LLM-as-judge específicas do domínio (substituindo as métricas genéricas do scaffold, `custom_response_quality`/`agent_turn_count`, que não diziam nada sobre regras de negócio):
    - `routing_correctness` — audita se a regra do limiar de $100 foi respeitada (nada acima de $100 pode ser auto-aprovado pelo sistema; nada abaixo deveria acionar LLM/humano).
    - `security_containment` — audita se PII nunca aparece em texto puro depois do `security_screen`, e se toda tentativa de injeção foi roteada direto pro humano com o LLM pulado.
  - **`Makefile`:** adicionados os targets `generate-traces` (roda o script Python), `grade` (chama `agents-cli eval grade --config tests/eval/eval_config.yaml --traces artifacts/traces/`) e `eval` (atalho que encadeia os dois). `generate-traces` confirmado funcionando de ponta a ponta: 5 traces gerados em `artifacts/traces/generated_traces.json`.
  - **Bug 1 encontrado e corrigido:** `generate_traces.py` importava `create_request_input_response` etc. de `google.adk.events.request_input` — caminho errado (esse módulo só define a *classe* `RequestInput`). As três funções de retomada do HITL (`has_request_input_function_call`, `create_request_input_response`, `get_request_input_interrupt_ids`) vivem em `google.adk.workflow.utils._workflow_hitl_utils`, um módulo privado não exportado em nenhum `__init__.py` público — só achado lendo o código-fonte instalado da lib direto. Corrigido o import.
  - **Bug 2 encontrado — `prompt_template` (LLMMetric) sempre exige projeto GCP:** com `eval_config.yaml` usando `prompt_template`, o `agents-cli eval grade` roteia a avaliação pelo serviço gerenciado da **Vertex AI Evaluation Service**, que exige um projeto GCP configurado (`--project` / `GOOGLE_CLOUD_PROJECT` / `gcloud config set project`) — mesmo só pra usar a região "global". Isso contradiz a decisão tomada desde o Dia 3 de usar só a `GOOGLE_API_KEY` do AI Studio e evitar Vertex/billing do GCP. A documentação da skill (`references/metrics-guide.md`) sugere a saída: trocar para `custom_function` (métrica `CodeExecutionMetric`, `execution: "local"` — supostamente roda dentro do processo do CLI, sem projeto/região nenhum) e, dentro da função Python, chamar o modelo-juiz "na mão" via REST (`urllib.request`, só biblioteca padrão), lendo a `GOOGLE_API_KEY` do `.env`. Reescritas as duas métricas (`routing_correctness`, `security_containment`) nesse formato.
  - **Bug 3 encontrado — a troca para `CodeExecutionMetric` não resolveu, e o motivo é um bug/incompatibilidade real no SDK instalado:** mesmo com as duas métricas 100% locais, `make grade` continuou falhando com um erro genérico, sem traceback: `Error: Evaluation failed.`. Passos da investigação:
    1. Confirmado (com um script de diagnóstico temporário, `debug_metric.py`, depois removido) que o código Python das duas métricas roda sem erro nenhum quando chamado direto — o bug não estava na nossa lógica.
    2. Pedido `agents-cli eval grade --help` e `agents-cli --help` pra achar uma flag de verbose/debug — não existe nenhuma; só revelou o caminho do código-fonte (`cmd_grade.py`) instalado pelo `uv tool`.
    3. Com a permissão do usuário, ganhei acesso direto à pasta de instalação do `agents-cli` (`~/AppData/Roaming/uv/tools/google-agents-cli/`, fora do projeto) pra ler o código-fonte de verdade da CLI e do SDK `vertexai` que ela usa por trás.
    4. **Causa raiz encontrada em `vertexai/_genai/_evals_metric_handlers.py` (`_METRIC_HANDLER_MAPPING`):** a tabela de roteamento dessa versão do SDK decide qual "handler" usar pra cada métrica custom, em ordem. A primeira regra captura **qualquer** objeto do tipo `CodeExecutionMetric` — antes de verificar se a `execution` é `"local"` ou se a função já é um Python `Callable` — e manda pro `CustomCodeExecutionMetricHandler`, que **sempre** faz uma chamada HTTP real (`:evaluateInstances`) pro backend gerenciado da Vertex AI. A rota que de fato executa a função em processo, sem nenhuma chamada de rede (`CustomMetricHandler`), só é usada para um `types.Metric` genérico (não `CodeExecutionMetric`) — uma combinação que o `agents-cli` nunca produz a partir do YAML. Resultado: mesmo com `execution: "local"`, o `cmd_grade.py` chama `vertexai.Client(project=None, location=None)` e a tentativa de bater na API remota falha (sem projeto/região válidos), virando o "Evaluation failed." genérico — porque o `cmd_grade.py` engole qualquer exceção desse bloco. **Conclusão: a doc da skill (`metrics-guide.md`, "execução local sem projeto GCP") está desatualizada/incorreta para a versão do SDK que o `agents-cli setup` instalou; não existe forma de evitar o requisito de GCP usando `agents-cli eval grade` com métricas custom, mesmo seguindo a doc à risca.**
    5. **Solução adotada:** abandonar `agents-cli eval grade` (do mesmo jeito que já tínhamos abandonado `agents-cli eval generate` na Seção 9) e escrever `tests/eval/grade.py`, um script próprio que: lê `eval_config.yaml`, compila (`exec`) cada `custom_function` numa função Python real, junta o `prompt` do dataset original com o `agent_data` de cada trace gerado, roda `evaluate(instance)` direto (sem nenhum SDK da Vertex AI envolvido), agrega a média de score por métrica, e salva `artifacts/grade_results/results_<timestamp>.{json,md}`. `Makefile` (target `grade`) atualizado pra chamar esse script em vez do comando da CLI.
    6. **Primeiro `make grade` real (rodado pelo usuário):** 5 casos avaliados — `routing_correctness` médio 4.40/5, `security_containment` médio 5.00/5. Um caso (`manual_rejection_clean`) ficou com `routing_correctness` 2/5, com a explicação do juiz dizendo que o nó `security_screen` "foi inteiramente pulado" — o que contradizia o `security_containment` 5/5 do mesmo caso ("o estado final confirma que o security_screen executou"). Essa contradição entre as duas métricas no mesmo caso foi a pista de que o problema não era de lógica do agente, e sim de como o trace estava sendo registrado.
- **Bug 4 encontrado e corrigido — `generate_traces.py` perdia a identidade dos nós Python puros no trace:** investigando a contradição acima, comparei o trace bruto (`artifacts/traces/generated_traces.json`) do caso `manual_rejection_clean` e vi que os eventos de `parse_expense` e `security_screen` apareciam **ambos** com o mesmo `author`: `"expense_approval_workflow"` (o nome do workflow, não do nó) — enquanto o evento do `review_agent` (um `LlmAgent`) corretamente mostrava `"review_agent"`. Como os dois eventos genéricos ficavam idênticos e em sequência, o LLM-juiz não conseguia distinguir um do outro e concluiu (errado) que o `security_screen` nunca rodou.
  - **Causa raiz (lida no código-fonte instalado do `google-adk`):** em `google/adk/workflow/_workflow.py`, todo `Workflow` faz `ctx.event_author = self.name` (o nome do próprio workflow) uma vez, no início da execução. Em `google/adk/agents/context.py`, a propriedade `event_author` é herdada de pai para filho em todo `Context` novo (`self._event_author = parent_ctx.event_author if parent_ctx else ''`) — então **todo nó filho** (inclusive funções `@node` puras) herda esse valor genérico. Em `google/adk/workflow/_node_runner.py`, a linha `event.author = ctx.event_author or self._node.name` só usa o nome real do nó (`self._node.name`) se `ctx.event_author` estiver vazio — o que nunca é o caso dentro de um `Workflow`. Resultado: `event.author` é sistematicamente o nome do workflow para nós Python puros — e isso não é bug do ADK em si (é comportamento documentado/intencional: "Workflow sets this to its own name so all child events appear under the workflow's author"), só não é o campo certo pra reconstruir "qual nó gerou este evento".
  - **A pista da correção, no mesmo arquivo (`_node_runner.py`):** a linha seguinte, `event.node_info.path = ctx.node_path`, roda **sem condição nenhuma**, pra todo evento — esse campo sempre carrega o caminho real do nó (ex.: `"expense_approval_workflow@1/security_screen@1"`), independente do que `event.author` diz.
  - **Correção aplicada em `tests/eval/generate_traces.py`:** criada a função `_event_author(event)`, que lê `event.node_info.path`, pega o último segmento do caminho e remove o sufixo `@run_id`, devolvendo o nome limpo do nó real (`"security_screen"`, `"parse_expense"` etc.) — com fallback pro `event.author` antigo se `node_info`/`path` não existir por algum motivo. `_event_to_agent_event` passou a chamar essa função em vez de ler `event.author` direto.
  - **Resultado depois da correção:** `make generate-traces` + `make grade` rodados de novo — `routing_correctness` subiu para **5.00/5** em todos os 5 casos (incluindo o `manual_rejection_clean`, que tinha 2/5). `security_containment` teve uma falha pontual e não relacionada (`HTTP Error 503: Service Unavailable` numa chamada do modelo-juiz, no caso `manual_approval_clean`) — instabilidade temporária de API, não bug de código; re-rodado o `grade.py` (sem regenerar traces) e o score voltou a 5/5. **Médias finais: 5.00/5 nas duas métricas, nos 5 casos.**
  - **Lição central:** quando duas métricas independentes discordam sobre o "mesmo fato" dentro do mesmo trace, é um sinal forte de bug de *observabilidade* (como o trace foi registrado), não necessariamente de bug na lógica de negócio do agente — a lógica real (`security_screen.screened: true` no estado final) já estava correta desde a Seção 5; só o registro do evento no trace é que mentia sobre qual nó o produziu.

**Pendências conhecidas:**
- `tests/integration/test_agent.py` e `test_server_e2e.py` ainda mandam uma mensagem de chat livre pro agente — funcionava com o agente de exemplo (chat simples), mas não bate com o grafo novo (que espera um evento de despesa). Corrigidos só os imports/caminhos para não quebrar a coleta dos testes; ainda precisam ser reescritos (item separado da Seção 9, que cobre só os *evals*, não os testes unitários/integração do pytest).
- **Codelab A: Seção 9 (avaliação local) concluída e validada de ponta a ponta** — `make generate-traces` + `make grade` rodando 100% local (sem GCP/Vertex AI), com `routing_correctness` e `security_containment` em 5.00/5 nos 5 casos do dataset sintético.
- Codelab B (Secure AI Code) **em andamento** — ver sessão abaixo.

**Sessão de aplicação prática — Codelab B: Vibecode and Secure an AI Agent Lifecycle with Antigravity and TDD — 2026-06-20/21:**
- Codelab: [Vibecode and Secure an AI Agent Lifecycle with Antigravity and TDD](https://codelabs.developers.google.com/secure-agentic-coding).
- **Correção de fluxo combinada com o usuário:** ele pediu para eu instruir passo a passo, sempre mostrando os comandos de terminal exatos para ele rodar e acompanhar — em vez de eu executar tudo de uma vez no meu próprio sandbox. Esse é o ritmo seguido a partir daqui.
- **Seção 2-4 (setup, scaffold, lint):** projeto `shopping-assistant` criado via `agents-cli scaffold create`, com a vulnerabilidade simulada pedida pelo codelab (chave de API fake hardcoded em `app/agent.py`) e o tool `redeem_discount` (resgate de cupom único por usuário registrado, com `DISCOUNT_STORE` em memória).
- **Bug de API drift encontrado no lint (`ty check`):** o codelab pede `Gemini(model=..., api_key="...")`, mas a versão instalada do `google-adk` (2.2.0) **não tem** o campo `api_key` no modelo `Gemini` — ele lê a credencial da variável de ambiente `GOOGLE_API_KEY`. O `ty` (type checker) acusou `unknown-argument`, travando o lint mesmo com `ruff`/`codespell` passando. **Correção:** trocado para `os.environ["GOOGLE_API_KEY"] = "AIzaSyD-mock-key-value-12345"` antes de instanciar o `Gemini(model=...)` sem o kwarg — mantém a chave hardcoded em texto puro no arquivo (continua sendo a "isca" pro Semgrep pegar na Seção 10), só corrige a forma de passá-la pra biblioteca.
- **Bug de toolchain (uv sync por grupos):** `agents-cli lint` roda `uv sync --dev --extra lint` por baixo dos panos — isso desinstala qualquer pacote que não esteja nesses dois grupos, incluindo o grupo customizado `security` (`pre-commit`, `pre-commit-hooks`, `semgrep`) que tínhamos adicionado ao `pyproject.toml`. **Lição:** sempre que rodar `agents-cli lint`, reinstalar depois com `uv sync --group dev --group security --extra lint` antes de seguir para os passos de segurança (Seções 6 e 10).
- Lint final 100% verde: `ruff check`, `ruff format --check`, `codespell` e `ty check` todos passando.
- **Seção 5 (`.agents/CONTEXT.md`):** criado o arquivo de padrões seguros do projeto ("paved roads": validação de input via Pydantic, proibição de shell execution sem hook aprovado, e a regra do "loop de remediação" — se o commit falhar no Semgrep, tratar como tarefa de refatoração, corrigir, re-testar e tentar comitar de novo).
- **Diferença de terminal Windows:** o usuário roda os comandos no PowerShell (via Cursor), não bash — `cat > arquivo << 'EOF' ... EOF` (heredoc do bash) não existe no PowerShell. Equivalente usado: `@' ... '@ | Set-Content -Encoding utf8 arquivo` (here-string do PowerShell).
- **Bug de corrupção de indentação:** o here-string colado como bloco multi-linha corrompeu a indentação do YAML (`severity: ERROR` perdeu 2 dos 4 espaços à esquerda) — diagnosticado como um problema de "paste-reflow" do terminal/PSReadLine. **Correção adotada para toda criação de arquivo no Windows a partir daqui:** montar o conteúdo como uma única linha de comando PowerShell, usando `` `n `` (backtick-n) como escape de quebra de linha, em vez de colar um bloco multi-linha — isso evita o problema por completo.
- **Seção 6 (git hook): criados `.semgrep/rules.yaml`** (regra customizada via `pattern-regex` detectando o prefixo `AIzaSy` de chaves do Google) e **`.pre-commit-config.yaml`** (hooks `end-of-file-fixer`, `trailing-whitespace` e `semgrep --error`, todos `language: system`).
- **Descoberta estrutural: o Semgrep não roda nativamente no Windows.** Trilha de diagnóstico até a causa raiz:
  1. `uv run pre-commit run semgrep` falhou com um caminho de executável corrompido.
  2. `uv run semgrep ...` direto falhou com "Failed to spawn: program not found" — `Get-ChildItem .venv\Scripts` revelou que o `uv`/`pip` gerou os scripts `semgrep`/`pysemgrep` **sem extensão `.exe`** (shebang estilo Unix), que o Windows não consegue executar.
  3. `python -m semgrep` (sugestão do próprio Semgrep) está **deliberadamente bloqueado** desde a versão 1.38.0 — só imprime um aviso e sai sem escanear nada.
  4. Chamando o script Python por trás diretamente (`python .venv\Scripts\pysemgrep`), o traceback completo revelou a causa real: `ModuleNotFoundError: No module named 'resource'` — o Semgrep depende do módulo `resource`, que só existe em sistemas POSIX (Linux/Mac). **Não é um erro de configuração: é uma limitação estrutural da ferramenta no Windows.**
- **Decisão tomada com o usuário:** em vez de contornar esse (e os vários outros) problema específico do Windows, migrar todo o terminal de desenvolvimento para **WSL2 com Ubuntu** — ambiente Linux real, rodando dentro do Windows.
- **Migração para WSL2:** `wsl --install -d Ubuntu` (instalação inicial mostrou `docker-desktop`/`docker-desktop-data` como distros padrão — essas são internas do Docker Desktop, não ambientes de uso geral). Criado usuário Linux (`ilanschapira`), rodado `sudo apt update && sudo apt upgrade`, instalados `uv` e `git` dentro da Ubuntu. As pastas do Windows ficam acessíveis em `/mnt/c/...` — por isso os arquivos do projeto continuam no mesmo lugar (preservando o acesso via Cowork), só o terminal/ambiente de execução mudou.
- **Conectando o Cursor ao WSL:** usado o fluxo **"Connect via WSL"** (extensão Remote-WSL) — abre uma janela nova do Cursor já conectada ao Ubuntu; dentro dela, reabrir a pasta do projeto via *File > Open Folder*, navegando manualmente até `/mnt/c/Users/ilans/Claude/Projects/Kaggle-AI-Agents-MBA` (o diálogo de seleção de pasta abre, por padrão, na home do Linux — `/home/ilanschapira` —, não no disco Windows).
- **Bug ao re-rodar `uv sync` dentro do WSL:** falhou com `Operation not permitted` ao tentar copiar metadados de um pacote (`google-cloud-bigquery`) pro `.venv`. Causa: o `.venv` estava sendo criado dentro de `/mnt/c/...` (disco Windows montado via `drvfs`), e esse sistema de arquivos não suporta bem certas operações de cópia/permissão que o `uv` usa. **Correção:** manter o código no disco Windows, mas apontar o `.venv` para o disco Linux nativo via variável de ambiente `UV_PROJECT_ENVIRONMENT=~/.venvs/shopping-assistant` (tornada permanente no `~/.bashrc`).
- **Bug de git no WSL:** `git status` numa pasta de `/mnt/c/...` falhou com "detected dubious ownership in repository" — o git do Linux desconfia de pastas cujo "dono" (visto pelo Linux) não é o usuário atual, comum em discos Windows montados. Corrigido com `git config --global --add safe.directory <caminho>`.
- **Semgrep validado de verdade, dentro do WSL:** `uv run semgrep --error --config .semgrep/rules.yaml app/agent.py` encontrou corretamente a chave hardcoded (`AIzaSyD-mock-key-value-12345`) na linha 25 — confirmando que toda a migração resolveu o problema.
- **Bug de escopo no `pre-commit run --all-files`:** como o `.git` da raiz fica em `Kaggle-AI-Agents-MBA` (não em `shopping-assistant`), os hooks `end-of-file-fixer`/`trailing-whitespace` (sem nenhuma restrição de caminho) rodaram no **repositório inteiro**, "corrigindo" arquivos de outros dias do curso já finalizados. Revertido com `git checkout -- . ':!shopping-assistant'`, e corrigido o `.pre-commit-config.yaml` adicionando `files: ^shopping-assistant/` em cada hook, restringindo o escopo. Re-testado: escaneou só os 4 arquivos certos, e o Semgrep voltou a bloquear corretamente a chave hardcoded — gate de git validado de ponta a ponta.
- **Seção 6 (agent hook):** criado `.agents/hooks.json` com um hook `PreToolUse` (campo `matcher: "run_command"` — obrigatório, senão o agente roda comandos sem checagem nenhuma) chamando `.agents/scripts/validate_tool_call.py` com timeout de 10s. Criado o script de validação, que lê o contexto da chamada via `sys.stdin` (JSON), bloqueia comandos destrutivos (`rm -rf /`, `mkfs`) com `sys.exit(1)`, e aprova o resto com `sys.exit(0)`. Diferente do git hook (que só age no `git commit`), o agent hook intercepta o comando **antes** mesmo dele ser executado pelo agente de IA.
- **Trade-off entre os dois tipos de hook (lição do codelab):** git hooks rodam mesmo com o agente em modo autônomo, mas podem ser pulados com `git commit --no-verify`; agent hooks pegam o comando ainda "em trânsito" (mid-trajectory), mas não protegem nada se o desenvolvedor sair do IDE. Nenhum dos dois substitui um pipeline de CI/CD remoto e isolado, que é a barreira de segurança definitiva (não pode ser pulada localmente).

**Conceitos novos:**
- **Intent Drift / Trust Decay:** o agente, a cada iteração de "vibe coding", desvia um pouco do que foi pedido originalmente; pequenos desvios acumulados ao longo de várias iterações erodem a confiança no resultado final.
- **Vibe Diff:** resumo em linguagem simples (não o diff bruto de código) do que um agente alterou, pensado para que uma pessoa não-técnica consiga revisar e aprovar.
- **RequestInput:** classe do ADK 2.0 que, quando "yielded" dentro de um node do `Workflow`, pausa a execução do grafo e pede uma resposta humana antes de continuar.
- **RoutingMap:** um dicionário (`{"rota": nó}`) usado como açúcar sintático para declarar múltiplas arestas condicionais a partir de um único nó, sem escrever `Edge(...)` manualmente para cada uma.
- **`@node` (decorator):** transforma uma função Python comum em um `FunctionNode` válido dentro do grafo — equivalente mais moderno ao que era feito manualmente no Dia 3.
- **`ctx.state` como "mural compartilhado":** diferente do `node_input` (que só viaja de um nó para o próximo via aresta), `ctx.state` é visível por todos os nós do grafo a qualquer momento — por isso um nó em Python puro pode "fingir" ser o LLM e preencher um campo (`risk_assessment`) que outro nó downstream espera ler, sem que esse nó saiba a diferença.
- **Security screen (checkpoint pré-LLM):** padrão de colocar uma etapa determinística (regex, validação, regras) *antes* do nó que chama o LLM, para que dados sensíveis (PII) ou tentativas de ataque (prompt injection) nunca cheguem ao modelo.
- **`google.genai.types.Content`:** estrutura que o ADK usa para representar qualquer mensagem trocada com um modelo (`parts` + `role`); o playground/dev-ui embrulha *qualquer* entrada de chat nesse formato, mesmo quando o nó de entrada do grafo não é um LLM — por isso um node de entrada em Python puro precisa saber "desembrulhar" esse objeto.
- **Alias de campo no Pydantic (`Field(alias=...)` + `populate_by_name=True`):** permite que um modelo aceite um nome de campo diferente do nome "oficial" na hora de validar dados externos (ex.: payload manda `"amount"`, o modelo guarda como `amount_usd`), sem duplicar lógica de mapeamento manual.
- **Ambient agent / trigger endpoint:** agente que não espera um humano digitar — fica escutando eventos (Pub/Sub, Eventarc, upload de arquivo) e dispara o grafo sozinho a cada evento. No ADK 2.0, basta passar `trigger_sources=["pubsub"]` pro `get_fast_api_app()` que o endpoint `/apps/<agente>/trigger/pubsub` já vem pronto, sem código manual de decodificação.
- **Middleware HTTP (FastAPI/Starlette):** uma camada que intercepta toda requisição antes (ou depois) dela chegar no endpoint de destino — útil pra normalizar/validar dados sem precisar duplicar ou sobrescrever a rota original.
- **LLM-as-judge:** usar um segundo modelo (o "juiz") pra ler o trace completo de uma execução do agente e atribuir uma nota (1–5) com justificativa, em vez de comparar contra uma resposta exata — útil quando "certo" depende de seguir regras/processo, não de bater uma string fixa.
- **Trace (no contexto de avaliação):** o registro completo de uma execução do agente — todos os eventos, de qual nó rodou a qual decisão foi tomada — usado como evidência pro LLM-juiz analisar, em vez de só a resposta final.
- **`Runner` + `resume_inputs` (retomada programática de HITL):** fora do Playground/API, dá pra retomar uma pausa de `RequestInput` chamando `runner.run_async(...)` de novo na mesma sessão, mandando como `new_message` uma `Content` com um `function_response` (via `create_request_input_response`) — é exatamente isso que a UI faz por trás quando alguém clica "aprovar".
- **`LLMMetric` vs. `CodeExecutionMetric` (métricas custom do `agents-cli eval`):** `LLMMetric` (`prompt_template`) é avaliada pelo serviço gerenciado da Vertex AI — sempre exige um projeto GCP. `CodeExecutionMetric` (`custom_function`) *deveria*, segundo a doc da skill, rodar localmente com `execution: "local"` — mas na versão do SDK instalada pelo `agents-cli setup`, isso não é verdade: o roteamento interno (`_METRIC_HANDLER_MAPPING` em `vertexai/_genai/_evals_metric_handlers.py`) manda **toda** `CodeExecutionMetric` pro mesmo serviço remoto da Vertex AI, ignorando a flag `execution`. Por isso usamos um script próprio (`tests/eval/grade.py`) que executa a função Python direto, sem passar pelo `agents-cli`/SDK da Vertex AI nenhum — só assim o LLM-juiz roda de fato local, chamando a `GOOGLE_API_KEY` do AI Studio via REST puro.

**Glossário do dia:**
- **Slopsquatting:** ataque que registra um nome de pacote/biblioteca que um LLM "inventa" com frequência (hallucination) — quem instalar esse pacote alucinado cai numa armadilha.
- **AgBOM (Agent Bill of Materials):** inventário de tudo que compõe um agente (modelos, tools, skills, dependências) — pensado para rastreabilidade e auditoria de segurança.
- **"It Works Ship It":** a falácia de tratar "rodou sem erro uma vez" como prova de que o código está correto e pronto para produção.
- **Vibe Trajectory:** o caminho completo de prompts e decisões que levou a um determinado estado do código — não só o resultado final.
- **`ctx.resume_inputs` / `ctx.node_path`:** propriedades do `Context` do ADK 2.0; `resume_inputs` guarda respostas humanas já recebidas (indexadas por `interrupt_id`); `node_path` identifica de forma única a posição do node atual dentro do grafo.
- **`event.author` vs. `event.node_info.path`:** dentro de um `Workflow`, `event.author` pode ser sobrescrito pro nome do workflow (não do nó) — é assim "de propósito" no ADK, pra agrupar eventos sob um autor comum. Quem precisa saber exatamente *qual nó* gerou um evento (como um script de trace pra avaliação) deve usar `event.node_info.path`, que é sempre o caminho real do nó, nunca sobrescrito.

**Conceitos novos (Codelab B):**
- **"Paved road" / CONTEXT.md:** arquivo de contexto persistente com convenções de segurança pré-aprovadas do projeto — evita que o agente "invente" um jeito de fazer algo (potencialmente inseguro) recorrendo só à memória de treinamento.
- **Context rot:** degradação da qualidade de raciocínio do agente quando se sobrecarrega o contexto com documentação genérica demais — por isso o `CONTEXT.md` deve ser curto e específico, carregado sob demanda.
- **Pre-Commit Remediation Loop:** regra de processo (não de código) que instrui o agente a tratar uma falha de pre-commit hook (ex.: Semgrep) como uma tarefa de refatoração — corrigir, re-testar, tentar comitar de novo — em vez de usar `--no-verify` pra simplesmente pular o hook.
- **Git Hook vs. Agent Hook (trade-off):** o git hook é nativo do controle de versão — roda mesmo com o agente em modo autônomo, mas pode ser pulado com `--no-verify`. O agent hook intercepta a ação ainda dentro do IDE/agente, antes de executar — mais "preventivo", mas inútil se o desenvolvedor sair do IDE e rodar comandos direto no sistema. Nenhum dos dois substitui um CI/CD remoto, que é a barreira que não pode ser pulada localmente.
- **WSL2 (Windows Subsystem for Linux) e `drvfs`:** o WSL2 roda um kernel Linux real dentro do Windows; pastas do Windows ficam acessíveis em `/mnt/c/...` através de um driver de sistema de arquivos chamado `drvfs`, que tem limitações conhecidas de permissões/hardlinks comparado a um disco Linux nativo — a causa de vários bugs nesta sessão.

**Glossário do dia (Codelab B):**
- **`uv sync --group X --extra Y`:** o `uv` só instala/mantém os grupos e extras (`[dependency-groups]` / `[project.optional-dependencies]`) explicitamente listados no comando — qualquer pacote de um grupo não citado é desinstalado. Por isso ferramentas como `agents-cli lint` (que chama `uv sync` com um conjunto fixo de grupos) podem remover pacotes de outros grupos do mesmo projeto sem avisar.
- **Here-string (PowerShell):** sintaxe `@' ... '@` para texto multi-linha literal — equivalente ao heredoc (`<< 'EOF'`) do bash, usado para gravar arquivos com conteúdo de várias linhas direto no terminal. Em blocos multi-linha colados no terminal, pode sofrer corrupção de indentação ("paste-reflow") — a alternativa mais segura no Windows é montar o conteúdo numa única linha com `` `n `` como escape de quebra de linha.
- **`ty` (type checker) vs. comportamento em runtime:** um Pydantic model pode "engolir" silenciosamente um argumento desconhecido em tempo de execução (sem erro), mas isso não significa que o campo seja válido — um type checker estático como o `ty` ainda vai reportar `unknown-argument`, porque ele valida contra a definição real da classe, não contra o que "funcionou na prática".
- **`UV_PROJECT_ENVIRONMENT`:** variável de ambiente que diz ao `uv` onde criar o `.venv`, independente de onde está o código do projeto — usada para manter o código em `/mnt/c/...` (Windows) mas o ambiente virtual num disco Linux nativo, evitando os bugs de permissão do `drvfs`.
- **`git config --global --add safe.directory`:** comando que diz ao git para confiar numa pasta específica mesmo quando o "dono" do arquivo (do ponto de vista do sistema operacional) não é o usuário atual — necessário em repositórios dentro de discos Windows montados no WSL.
- **`matcher` (em hooks de agente):** campo que define *qual* ferramenta/ação um hook deve interceptar (ex.: `"run_command"`). Sem ele, o hook não filtra nada e o agente roda ações sem checagem.
- **`sys.stdin` / código de saída (`exit code`):** forma de um script de validação "conversar" com quem o chamou — recebe dados (aqui, um JSON com o comando que o agente quer rodar) pela entrada padrão, e devolve a decisão pelo código de saída (`0` = aprovado, qualquer outro valor = bloqueado).
- **`files:` (escopo de hook no pre-commit):** expressão regular que restringe um hook a um subconjunto de caminhos do repositório — essencial em monorepos, para não aplicar correções automáticas em pastas de outros projetos sem querer.

### Seção 7 — Skill de Threat Modeling STRIDE

**O que foi feito:** criamos uma skill customizada do Antigravity, `stride-threat-model` (`shopping-assistant/.agents/skills/stride-threat-model/SKILL.md`), que documenta o processo de análise de segurança usando o framework STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Aplicamos essa skill de fato sobre `app/agent.py` (o agente `ShoppingHelper` e sua tool `redeem_discount`), gerando `shopping-assistant/threat_model.md`.

**Principais achados do threat model:**
- **Spoofing:** `user_id` é só uma string decidida pelo próprio LLM a partir da conversa — não há autenticação real, só uma checagem de prefixo (`guest_`).
- **Tampering:** a chave de API hardcoded (já conhecida, alvo do Semgrep) + uma race condition no dicionário `DISCOUNT_STORE` (duas chamadas simultâneas podem ambas passar pela verificação "já foi usado?" antes de qualquer uma marcar o código como usado).
- **Repudiation:** nenhuma redenção é logada — impossível auditar quem usou o quê.
- **Information Disclosure:** a chave hardcoded de novo, e mensagens de erro que permitem "enumerar" quais códigos de desconto existem.
- **Denial of Service:** sem rate limiting nem isolamento por usuário na tool.
- **Elevation of Privilege:** como `user_id` e `code` são preenchidos pelo LLM a partir do texto da conversa (não por uma fonte autenticada), a tool é vulnerável a prompt injection — um usuário poderia escrever um prompt que convence o modelo a redimir um código em nome de outro `user_id`.

**Conceito-chave:** o risco mais sério não é só "o código tem uma chave hardcoded" — é que a tool inteira confia em argumentos (`user_id`, `code`) que o modelo decide a partir da conversa, em vez de vir de uma fonte autenticada fora do alcance do LLM. Isso conecta Spoofing, Tampering e Elevation of Privilege num único ponto de origem.

### Seção 8 — Gate da fase de Plan (TDD Planning Gate)

**O que foi feito:** adicionamos uma nova regra ao final de `shopping-assistant/.agents/CONTEXT.md` — o **TDD Planning Gate**. A partir de agora, toda vez que o agente entrar na fase de Plan (antes de gerar código), ele é obrigado a decompor a tarefa em estágios lógicos *e* incluir uma seção dedicada de **Security Boundaries & Assertions**, listando casos de borda que poderiam explorar a feature.

**Teste do gate**: geramos três `implementation_plan.md` de demonstração (sem implementar nenhuma tool de fato), em `shopping-assistant/.agents/test-plans/`, simulando o que o Antigravity mostraria antes de pedir aprovação:
- `award_loyalty_points`: risco de pontos negativos/zero, dupla concessão pra mesma compra (replay), `user_id` não-autenticado.
- `process_cart_checkout`: condição de corrida no checkout duplicado, total de pedido que deve ser recalculado no servidor (nunca confiar no valor vindo do LLM), `cart_id` de outro usuário (IDOR).
- `update_discount_status`: elevação de privilégio (tool administrativa), ausência de log de auditoria, abuso de disponibilidade por credencial comprometida.

**Conceito-chave (timing dos mecanismos de segurança até agora)**:
- **`CONTEXT.md`** → lido *antes* de planejar — molda como o agente pensa e propõe a solução.
- **Agent Hook** (`.agents/hooks.json`) → intercepta *durante* a execução, antes de uma tool/comando rodar.
- **Git Hook** (`pre-commit`) → roda *depois* do código pronto, no momento do commit.
- **CI/CD remoto** (ainda não implementado neste projeto) → a única camada que não pode ser pulada localmente.
Cada camada gateia o processo em um ponto diferente da linha do tempo — juntas formam defesa em profundidade, nenhuma sozinha é suficiente.

**Status:** commit `141f5fb` pushado com sucesso para `origin/main` (`shopping-assistant/.agents/CONTEXT.md`, os 3 `implementation_plan.md` de teste, e o Diário).

**Troubleshooting (fora do código, mas registrado por ser útil):** o `git push` falhou uma vez com `Could not resolve host: github.com` — não era erro de git, e sim DNS do WSL2 desatualizado (comum após o PC dormir/trocar de rede). Resolvido forçando um servidor DNS conhecido: `echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf`, depois repetindo só o `git push` (sem precisar refazer add/commit).

### Seção 9 — Testes de segurança outcome-based (fase GREEN do TDD)

**O que foi feito:** criado `shopping-assistant/tests/test_agent.py` com 3 testes de segurança para a tool `redeem_discount`, seguindo dois princípios centrais:
- **Assert on outcomes, not interactions**: os testes verificam a string de retorno final e o estado do `DISCOUNT_STORE` depois da chamada — nunca espionam *como* a função chegou lá (sem mocks de chamadas internas). Isso torna o teste resiliente a refatorações internas que não mudem o comportamento.
- **Enforce Strict Guardrails**: cada teste cobre uma regra de negócio/segurança específica já identificada no `threat_model.md` (Seção 7): código de uso único, código inválido, conta guest sem permissão.

**Testes**:
1. `test_discount_code_can_only_be_redeemed_once` — primeira redenção com sucesso, segunda (mesmo código, usuário diferente) bloqueada.
2. `test_discount_redemption_rejects_invalid_code` — código inexistente é rejeitado.
3. `test_discount_redemption_rejects_guest_accounts` — usuário `guest_*` não pode redimir, e o estado do store permanece inalterado (`False`).

**Fixture de isolamento**: `reset_store` (`@pytest.fixture(autouse=True)`) zera o `DISCOUNT_STORE` antes *e* depois de cada teste (via `yield`), garantindo que a ordem de execução dos testes não afete o resultado.

**Validação (fase GREEN):** `uv run pytest tests/test_agent.py` → **3 passed**. Dois avisos cosméticos, sem impacto: `PytestCacheWarning` (de novo o `drvfs`, não conseguindo escrever cache em `/mnt/c/...`) e um `DeprecationWarning` interno do `google-adk` (`BaseAgentConfig`), não relacionado ao nosso código.

### Seção 10 — Verificar o gating e a autocorreção do agente

**O que foi feito:** demonstramos o ciclo completo Refactor-and-Commit do TDD, com o gate de git de verdade bloqueando e depois liberando um commit.

- **Primeira tentativa de commit não disparou nada:** `agent.py` já estava commitado desde a Seção 2-4 sem nenhuma mudança — `git add .` não tinha diff pra commitar, então o pre-commit nem rodou nos arquivos certos. Adicionada uma linha de comentário trivial em `agent.py` (mantendo a chave hardcoded) só pra criar uma mudança real e poder reproduzir a demonstração do codelab.
- **Falha real do Semgrep observada:** `uv run git commit` (sem `--no-verify`, de propósito) disparou o hook e o Semgrep bloqueou o commit, apontando exatamente a linha 25 (`Security Issue: Hardcoded Google API key prefix detected.`) — o mesmo "Pre-Commit Remediation Loop" documentado no `CONTEXT.md` desde a Seção 5.
- **Refactor de segurança aplicado em `shopping-assistant/app/agent.py`:** removida a chave hardcoded; adicionado `load_dotenv(Path(__file__).resolve().parent / ".env")` (carregando `app/.env`, já no `.gitignore`) e uma checagem explícita (`RuntimeError`) caso `GOOGLE_API_KEY` não esteja definida. Criado `shopping-assistant/app/.env.example` (placeholder seguro, esse sim versionado) documentando o formato esperado.
- **Pytest re-validado depois do refactor:** `uv run pytest tests/test_agent.py` → 3 passed — confirma que a correção de segurança não quebrou nenhum guardrail de negócio.
- **Segunda tentativa de commit: sucesso.** Com a chave removida, o Semgrep não encontrou mais nada para reportar, e o commit (`fix(security): load GOOGLE_API_KEY from .env instead of hardcoding it`) passou e foi enviado ao GitHub.

**Conceito-chave:** o valor real do gate local não é só *bloquear* — é fechar o ciclo: bloquear → ler o erro → refatorar → re-testar → tentar de novo, tudo localmente, antes de qualquer push. Isso evita gastar um ciclo de CI/CD remoto (mais lento) só para descobrir um problema que podia ter sido pego na própria máquina do desenvolvedor.

### Seção 11 — Rodar e testar o agente localmente

**O que foi feito:** validado o agente `ShoppingHelper` de ponta a ponta no ADK Dev UI (playground), já com a chave de API carregada de forma segura (Seção 10).

- **Instalação faltante identificada:** o `agents-cli` é uma ferramenta global (`uv tool`), não uma dependência do projeto — nunca tinha sido instalada no ambiente WSL novo. Resolvido com `uvx google-agents-cli setup` + `agents-cli login -i` (opção Gemini API Key).
- **`GEMINI_API_KEY` vs. `GOOGLE_API_KEY`:** reapareceu a mesma pegadinha do Dia 3 — `GEMINI_API_KEY` precisa ser exportada a cada terminal novo e só é usada pelo `agents-cli` (login/CLI), enquanto o `agent.py` lê `GOOGLE_API_KEY` do `app/.env` (Seção 10). São duas chaves/variáveis com propósitos diferentes, mesmo que o valor real seja a mesma chave do AI Studio.
- **Erro `400 API_KEY_INVALID` no playground:** causa raiz era o `app/.env` ainda com o placeholder `YOUR_API_KEY` — corrigido editando o arquivo direto no Cursor com a chave real.
- **Teste final no Dev UI:** prompt `"Can you redeem the discount code WELCOME50 for user user_123?"` → o agente chamou a tool `redeem_discount`, que teve sucesso (`user_123` não começa com `guest_`, então passa como usuário registrado) → resposta confirmando a redenção. Trace visível no painel de eventos: `ShoppingHelper` → `redeem_discount` (chamada) → `redeem_discount` (retorno) → resposta final.

**Status: Codelab B (Vibecode and Secure an AI Agent Lifecycle with Antigravity and TDD) concluído — Seções 1 a 11.**

## Dia 5 — *(a iniciar)*

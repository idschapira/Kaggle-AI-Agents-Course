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

## Dia 4 — *(a iniciar)*

## Dia 5 — *(a iniciar)*

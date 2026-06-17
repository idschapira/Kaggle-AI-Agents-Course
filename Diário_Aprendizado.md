# Diário de Aprendizado — 5-Day AI Agents (Kaggle)

> Registro de progresso do curso, mantido sessão a sessão pelo Tutor de Engenharia de Dados.

## Sobre este projeto
- **Curso:** 5-Day AI Agents (Kaggle)
- **Aluno:** Ilan (MBA em curso)
- **Objetivo:** Aprender conceitos de AI Agents e Engenharia de Dados na prática, documentando tudo aqui e versionando no GitHub.

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

## Dia 3 — *(a iniciar)*

## Dia 4 — *(a iniciar)*

## Dia 5 — *(a iniciar)*

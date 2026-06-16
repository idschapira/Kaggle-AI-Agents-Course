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

**Objetivo da
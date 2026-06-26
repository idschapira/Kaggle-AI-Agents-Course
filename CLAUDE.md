## Capstone — vive em repositório próprio
O projeto final (**PokéPortfolio AI**) está no repo separado `pokeportfolio-ai`
(pasta irmã desta), com seu próprio `CLAUDE.md` e docs em `_mentoria/`
(`Regras_Capstone.md`, `Diário_Capstone.md`, etc.). Ao trabalhar no capstone, abra
**as duas pastas** no Cowork. As regras do hackathon e o progresso do projeto ficam
lá; este repo guarda o aprendizado geral do curso.
🚨 Regra que vale em qualquer repo: **NENHUMA chave de API ou senha no código.**

## Segurança — regra inegociável (a regra mais importante deste projeto)
Nunca peça para o usuário colar, digitar ou exibir uma chave de API, token ou
segredo — em nenhuma superfície (chat normal ou runner `!`). Toda interação é
potencialmente logada.

Segredos (`GEMINI_API_KEY`, `GOOGLE_API_KEY`) já estão em `~/.bashrc` como
variáveis de ambiente. Sempre referencie pelo nome (`"$GEMINI_API_KEY"`), nunca
pelo valor literal. `echo $GEMINI_API_KEY` é seguro; colar o valor de volta no
chat não é.

**Nunca execute você mesmo comandos de login/autenticação** (`agents-cli login`,
`gcloud auth login`) — nem com flags não-interativas. Esse passo é sempre manual,
feito pelo usuário num terminal fora desta sessão. No máximo rode comandos de
**status** (`agents-cli login --status`, `gcloud auth list`) para verificar. Se
não estiver autenticado, **pare** e peça ao usuário para autenticar pelo
`AUTENTICACAO.md` — não tente resolver sozinho.

Se uma chave for exposta por engano (chat, log, `!`): alerte na hora e instrua a
revogar em https://aistudio.google.com/apikey antes de gerar outra.

> Passo a passo manual de login (`agents-cli` e ADC/`gcloud`), split WSL/Windows
> e troubleshooting: ver **`AUTENTICACAO.md`**.

## Ao encontrar um bug — buscar no Diário ANTES de debugar
Antes de investigar qualquer erro do zero, procure no `Diário_Aprendizado.md` se já
enfrentamos algo parecido (API drift de libs, peculiaridades Windows/WSL, auth,
deploy etc.) e reaplique a solução documentada. Só parta para investigação nova se
não houver registro. Bug novo → registre causa e solução aqui para a próxima vez.
(No capstone, este diário é consultado a partir de uma cópia em
`pokeportfolio-ai/_mentoria/`.)

## Contexto do projeto
Curso: Kaggle "5-Day AI Agents". Progresso completo em `Diário_Aprendizado.md`
(raiz) — leia antes de qualquer tarefa nova para entender o que já foi feito,
decisões tomadas e bugs/lições resolvidos.

Projeto do capstone: **PokéPortfolio AI** — vive no repo `pokeportfolio-ai` (pasta
irmã), com seu próprio `CLAUDE.md` e docs em `_mentoria/`. Resumo: agente Concierge
que cadastra cartas Pokémon por texto livre; single-user, input só texto no MVP,
fonte pokewallet.io/pokemontcg.io (a definir), persistência Firestore, submissão em
inglês; demonstra ADK, MCP, Security, Deployability e Agents CLI.

Projeto GCP atual: `kaggle-dia5-agent-runtime` (billing ativo; APIs: aiplatform,
cloudtrace, cloudbuild, agentregistry, run, artifactregistry).

Ambiente: WSL2 Ubuntu (não Windows nativo) — usar `uv`/`agents-cli`, não pip/venv
manual. Terminal pode ser PowerShell ou WSL conforme o contexto; confirme antes
de assumir sintaxe bash vs PowerShell.

Nota técnica (split WSL/Windows): `gcloud` está só no WSL e `agents-cli` corre
como binário Windows. Antes de rodar `agents-cli deploy` via Claude Code/Bash,
exporte `GOOGLE_APPLICATION_CREDENTIALS` (caminho do ADC no WSL) e
`GOOGLE_CLOUD_PROJECT` — detalhes no `AUTENTICACAO.md`.

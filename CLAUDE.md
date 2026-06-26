## Regras do Capstone (LER ANTES de trabalhar no projeto final)
As regras oficiais completas estão em `Regras_Capstone.md` (raiz desta pasta) —
leia esse arquivo antes de qualquer decisão sobre a submissão final. Resumo das
regras inquebráveis:

- **Hackathon = 1 (uma) submissão por equipe.** "Salvar" ≠ "Submeter": clicar em
  **Submit** na Writeup antes do prazo. Rascunhos não são avaliados.
- **Submissão válida = Kaggle Writeup** (≤2.500 palavras) + 3 anexos obrigatórios:
  **imagem de capa**, **vídeo no YouTube (≤5 min)** e **link público** (demo OU
  repositório GitHub com README + setup).
- **Demonstrar ≥3 conceitos do curso:** Agent/Multi-agent (ADK), MCP Server,
  Antigravity, Security, Deployability, Agent skills (Agents CLI). Uso de agentes
  deve ser claro, central e significativo.
- **Selecionar 1 das 4 tracks** é obrigatório para submeter.
- 🚨 **NENHUMA chave de API ou senha no código/submissão.**
- **Prazo:** confirmar na aba *Overview > Timeline* da competição (~06/07/2026 PT,
  a verificar — não confiar na memória).

### Ferramentas externas (Claude Code, Cursor, Copilot etc.)
Permitido usar ferramentas além do codelab para *construir* o projeto (Seção 2.6
das regras: não proibidas pelo Host + custo razoável/acessível a todos). MAS:
ferramenta de build ≠ conceito avaliado — a submissão ainda precisa **conter e
mostrar** os ≥3 conceitos do curso. Código open-source reaproveitado só sob
licença OSI.

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

## Ao encontrar um bug — buscar nos Diários ANTES de debugar
Antes de investigar qualquer erro do zero, procure **nos dois diários** se já
enfrentamos algo parecido (API drift de libs, peculiaridades Windows/WSL, auth,
deploy etc.) e reaplique a solução documentada. **Ambos valem durante o capstone:**
o `Diário_Aprendizado.md` concentra as lições técnicas do curso (que reaparecem ao
construir o projeto) e o `Diário_Capstone.md` registra o que é específico do projeto
final. Só parta para investigação nova se não houver registro em nenhum dos dois. Ao
resolver um bug inédito, registre a causa e a solução no diário correspondente
(técnico → Aprendizado; específico do projeto → Capstone) para a próxima vez.

## Contexto do projeto
Curso: Kaggle "5-Day AI Agents". Progresso completo em `Diário_Aprendizado.md`
(raiz) — leia antes de qualquer tarefa nova para entender o que já foi feito,
decisões tomadas e bugs/lições resolvidos.

Projeto do capstone: **PokéPortfolio AI** — agente Concierge que cadastra cartas
Pokémon por texto livre. Decisões, escopo e progresso em `Diário_Capstone.md`
(raiz) — leia antes de qualquer tarefa do projeto final. Resumo: track Concierge,
single-user, input só texto no MVP, fonte de dados pokewallet.io/pokemontcg.io
(a definir), persistência Firestore, submissão em inglês; demonstra ADK, MCP,
Security, Deployability e Agents CLI.

Projeto GCP atual: `kaggle-dia5-agent-runtime` (billing ativo; APIs: aiplatform,
cloudtrace, cloudbuild, agentregistry, run, artifactregistry).

Ambiente: WSL2 Ubuntu (não Windows nativo) — usar `uv`/`agents-cli`, não pip/venv
manual. Terminal pode ser PowerShell ou WSL conforme o contexto; confirme antes
de assumir sintaxe bash vs PowerShell.

Nota técnica (split WSL/Windows): `gcloud` está só no WSL e `agents-cli` corre
como binário Windows. Antes de rodar `agents-cli deploy` via Claude Code/Bash,
exporte `GOOGLE_APPLICATION_CREDENTIALS` (caminho do ADC no WSL) e
`GOOGLE_CLOUD_PROJECT` — detalhes no `AUTENTICACAO.md`.

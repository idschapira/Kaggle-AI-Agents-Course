## Segurança — regra inegociável
Nunca peça para o usuário colar, digitar ou exibir uma chave de API, token ou
qualquer segredo nesta conversa, em nenhuma circunstância — nem na caixa de
chat normal, nem em runners de comando (`!`). Toda interação com este agente é
potencialmente registrada/logada.

Segredos (ex.: GEMINI_API_KEY, GOOGLE_API_KEY) já estão definidos como
variáveis de ambiente em ~/.bashrc. Sempre referencie-os via variável de shell
(ex.: "$GEMINI_API_KEY"), nunca como valor literal. Para autenticação de CLIs
(agents-cli, gcloud), prefira sempre flags não-interativas; evite `-i`/modo
interativo, que tende a travar quando executado por um agente em vez de um
terminal real com humano digitando.

Se uma chave for exposta por engano nesta conversa, alerte o usuário
imediatamente e instrua a revogar em https://aistudio.google.com/apikey.

**Nunca execute, você mesmo, comandos de login/autenticação de nenhuma CLI**
(`agents-cli login`, `gcloud auth login`, etc.) — mesmo com flags
não-interativas. Esse passo deve ser sempre feito manualmente pelo usuário,
num terminal fora desta sessão, antes de você começar a trabalhar. Assuma que
a autenticação já foi feita; no máximo, rode comandos de **status/verificação**
(ex.: `agents-cli login --status`) para confirmar — nunca um comando que
escreva, injete ou processe a credencial. Se a verificação mostrar
"não autenticado", pare e peça ao usuário para autenticar manualmente fora
desta sessão, em vez de tentar resolver isso você mesmo.

## Protocolo de login seguro do agents-cli / gcloud (passo a passo)
Sempre que for preciso autenticar uma ferramenta (`agents-cli`, `gcloud`), siga
exatamente esta sequência — nunca improvise um comando alternativo:

1. **Rode só um comando de status/verificação**, nunca um comando de login:
   - `agents-cli login --status`
   - `gcloud auth list` (sem executar o login propriamente)
2. **Se já estiver autenticado** (status mostra usuário/projeto válido): siga
   normalmente com a tarefa, sem tocar em nenhuma credencial.
3. **Se não estiver autenticado**: pare imediatamente. Não tente "ajudar"
   sugerindo `agents-cli login -i`, `gcloud auth login`, nem qualquer comando
   que vá pedir para o usuário colar uma chave/token na conversa. Em vez
   disso, devolva ao usuário uma instrução assim (pedindo para ele rodar fora
   desta sessão, nunca aqui no chat nem com `!`):
   ```
   Preciso que você autentique manualmente, num terminal comum fora desta
   sessão:
     agents-cli login -i
   Depois disso, volte aqui e me avise — ou abra uma sessão nova do Claude
   Code, que já vai herdar a autenticação automaticamente.
   ```
4. **Nunca digite, monte ou complete um comando contendo o valor literal de
   uma chave/token** — nem dentro do chat normal, nem no runner `!`. Se uma
   variável de ambiente já existe (`$GEMINI_API_KEY`, `$GOOGLE_API_KEY`),
   referencie-a só pelo nome (`echo $GEMINI_API_KEY` é seguro de rodar; colar
   o valor de volta no chat não é).
5. **Se precisar editar/persistir uma variável de ambiente** (ex.: corrigir
   uma chave revogada), instrua o usuário a editá-la num terminal puro, fora
   da sessão do agente: `sed -i '/NOME_DA_VAR/d' ~/.bashrc && echo
   'export NOME_DA_VAR="..."' >> ~/.bashrc && source ~/.bashrc` — e depois
   pedir para reiniciar a sessão do agente, que herda a variável sem nunca
   precisar exibi-la.
6. **Se uma chave aparecer exposta em qualquer momento** (chat, log, `!`
   runner): alertar o usuário na hora e instruir revogação em
   https://aistudio.google.com/apikey antes de gerar uma nova.

## Contexto do projeto
Curso: Kaggle "5-Day AI Agents". Progresso completo documentado em
`Diário_Aprendizado.md` na raiz desta pasta — leia esse arquivo antes de
qualquer tarefa nova para entender o que já foi feito, decisões tomadas, e
bugs/lições já resolvidos (API drift de libs, peculiaridades do Windows/WSL,
etc.).

Projeto GCP atual: kaggle-dia5-agent-runtime (billing ativo, APIs habilitadas:
aiplatform, cloudtrace, cloudbuild, agentregistry, run, artifactregistry).

Ambiente: WSL2 Ubuntu (não Windows nativo) — usar `uv`/`agents-cli`, não pip/venv
manual. Terminal é PowerShell ou WSL conforme o contexto; confirme antes de
assumir sintaxe bash vs PowerShell.
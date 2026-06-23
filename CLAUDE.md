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

## Checklist do usuário: como autenticar o agents-cli sem stress (manual rápido)
Isto é o passo a passo pra **você (humano)** seguir sempre que precisar logar ou
relogar o `agents-cli` — destilado de todos os incidentes do Dia 3 e Dia 5.
Claude (chat ou Code) nunca deve participar da etapa 2.

1. **Abra um terminal Ubuntu/WSL "de verdade"** — ícone do Ubuntu, ou `wsl` a
   partir do Windows Terminal. **Nunca** use a aba "Code" embutida do Cowork
   nem o runner `!` de dentro de uma sessão de IA pra essa etapa: nenhuma
   superfície de agente é segura pra isso, e a aba Code já demonstrou rodar em
   ambiente inconsistente (PowerShell em vez de WSL, shell não-interativo que
   não carrega `.bashrc`).
2. **Confira se a variável já existe** (sem mostrar o valor):
   ```bash
   [ -n "$GEMINI_API_KEY" ] && echo "definida" || echo "vazia"
   ```
3. **Se estiver vazia ou a chave foi revogada**, edite o `~/.bashrc` direto
   (nunca cole a chave em nenhum chat de IA):
   ```bash
   sed -i '/GEMINI_API_KEY/d' ~/.bashrc
   echo 'export GEMINI_API_KEY="SUA_CHAVE_AQUI"' >> ~/.bashrc
   source ~/.bashrc
   ```
4. **Logue o `agents-cli` nesse mesmo terminal puro:**
   ```bash
   agents-cli login -i
   ```
   (escolha a opção **Gemini API Key**). Confirme com:
   ```bash
   agents-cli login --status
   ```
5. **Só depois de ver "autenticado" no passo 4**, abra/reabra o Claude Code
   (terminal ou aba Code) — ele herda a autenticação automaticamente, sem
   nunca precisar ver a chave.
6. **Se o `agents-cli: command not found` aparecer** num terminal novo mesmo
   depois de tudo isso: é quase certo que esse terminal não está carregando o
   `~/.bashrc` (ex.: é a aba Code, não um terminal nativo). Diagnóstico rápido:
   ```bash
   cat ~/.profile | grep -A3 bashrc   # confirma o encadeamento .profile→.bashrc
   source ~/.bashrc                    # corrige a sessão atual na hora
   which agents-cli                    # deve apontar pra ~/.local/bin/agents-cli
   ```

## Checklist do usuário: ADC (gcloud) — necessário antes de qualquer deploy
Autenticação do `agents-cli`/Gemini API Key (checklist acima) é **separada** da
autenticação do `gcloud`/ADC (Application Default Credentials) — comandos como
`agents-cli deploy` precisam das duas. Faltar a ADC dá um erro de import
(`google.auth.default()` sem credenciais), não um erro óbvio de "não logado".

1. **Antes de rodar qualquer `agents-cli deploy` (real ou `--dry-run` que
   precise importar o app), verifique a ADC primeiro**, num terminal puro:
   ```bash
   gcloud auth application-default print-access-token
   ```
   Deve imprimir um token longo (não um erro). **Não cole esse token em
   nenhum chat de IA** — é só pra confirmar visualmente que funcionou.
2. **Se der erro** (sem credenciais), autentique manualmente, no mesmo
   terminal puro, fora de qualquer sessão de agente:
   ```bash
   gcloud auth application-default login
   gcloud config set project kaggle-dia5-agent-runtime
   ```
3. Só depois de confirmar o passo 1 com sucesso, volte para o Claude Code (ou
   abra uma sessão nova — ela herda a ADC automaticamente) e siga com o
   deploy.

**Atenção — split WSL/Windows:** `gcloud` está instalado só no WSL; `agents-cli`
corre como binário Windows. As credenciais ADC do WSL ficam em
`//wsl$/Ubuntu/home/ilanschapira/.config/gcloud/application_default_credentials.json`
e são **invisíveis** para o processo Windows por padrão. Solução: antes de
rodar `agents-cli deploy` a partir do Claude Code / Bash tool, exporte:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="//wsl$/Ubuntu/home/ilanschapira/.config/gcloud/application_default_credentials.json"
export GOOGLE_CLOUD_PROJECT="kaggle-dia5-agent-runtime"
```
(Claude Code faz isso automaticamente agora — veja os deploys registados no
`Diário_Aprendizado.md`.)

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
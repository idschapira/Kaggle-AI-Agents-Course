# 🔐 Autenticação — passo a passo manual (agents-cli e gcloud/ADC)

> Companheiro do `CLAUDE.md`. Aqui ficam os **checklists que VOCÊ (humano)** executa
> num terminal real. O Claude (chat ou Code) **nunca** participa das etapas de login —
> no máximo roda comandos de *status* para verificar. Destilado dos incidentes do
> Dia 3 e Dia 5.

---

## Regra de ouro (vale para tudo abaixo)
- **Nunca** cole o valor de uma chave/token em nenhum chat de IA, nem no runner `!`.
- Variáveis de ambiente já existentes (`$GEMINI_API_KEY`, `$GOOGLE_API_KEY`):
  referencie só pelo nome. `echo $GEMINI_API_KEY` é seguro de rodar; colar o valor
  de volta no chat **não** é.
- Se uma chave vazar por engano: revogue na hora em https://aistudio.google.com/apikey
  antes de gerar outra.
- As etapas de **login** são sempre feitas num terminal Ubuntu/WSL "de verdade" —
  **nunca** na aba "Code" embutida do Cowork nem no runner `!` de uma sessão de IA
  (essas superfícies já rodaram em ambiente inconsistente: PowerShell em vez de WSL,
  shell não-interativo que não carrega `.bashrc`).

---

## 1. Autenticar o `agents-cli` (Gemini API Key)

1. **Abra um terminal Ubuntu/WSL real** — ícone do Ubuntu, ou `wsl` a partir do
   Windows Terminal.
2. **Confira se a variável já existe** (sem mostrar o valor):
   ```bash
   [ -n "$GEMINI_API_KEY" ] && echo "definida" || echo "vazia"
   ```
3. **Se estiver vazia ou a chave foi revogada**, edite o `~/.bashrc` direto
   (nunca cole a chave em chat de IA):
   ```bash
   sed -i '/GEMINI_API_KEY/d' ~/.bashrc
   echo 'export GEMINI_API_KEY="SUA_CHAVE_AQUI"' >> ~/.bashrc
   source ~/.bashrc
   ```
4. **Logue o `agents-cli` nesse mesmo terminal puro** (escolha a opção
   **Gemini API Key**):
   ```bash
   agents-cli login -i
   ```
   Confirme com:
   ```bash
   agents-cli login --status
   ```
5. **Só depois de ver "autenticado"**, abra/reabra o Claude Code — ele herda a
   autenticação automaticamente, sem nunca precisar ver a chave.

### Se aparecer `agents-cli: command not found` num terminal novo
Quase sempre é um terminal que não está carregando o `~/.bashrc` (ex.: a aba Code,
não um terminal nativo). Diagnóstico rápido:
```bash
cat ~/.profile | grep -A3 bashrc   # confirma o encadeamento .profile -> .bashrc
source ~/.bashrc                    # corrige a sessão atual na hora
which agents-cli                    # deve apontar para ~/.local/bin/agents-cli
```

---

## 2. Autenticar a ADC (gcloud) — necessária antes de qualquer deploy

A autenticação do `agents-cli`/Gemini API Key (seção 1) é **separada** da
autenticação do `gcloud`/ADC (Application Default Credentials). Comandos como
`agents-cli deploy` precisam das **duas**. Faltar a ADC dá um erro de import
(`google.auth.default()` sem credenciais), não um erro óbvio de "não logado".

1. **Antes de qualquer `agents-cli deploy`** (real ou `--dry-run` que importe o
   app), verifique a ADC num terminal puro:
   ```bash
   gcloud auth application-default print-access-token
   ```
   Deve imprimir um token longo (não um erro). **Não cole esse token em chat de IA** —
   é só confirmação visual.
2. **Se der erro** (sem credenciais), autentique manualmente, no mesmo terminal puro:
   ```bash
   gcloud auth application-default login
   gcloud config set project kaggle-dia5-agent-runtime
   ```
3. Só depois de confirmar o passo 1 com sucesso, volte para o Claude Code (ou abra
   uma sessão nova — ela herda a ADC automaticamente) e siga com o deploy.

---

## 3. Split WSL/Windows (por que o deploy não enxerga as credenciais)

`gcloud` está instalado **só no WSL**; `agents-cli` corre como **binário Windows**.
As credenciais ADC do WSL ficam em
`//wsl$/Ubuntu/home/ilanschapira/.config/gcloud/application_default_credentials.json`
e são **invisíveis** para o processo Windows por padrão.

Solução: antes de rodar `agents-cli deploy` a partir do Claude Code / Bash tool,
exporte:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="//wsl$/Ubuntu/home/ilanschapira/.config/gcloud/application_default_credentials.json"
export GOOGLE_CLOUD_PROJECT="kaggle-dia5-agent-runtime"
```
(O Claude Code já faz isso automaticamente — ver os deploys registrados no
`Diário_Aprendizado.md`.)

---

## Protocolo do Claude quando a verificação falha
Se um comando de **status** mostrar "não autenticado", o Claude deve **parar** e
pedir para você seguir o checklist acima num terminal externo — nunca tentar
"ajudar" sugerindo `agents-cli login -i`, `gcloud auth login` ou qualquer comando
que peça a chave/token na conversa.

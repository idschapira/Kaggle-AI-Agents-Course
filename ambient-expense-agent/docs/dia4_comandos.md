# Dia 4 — Comandos centralizados (ambient-expense-agent)

> Roda cada bloco na pasta `ambient-expense-agent/`, no PowerShell.

## 1. Confirmar toolchain
```powershell
agents-cli info
```

## 2. Instalar as 7 skills do ADK no escopo do PROJETO
Pacote oficial: `github.com/google/agents-cli` (skills: adk-code, deploy, eval,
observability, publish, scaffold, workflow). Sem `-g` instala em
`.agent/skills/` (versionável no Git), não na pasta global do usuário.
```powershell
npx skills add https://github.com/google/agents-cli -y --all
```

## 3. Confirmar instalação
```powershell
skills list
agents-cli info
```

## 4. Rodar o ADK Playground (Passo 6 do codelab)
```powershell
make playground
```

## 5. Gerar e avaliar traces (Passo 9 do codelab)
```powershell
make generate-traces
make grade
```

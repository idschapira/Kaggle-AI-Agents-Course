---
name: stride-threat-model
description: Use this skill when the user asks for a security threat model, STRIDE analysis, or risk assessment of an AI agent's code (entry points, tools, data flows). Produces a structured threat_model.md covering Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.
---

# STRIDE Threat Model Skill

## Objective
Analisar o grafo do agente (entry points, tools, fluxos de dados, estado) e produzir um relatório `threat_model.md` aplicando o framework STRIDE.

## Quando usar
Sempre que o usuário pedir uma análise de segurança, "threat model", ou "STRIDE" sobre um agente de IA neste repositório.

## Processo

1. **Mapear a superfície de ataque**: identificar entry points (ex: prompts do usuário, tool calls), dados sensíveis manipulados (ex: variáveis de ambiente, segredos, IDs de usuário), e estado persistente (ex: stores em memória).
2. **Aplicar as 6 categorias STRIDE** a cada componente relevante:
   - **Spoofing** (falsificação de identidade): o agente confia em algum identificador (ex: `user_id`) sem autenticação real?
   - **Tampering** (adulteração): dados ou código podem ser modificados sem autorização (ex: segredos hardcoded, estado mutável sem controle de concorrência)?
   - **Repudiation** (repúdio): existe log/auditoria das ações sensíveis (ex: redenção de um código de desconto)? Um usuário poderia negar ter feito a ação?
   - **Information Disclosure** (exposição de informação): segredos, chaves de API, ou dados internos podem ser expostos (ex: hardcoded keys, mensagens de erro verbosas)?
   - **Denial of Service** (negação de serviço): o agente ou suas tools podem ser sobrecarregados ou travados (ex: falta de rate limiting, loops, store sem limite de tamanho)?
   - **Elevation of Privilege** (elevação de privilégio): um usuário pode fazer o agente executar uma ação além do que deveria ser permitido (ex: prompt injection levando a tool calls não intencionados)?
3. **Para cada achado**: descrever o risco, o componente afetado, severidade (Alta/Média/Baixa) e uma recomendação de mitigação.
4. **Gerar `threat_model.md`** na raiz do projeto analisado, com uma seção por categoria STRIDE.

## Formato de saída esperado
```markdown
# Threat Model: <nome do agente>

## Visão Geral da Superfície de Ataque
...

## Spoofing
...

## Tampering
...

## Repudiation
...

## Information Disclosure
...

## Denial of Service
...

## Elevation of Privilege
...

## Resumo de Severidade
| Categoria | Achado | Severidade |
|---|---|---|
```

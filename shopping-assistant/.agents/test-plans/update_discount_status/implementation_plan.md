# Implementation Plan: `update_discount_status`

> Plano de demonstração gerado para testar o TDD Planning Gate (Seção 8).
> Nenhum código foi implementado — aguardando aprovação.

## Objetivo
Criar uma nova tool de agente que permite a administradores ativar ou desativar códigos de desconto na loja.

## Estágios

1. **Schema de entrada (Pydantic)**: `UpdateDiscountStatusInput` com `admin_id: str`, `discount_code: str`, `active: bool`.
2. **Verificação de papel (role)**: confirmar que `admin_id` corresponde de fato a uma conta com privilégio de administrador, em uma fonte de autorização própria — não apenas aceitar o argumento como verdadeiro.
3. **Validação do código**: confirmar que `discount_code` existe antes de tentar atualizar seu status.
4. **Atualização do status**: aplicar a mudança (`active`/`inactive`) e registrar em log de auditoria quem fez a alteração e quando.
5. **Testes**: admin válido ativando/desativando, tentativa de chamada por um `admin_id` que não é administrador, código inexistente.

## Security Boundaries & Assertions

- **Elevação de privilégio (o achado mais crítico aqui)**: a tool concede um poder administrativo (ativar/desativar descontos para todos os usuários). Assertion: `admin_id` nunca deve ser apenas um argumento de texto fornecido na conversa — deve ser resolvido contra uma fonte de identidade/autorização real (papel de admin verificado fora do alcance do LLM), igual ao padrão já recomendado para `user_id` no `redeem_discount` (Seção 7).
- **Prompt injection visando a tool administrativa**: como essa tool tem efeito amplo (afeta todos os usuários da loja), ela é o alvo mais valioso para um ataque de prompt injection. Assertion: a tool deve ser inacessível a sessões não-administrativas no nível da definição do agente, não apenas validada por dentro da função.
- **Ausência de log de auditoria**: toda mudança de status de um código de desconto deve ser logada (quem, quando, de "ativo" pra "inativo" ou vice-versa) — sem isso, não há como investigar um desconto desativado/ativado indevidamente (Repudiation).
- **Desativação em massa / abuso de disponibilidade**: considerar se há necessidade de limitar quantas alterações de status um mesmo `admin_id` pode fazer em um intervalo curto, para conter um cenário de credencial de admin comprometida sendo usada para desativar todos os descontos da loja de uma vez (Denial of Service direcionado ao negócio, não à infraestrutura).

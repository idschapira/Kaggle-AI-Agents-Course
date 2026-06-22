# Implementation Plan: `award_loyalty_points`

> Plano de demonstração gerado para testar o TDD Planning Gate (Seção 8).
> Nenhum código foi implementado — aguardando aprovação.

## Objetivo
Criar uma nova tool de agente que premia pontos de fidelidade a um usuário após uma compra bem-sucedida.

## Estágios

1. **Schema de entrada (Pydantic)**: definir `AwardLoyaltyPointsInput` com `user_id: str`, `purchase_id: str`, `points: int` (`points` deve ser validado como inteiro positivo, `gt=0`).
2. **Verificação de idempotência**: antes de creditar, checar se `purchase_id` já recebeu pontos antes (store de "compras já recompensadas"), para não premiar a mesma compra duas vezes.
3. **Aplicação do crédito**: somar `points` ao saldo do usuário em um único passo atômico (lock ou transação).
4. **Log de auditoria**: registrar `user_id`, `purchase_id`, `points`, timestamp — toda concessão de pontos deve ser rastreável.
5. **Testes**: caso de sucesso, caso de `purchase_id` repetido, caso de `points` inválido (negativo, zero, não-inteiro).

## Security Boundaries & Assertions

- **Valores negativos ou zero em `points`**: o schema Pydantic deve rejeitar `points <= 0` — sem essa validação, um prompt injection poderia tentar "premiar -1000 pontos" (efetivamente debitando o usuário) ou "premiar 0" sem efeito mas mascarando uma chamada maliciosa.
- **Reentrância / dupla concessão**: a mesma `purchase_id` não pode gerar pontos duas vezes (replay attack ou erro de retry do cliente). Assertion: antes de creditar, verificar e marcar a compra como "já recompensada" em uma única operação atômica.
- **`user_id` não validado contra a compra**: `purchase_id` deve pertencer de fato ao `user_id` informado — sem essa checagem, um usuário poderia reivindicar pontos de uma compra de outro usuário (elevação de privilégio horizontal).
- **Limite superior de pontos por chamada**: definir um teto razoável (ex: baseado no valor máximo de compra possível) para `points`, evitando que um valor absurdamente alto seja injetado e usado depois para resgates de alto valor.
- **Ausência de autenticação real do chamador**: assim como no `redeem_discount` (ver `threat_model.md`, Seção 7), `user_id` não deve ser um argumento livre decidido pelo LLM — deve vir de uma sessão autenticada fora do contexto da conversa.

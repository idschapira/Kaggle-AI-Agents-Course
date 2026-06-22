# Implementation Plan: `process_cart_checkout`

> Plano de demonstração gerado para testar o TDD Planning Gate (Seção 8).
> Nenhum código foi implementado — aguardando aprovação.

## Objetivo
Criar uma nova tool de agente que recebe um `cart_id` e um código de desconto, aplica o desconto e processa o pedido.

## Estágios

1. **Schema de entrada (Pydantic)**: `ProcessCartCheckoutInput` com `cart_id: str`, `discount_code: Optional[str]`, `user_id: str`.
2. **Carregamento do carrinho**: buscar o carrinho por `cart_id`, validar que pertence ao `user_id` informado e que ainda está em estado "aberto" (não finalizado, não expirado).
3. **Aplicação do desconto**: se `discount_code` for informado, validar (existe? já usado? ainda válido?) e recalcular o total — nunca confiar em um total já calculado vindo do cliente/LLM.
4. **Processamento atômico**: marcar o carrinho como "finalizado" e o código de desconto (se houver) como "usado" em uma única transação, para evitar reprocessamento.
5. **Testes**: checkout sem desconto, checkout com desconto válido, checkout com desconto inválido/expirado, tentativa de reprocessar o mesmo `cart_id` duas vezes.

## Security Boundaries & Assertions

- **Condição de corrida (double-checkout)**: duas chamadas simultâneas para o mesmo `cart_id` não podem ambas processar o pedido com sucesso — assertion: o "fechamento" do carrinho deve ser uma operação atômica (check-and-set), igual ao problema já identificado no `DISCOUNT_STORE` (Seção 7).
- **Total de pedido manipulado**: o preço final do pedido deve ser **recalculado no servidor** a partir dos itens reais do carrinho e da regra do desconto — nunca aceito como um número que o LLM "decidiu" passar como argumento.
- **`cart_id` de outro usuário (IDOR)**: a tool deve verificar que o `cart_id` pertence ao `user_id` autenticado antes de processar — caso contrário, um usuário poderia finalizar o carrinho de outra pessoa.
- **Reuso de `discount_code` em paralelo com a Seção 7**: aplica-se a mesma mitigação do `redeem_discount` — verificação e marcação do código como "usado" devem ser atômicas.
- **Carrinho vazio ou já finalizado**: a tool deve rejeitar explicitamente um checkout de carrinho vazio ou já processado, em vez de silenciosamente "ter sucesso" sem cobrar nada.

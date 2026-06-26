# 📓 Diário do Capstone — PokéPortfolio AI

> Diário **específico do projeto final** (capstone do curso "5-Day AI Agents").
> Registra decisões, progresso, dúvidas em aberto e lições do projeto.
> O diário geral do curso continua sendo o `Diário_Aprendizado.md`.
> Regras oficiais do hackathon: `Regras_Capstone.md`.

---

## 🎯 Visão do produto
**PokéPortfolio AI** — app web em que o usuário adiciona cartas Pokémon à coleção
por **texto livre** (em vez de busca manual ou scanner). Ex.: o usuário escreve
*"Adicionar 2 Charizard ex 151 NM, 1 Pikachu promo japonês LP e 1 Mewtwo GX PSA 9"*
e o agente: (1) interpreta o texto, (2) extrai entidades, (3) resolve ambiguidades,
(4) pede confirmação, (5) salva a coleção e atualiza o portfólio com valor total.

**Problema:** apps como Collectr e Pokécardex dependem de busca manual/filtros/
scanner — cadastro de lotes, cartas antigas ou texto bagunçado (ex.: print de
WhatsApp) gera fricção. Nosso diferencial é o **cadastro por linguagem natural**.

**Usuário-alvo:** colecionador casual (organizar sem esforço), intermediário
(acompanhar condição/idioma/quantidade) e usuário de binder/portfolio cansado do
cadastro manual.

---

## ✅ Decisões fechadas no brainstorming (Sessão 1 — 25/06/2026)

| Tema | Decisão |
| --- | --- |
| **Track** | **Concierge Agents** (assistente pessoal; mantém dados seguros) |
| **Escopo de usuário** | **Single-user** (só o próprio usuário; sem login no MVP) |
| **Input** | **Somente texto** no MVP (foto fica como visão de futuro) |
| **Campos da carta** | nome, set, quantidade, condição (NM/LP/MP…), idioma (PT/EN/JP), grading (PSA/CGC + nota) |
| **Fonte de dados** | **pokewallet.io** (forte candidata — preço ao vivo, REST+GraphQL) vs pokemontcg.io. Decisão final na arquitetura |
| **Persistência** | **Firestore** (plano gratuito Spark: 50k leituras / 20k escritas por dia — sobra muito) |
| **Submissão** | **Tudo em inglês** (Writeup ≤2.500 palavras + vídeo ≤5 min) |
| **Arquitetura de agente** | **Um agente** com ferramentas no MVP; multi-agente só se sobrar tempo |
| **UI** | Aproveitar o frontend React do antigo PokeAsset Manager (`apps/dia1_pokeasset_manager`) |

### Conceitos do curso que vamos demonstrar (mínimo é 3 — temos 5)
1. **Agent / ADK + Agents CLI** — o agente que interpreta e orquestra o fluxo.
2. **MCP Server** — a API de cartas/preço embrulhada como ferramenta (evita alucinação de preço).
3. **Security** — confirmação humana antes de salvar + chave de API só em variável de ambiente.
4. **Deployability** — deploy no Cloud Run (projeto GCP `kaggle-dia5-agent-runtime`).
5. **(Agents CLI já contado acima.)**
- **Antigravity** = único que fica de fora (opcional; é ferramenta de build mostrada no vídeo).

### Visão de futuro (mencionar na Writeup, NÃO construir no MVP)
- Preço em tempo real exibido continuamente no portfólio.
- Input por **foto** (Gemini multimodal).
- **Marketplace / rede social** para colecionadores.

---

## ❓ Dúvidas em aberto para a fase de ARQUITETURA
1. **Resolução de ambiguidade / UX da confirmação:** confirmar carta por carta ou
   o lote inteiro de uma vez? Como mostrar as opções quando há mais de um "match"?
2. **Identificar o "set":** "151" é um set; como o agente diferencia set, número da
   carta e nome quando o texto é curto/ambíguo?
3. **Preço: snapshot ou ao vivo?** Guardar o preço no momento do cadastro, ou sempre
   rebuscar na API ao abrir o portfólio? (afeta nº de requisições e a UX)
4. **Carta não encontrada:** o que o agente faz quando não acha a carta (sugerir
   parecidas? salvar como "não resolvida"?).
5. **Modelo e framework:** confirmar ADK + modelo Gemini; estrutura de pastas do agente.
6. **Fonte de dados final:** comparar docs da pokewallet.io vs pokemontcg.io (chave,
   limites, formato de resposta) e escolher.

---

## 🗓️ Próximos passos
- [ ] **Próxima sessão:** desenhar a arquitetura definitiva (componentes, fluxo de
      dados, contratos das ferramentas).
- [ ] Depois: montar o **backlog** e o **plano de execução** até a entrega.
- [ ] Confirmar o prazo na aba *Overview > Timeline* da competição (~06/07/2026 PT).

---

## 📌 Log de sessões
- **Sessão 1 (25/06/2026):** brainstorming completo. Visão do produto definida,
  track e escopo fechados, conceitos do curso mapeados (5 de 6). Criados
  `Regras_Capstone.md`, `AUTENTICACAO.md` e este diário; `CLAUDE.md` reorganizado.

import { Card } from "./types";

// Dynamic background color and illustration colors for Pokemon based on text names
export function getPokemonDesign(name: string, rarity: string): {
  gradient: string;
  borderColor: string;
  shadowColor: string;
  badgeBg: string;
  symbol: string;
  accentColor: string;
} {
  const normName = name.toLowerCase().trim();
  const normRarity = rarity.toLowerCase().trim();

  let accentColor = "amber-500";
  let gradient = "from-amber-400 to-orange-500";
  let borderColor = "border-amber-400";
  let shadowColor = "shadow-amber-500/20";
  let badgeBg = "bg-amber-500/10 text-amber-400";
  let symbol = "⚡"; // Electric by default

  if (normName.includes("pikachu") || normName.includes("raichu") || normName.includes("zapdos") || normName.includes("jolteon")) {
    gradient = "from-yellow-300 via-amber-400 to-yellow-500";
    borderColor = "border-yellow-400";
    shadowColor = "shadow-yellow-500/30";
    badgeBg = "bg-yellow-500/20 text-yellow-100";
    accentColor = "yellow-400";
    symbol = "⚡";
  } else if (normName.includes("charizard") || normName.includes("arcanine") || normName.includes("moltres") || normName.includes("flareon") || normName.includes("vulpix") || normName.includes("cyndaquil")) {
    gradient = "from-orange-500 via-red-500 to-rose-600";
    borderColor = "border-orange-500";
    shadowColor = "shadow-orange-500/30";
    badgeBg = "bg-orange-500/20 text-orange-200";
    accentColor = "orange-500";
    symbol = "🔥";
  } else if (normName.includes("blastoise") || normName.includes("gyarados") || normName.includes("vaporeon") || normName.includes("lapras") || normName.includes("suicune") || normName.includes("squirtle")) {
    gradient = "from-blue-400 via-blue-600 to-indigo-700";
    borderColor = "border-blue-500";
    shadowColor = "shadow-blue-500/30";
    badgeBg = "bg-blue-500/20 text-blue-200";
    accentColor = "blue-500";
    symbol = "💧";
  } else if (normName.includes("venusaur") || normName.includes("bulbasaur") || normName.includes("celebi") || normName.includes("meganium") || normName.includes("sceptile")) {
    gradient = "from-emerald-400 via-teal-500 to-green-600";
    borderColor = "border-emerald-500";
    shadowColor = "shadow-emerald-500/30";
    badgeBg = "bg-emerald-500/20 text-emerald-200";
    accentColor = "emerald-500";
    symbol = "🌿";
  } else if (normName.includes("mewtwo") || normName.includes("mew") || normName.includes("alakazam") || normName.includes("lugia") || normName.includes("espeon")) {
    gradient = "from-purple-400 via-violet-600 to-fuchsia-700";
    borderColor = "border-purple-500";
    shadowColor = "shadow-purple-500/30";
    badgeBg = "bg-purple-500/20 text-purple-200";
    accentColor = "purple-500";
    symbol = "👁️";
  } else if (normName.includes("gengar") || normName.includes("umbreon") || normName.includes("darkrai")) {
    gradient = "from-slate-700 via-indigo-950 to-purple-950";
    borderColor = "border-indigo-800";
    shadowColor = "shadow-indigo-950/40";
    badgeBg = "bg-indigo-900/40 text-indigo-200";
    accentColor = "indigo-800";
    symbol = "💀";
  } else if (normName.includes("lugia") || normName.includes("pidgeot") || normName.includes("rayquaza")) {
    gradient = "from-teal-300 via-cyan-500 to-sky-600";
    borderColor = "border-cyan-400";
    shadowColor = "shadow-cyan-500/20";
    badgeBg = "bg-cyan-500/20 text-cyan-100";
    accentColor = "cyan-400";
    symbol = "🌀";
  } else {
    // Default Normal/Dragon/Especial type
    gradient = "from-stone-400 via-zinc-500 to-stone-600";
    borderColor = "border-stone-400";
    shadowColor = "shadow-stone-500/25";
    badgeBg = "bg-stone-500/20 text-stone-200";
    accentColor = "stone-500";
    symbol = "⭐";
  }

  // Handle Rarity Enhancements: Holo / Secret Rare cards have shiny, gold borders and reflections!
  if (normRarity.includes("holo") || normRarity.includes("secret") || normRarity.includes("ultra") || normRarity.includes("promo")) {
    borderColor = "border-amber-300 border-2 shadow-[0_0_15px_rgba(251,191,36,0.4)]";
    shadowColor = "shadow-amber-400/40";
  }

  return { gradient, borderColor, shadowColor, badgeBg, symbol, accentColor };
}

// Initial default pokemon card portfolio
export const INITIAL_PORTFOLIO: Card[] = [
  {
    id: 1,
    nome_carta: "Pikachu Shadowless",
    set: "Base Set",
    raridade: "Holo Rare",
    estado_conservacao: "PSA 10",
    preco_compra: 100.0,
    preco_atual: 150.0,
    valorizacao_absoluta: 50.0,
    valorizacao_percentual: "50.00%",
    status: "lucro",
  },
  {
    id: 2,
    nome_carta: "Charizard",
    set: "Base Set",
    raridade: "Holo",
    estado_conservacao: "PSA 9",
    preco_compra: 500.0,
    preco_atual: 450.0,
    valorizacao_absoluta: -50.0,
    valorizacao_percentual: "-10.00%",
    status: "prejuizo",
  },
  {
    id: 3,
    nome_carta: "Mewtwo",
    set: "Fossil",
    raridade: "Ultra Rare",
    estado_conservacao: "PSA 10",
    preco_compra: 200.0,
    preco_atual: 200.0,
    valorizacao_absoluta: 0.0,
    valorizacao_percentual: "0.00%",
    status: "neutro",
  },
];

// Helper to calculate card metrics
export function calculateCardMetrics(precoCompra: number, precoAtual: number) {
  const valorizacao_absoluta = precoAtual - precoCompra;
  // Handle division by zero
  const pct = precoCompra > 0 ? (valorizacao_absoluta / precoCompra) * 100 : 0;
  const valorizacao_percentual = pct.toFixed(2) + "%";

  let status: "lucro" | "prejuizo" | "neutro" = "neutro";
  if (valorizacao_absoluta > 0) status = "lucro";
  else if (valorizacao_absoluta < 0) status = "prejuizo";

  return {
    valorizacao_absoluta,
    valorizacao_percentual,
    status,
  };
}

// Flexible command parser for PokéAsset Manager
export function parseAndExecuteCommand(
  commandText: string,
  currentPortfolio: Card[]
): {
  updatedPortfolio: Card[];
  successMessage: string;
  actionType: "adicionar" | "editar" | "excluir" | "unknown";
  targetCard?: Card;
} {
  const text = commandText.trim();
  const lowerText = text.toLowerCase();

  // 1. ADICIONAR CARD
  if (lowerText.startsWith("adicionar") || lowerText.startsWith("add")) {
    // Robust extraction: find label tags across the string
    // Standard signature: "Adicionar Pikachu, set Base, raridade Holo, estado PSA 10, compra 100, atual 150"
    
    // Help parse name first: Strip "Adicionar" or "Add"
    let rest = text.substring(lowerText.startsWith("adicionar") ? 9 : 3).trim();
    
    // Check if comma-spaced extraction or keyword-spaced extraction works better
    let nome_carta = "";
    let setVal = "Desconhecido";
    let raridadeVal = "Comum";
    let estadoVal = "Near Mint";
    let compraVal = 0;
    let atualVal = 0;

    if (rest.includes(",")) {
      const parts = rest.split(",").map(p => p.trim());
      // First part is usually the name, maybe stripped of leading punctuation
      nome_carta = parts[0].replace(/^["'\s]+|["'\s]+$/g, "");
      
      // Parse other parts looking for keys/values
      for (let i = 1; i < parts.length; i++) {
        const pStr = parts[i];
        const pLower = pStr.toLowerCase();
        
        if (pLower.startsWith("set ")) {
          setVal = pStr.substring(4).trim();
        } else if (pLower.startsWith("raridade ")) {
          raridadeVal = pStr.substring(9).trim();
        } else if (pLower.startsWith("estado ")) {
          estadoVal = pStr.substring(7).trim();
        } else if (pLower.startsWith("compra ")) {
          const numStr = pStr.substring(7).replace(/[^\d.]/g, "");
          compraVal = parseFloat(numStr) || 0;
        } else if (pLower.startsWith("atual ")) {
          const numStr = pStr.substring(6).replace(/[^\d.]/g, "");
          atualVal = parseFloat(numStr) || 0;
        } else {
          // Try loose matching
          const colonIdx = pStr.indexOf(":");
          if (colonIdx > 0) {
            const key = pStr.substring(0, colonIdx).trim().toLowerCase();
            const val = pStr.substring(colonIdx + 1).trim();
            if (key === "set") setVal = val;
            else if (key === "raridade" || key === "rarity") raridadeVal = val;
            else if (key === "estado" || key === "conservacao" || key === "estado_conservacao") estadoVal = val;
            else if (key === "compra" || key === "preco_compra") compraVal = parseFloat(val.replace(/[^\d.]/g, "")) || 0;
            else if (key === "atual" || key === "preco_atual") atualVal = parseFloat(val.replace(/[^\d.]/g, "")) || 0;
          }
        }
      }
    } else {
      // Keyword split index approach if no commas are found
      // "Adicionar Venusaur set Base raridade Holo estado PSA 10 compra 100 atual 120"
      const keywords = ["set", "raridade", "estado", "compra", "atual"];
      const indices: { key: string; index: number }[] = [];
      
      keywords.forEach(kw => {
        const idx = lowerText.indexOf(" " + kw + " ");
        if (idx !== -1) {
          indices.push({ key: kw, index: idx + 1 });
        }
      });
      
      // Sort indices
      indices.sort((a, b) => a.index - b.index);
      
      if (indices.length > 0) {
        // Name is from start of rest to first keyword index relative to rest
        const firstKwRelative = indices[0].index - (lowerText.startsWith("adicionar") ? 10 : 4);
        if (firstKwRelative > 0) {
          nome_carta = rest.substring(0, firstKwRelative).trim();
        } else {
          nome_carta = "Carta";
        }
        
        for (let i = 0; i < indices.length; i++) {
          const curr = indices[i];
          const start = curr.index + curr.key.length;
          const end = i < indices.length - 1 ? indices[i+1].index : text.length;
          const extractedValue = text.substring(start, end).trim().replace(/^,+|,+$/g, "").trim();
          
          if (curr.key === "set") setVal = extractedValue;
          else if (curr.key === "raridade") raridadeVal = extractedValue;
          else if (curr.key === "estado") estadoVal = extractedValue;
          else if (curr.key === "compra") compraVal = parseFloat(extractedValue.replace(/[^\d.]/g, "")) || 0;
          else if (curr.key === "atual") atualVal = parseFloat(extractedValue.replace(/[^\d.]/g, "")) || 0;
        }
      } else {
        // Fallback: just name of card
        nome_carta = rest;
      }
    }

    if (!nome_carta) {
      nome_carta = "Nova Carta Pokémon";
    }

    // Sequence ID
    const nextId = currentPortfolio.reduce((max, card) => card.id > max ? card.id : max, 0) + 1;
    const metrics = calculateCardMetrics(compraVal, atualVal);

    const newCard: Card = {
      id: nextId,
      nome_carta,
      set: setVal,
      raridade: raridadeVal,
      estado_conservacao: estadoVal,
      preco_compra: compraVal,
      preco_atual: atualVal,
      ...metrics,
    };

    const updatedPortfolio = [...currentPortfolio, newCard];
    return {
      updatedPortfolio,
      successMessage: `Carta "${nome_carta}" (ID: ${nextId}) adicionada com sucesso!`,
      actionType: "adicionar",
      targetCard: newCard,
    };
  }

  // 2. EDITAR CARD
  if (lowerText.startsWith("editar") || lowerText.startsWith("update") || lowerText.startsWith("alterar")) {
    // Pattern: "Editar id 1, novo preco_atual 160" or "Editar id 1, preco_atual 160" or "Editar id: 1, set Base 2"
    
    // Extract ID
    const idMatch = lowerText.match(/(?:id\s*:?\s*|id\s+|editar\s+id\s+)(\d+)/i);
    if (!idMatch) {
      throw new Error("Erro: ID da carta não especificado para edição. Use o formato: Editar id [numero] ...");
    }
    
    const cardId = parseInt(idMatch[1]);
    const cardIndex = currentPortfolio.findIndex(c => c.id === cardId);
    if (cardIndex === -1) {
      throw new Error(`Erro: Nenhuma carta encontrada com o ID ${cardId}.`);
    }

    const cardToEdit = { ...currentPortfolio[cardIndex] };
    
    // Parse key-value alterations
    // E.g., "novo preco_atual 160" or "set Base Set 2" or "atual: 180"
    // Let's sweep the command text for field patterns
    let updated = false;

    // Remove the command and ID part to look at modifications
    const modString = text.replace(/^(editar|update|alterar)\s+id\s*:?\s*\d+/i, "").trim();
    
    // Split modifiers by comma or analyze the main fields
    // We can support editing multiple fields separated by commas
    const modifiers = modString.split(",").map(m => m.trim());
    
    for (const mod of modifiers) {
      const lowerMod = mod.toLowerCase();
      
      // Look for preco_atual
      if (lowerMod.includes("preco_atual") || lowerMod.includes("atual") || lowerMod.includes("preco atual")) {
        const valStr = lowerMod.replace(/(?:novo\s+)?(?:preco_atual|preco\s+atual|atual)(?:\s*:?\s*)?/i, "").replace(/[^\d.]/g, "");
        const actualVal = parseFloat(valStr);
        if (!isNaN(actualVal)) {
          cardToEdit.preco_atual = actualVal;
          updated = true;
        }
      }
      // Look for preco_compra
      else if (lowerMod.includes("preco_compra") || lowerMod.includes("compra") || lowerMod.includes("preco compra")) {
        const valStr = lowerMod.replace(/(?:novo\s+)?(?:preco_compra|preco\s+compra|compra)(?:\s*:?\s*)?/i, "").replace(/[^\d.]/g, "");
        const compraVal = parseFloat(valStr);
        if (!isNaN(compraVal)) {
          cardToEdit.preco_compra = compraVal;
          updated = true;
        }
      }
      // Look for set
      else if (lowerMod.includes("set ")) {
        const val = mod.replace(/^(?:novo\s+)?set\s*:?/i, "").trim();
        if (val) {
          cardToEdit.set = val;
          updated = true;
        }
      }
      // Look for raridade
      else if (lowerMod.includes("raridade") || lowerMod.includes("rarity")) {
        const val = mod.replace(/^(?:nova\s+|novo\s+)?(?:raridade|rarity)\s*:?/i, "").trim();
        if (val) {
          cardToEdit.raridade = val;
          updated = true;
        }
      }
      // Look for estado_conservacao
      else if (lowerMod.includes("estado") || lowerMod.includes("conservacao")) {
        const val = mod.replace(/^(?:novo\s+)?(?:estado_conservacao|estado|conservacao)\s*:?/i, "").trim();
        if (val) {
          cardToEdit.estado_conservacao = val;
          updated = true;
        }
      }
      // Look for nome_carta
      else if (lowerMod.includes("nome_carta") || lowerMod.includes("nome")) {
        const val = mod.replace(/^(?:novo\s+)?(?:nome_carta|nome)\s*:?/i, "").trim();
        if (val) {
          cardToEdit.nome_carta = val;
          updated = true;
        }
      }
    }

    if (!updated) {
      // If we couldn't parse structured descriptors, let's try a last resort regex
      // E.g., "Editar id 1, 160" (assumes setting current price)
      const numberMatches = modString.match(/(\d+(?:\.\d+)?)/g);
      if (numberMatches && numberMatches.length > 0) {
        cardToEdit.preco_atual = parseFloat(numberMatches[0]);
        updated = true;
      } else {
        throw new Error("Erro: Nenhum campo de edição reconhecido. Exemplos: 'Editar id 1, novo preco_atual 200' ou 'Editar id 1, set Jungle'.");
      }
    }

    // Recalculate metrics
    const metrics = calculateCardMetrics(cardToEdit.preco_compra, cardToEdit.preco_atual);
    const finalizedCard = {
      ...cardToEdit,
      ...metrics,
    };

    const updatedPortfolio = [...currentPortfolio];
    updatedPortfolio[cardIndex] = finalizedCard;

    return {
      updatedPortfolio,
      successMessage: `Carta "${finalizedCard.nome_carta}" (ID: ${cardId}) editada com sucesso!`,
      actionType: "editar",
      targetCard: finalizedCard,
    };
  }

  // 3. EXCLUIR CARD
  if (lowerText.startsWith("excluir") || lowerText.startsWith("deletar") || lowerText.startsWith("remover") || lowerText.startsWith("delete")) {
    const idMatch = lowerText.match(/(?:id\s*:?\s*|id\s+|excluir\s+id\s+|deletar\s+|remover\s+)(\d+)/i);
    if (!idMatch) {
      throw new Error("Erro: ID da carta não especificado para exclusão. Use o formato: Excluir id [numero]");
    }

    const cardId = parseInt(idMatch[1]);
    const cardIndex = currentPortfolio.findIndex(c => c.id === cardId);
    if (cardIndex === -1) {
      throw new Error(`Erro: Nenhuma carta encontrada com o ID ${cardId}.`);
    }

    const removedCard = currentPortfolio[cardIndex];
    const updatedPortfolio = currentPortfolio.filter(c => c.id !== cardId);

    return {
      updatedPortfolio,
      successMessage: `Carta "${removedCard.nome_carta}" (ID: ${cardId}) excluída com sucesso!`,
      actionType: "excluir",
      targetCard: removedCard,
    };
  }

  // 4. Fallback search / unknown
  return {
    updatedPortfolio: currentPortfolio,
    successMessage: "Comando não reconhecido. Use: Adicionar, Editar ou Excluir com a sintaxe correta.",
    actionType: "unknown",
  };
}

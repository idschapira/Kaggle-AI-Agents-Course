import { Card, SearchState } from "../types";
import { getPokemonDesign } from "../utils";
import { Edit2, Trash2, Shield, Info, Sparkles } from "lucide-react";

interface CardGridProps {
  portfolio: Card[];
  searchState: SearchState;
  onEditClick: (card: Card) => void;
  onDeleteClick: (cardId: number) => void;
}

export default function CardGrid({ portfolio, searchState, onEditClick, onDeleteClick }: CardGridProps) {
  // Filter search terms
  const filteredPortfolio = portfolio.filter(card => {
    const term = searchState.searchTerm.toLowerCase();
    const nameMatch = card.nome_carta.toLowerCase().includes(term);
    const setMatch = card.set.toLowerCase().includes(term);
    const rMatch = card.raridade.toLowerCase().includes(term);
    
    const termMatch = nameMatch || setMatch || rMatch;

    const statusMatch = searchState.statusFilter === "todos" || card.status === searchState.statusFilter;
    const raritySpecificMatch = !searchState.rarityFilter || card.raridade.toLowerCase().includes(searchState.rarityFilter.toLowerCase());

    return termMatch && statusMatch && raritySpecificMatch;
  });

  if (filteredPortfolio.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 px-4 border-2 border-dashed border-slate-300 rounded-none bg-white">
        <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 mb-3 text-lg border border-slate-200">🔍</div>
        <p className="text-slate-800 font-bold text-center uppercase tracking-wider text-xs">Nenhuma carta encontrada</p>
        <p className="text-slate-400 text-[11px] text-center mt-1">Experimente mudar seus filtros ou adicionar novos ativos pelo console.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {filteredPortfolio.map(card => {
        const design = getPokemonDesign(card.nome_carta, card.raridade);
        const isAppreciated = card.status === "lucro";
        const isDepreciated = card.status === "prejuizo";

        return (
          <div
            key={card.id}
            id={`card-${card.id}`}
            className="group relative bg-white border-2 border-slate-900 rounded-none shadow-sm hover:shadow-[6px_6px_0px_rgba(15,23,42,1)] hover:-translate-x-1 hover:-translate-y-1 transition-all duration-200 p-4 flex flex-col justify-between"
          >
            {/* Top Bar (ID & Rarity Badge) */}
            <div className="flex items-center justify-between mb-3 relative z-10">
              <span className="font-mono text-xs font-bold text-slate-400">#{String(card.id).padStart(3, '0')}</span>
              <div className="flex gap-1.5 items-center">
                <span className="text-[9px] px-2 py-0.5 border-2 border-slate-900 rounded-none font-bold tracking-wider flex items-center gap-1 uppercase bg-slate-50 text-slate-800">
                  <span>{design.symbol}</span>
                  {card.raridade}
                </span>
                
                {/* Holographic sparkle indicator */}
                {(card.raridade.toLowerCase().includes("holo") || card.raridade.toLowerCase().includes("secret") || card.raridade.toLowerCase().includes("ultra")) && (
                  <span className="text-amber-550 shrink-0" title="Shiny Card">
                    <Sparkles className="h-3.5 w-3.5 fill-amber-400" />
                  </span>
                )}
              </div>
            </div>

            {/* Pokémon Card Artwork Box */}
            <div className={`h-36 rounded-none bg-linear-to-br ${design.gradient} relative overflow-hidden flex items-center justify-center p-4 border-2 border-slate-900`}>
              {/* Pattern inside box */}
              <div className="absolute inset-0 opacity-15 mix-blend-overlay bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white via-stone-400 to-black select-none pointer-events-none" />
              
              {/* Energy watermark */}
              <div className="text-white/20 select-none text-[8rem] font-bold font-sans flex items-center justify-center scale-75">
                {design.symbol}
              </div>
            </div>

            {/* Card Information */}
            <div className="mt-4 flex-1 flex flex-col justify-between relative z-10">
              <div>
                <h3 className="text-sm font-black text-slate-900 tracking-tight line-clamp-1 uppercase group-hover:text-red-650 transition-colors">
                  {card.nome_carta}
                </h3>
                
                <div className="mt-2 grid grid-cols-2 gap-2 text-[11px] text-slate-500 font-bold uppercase">
                  <div className="flex items-center">
                    <span className="text-slate-400 mr-1 font-sans font-medium">Set:</span>
                    <span className="text-slate-800 truncate">{card.set}</span>
                  </div>
                  <div className="flex items-center justify-end">
                    <span className="text-slate-400 mr-1 font-sans font-medium">Grade:</span>
                    <span className="text-slate-800 font-mono font-black border border-slate-300 px-1 bg-slate-50">{card.estado_conservacao}</span>
                  </div>
                </div>
              </div>

              {/* Financial calculations info */}
              <div className="mt-4 pt-3 border-t-2 border-slate-100">
                <div className="grid grid-cols-2 gap-3 mb-2">
                  <div>
                    <span className="block text-[9px] text-slate-400 uppercase font-black tracking-wider">Custo de Compra</span>
                    <span className="text-xs font-bold text-slate-600 font-mono">
                      R$ {card.preco_compra.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="block text-[9px] text-slate-400 uppercase font-black tracking-wider">Preço Atual</span>
                    <span className="text-xs font-black text-slate-900 font-mono">
                      R$ {card.preco_atual.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                  </div>
                </div>

                {/* Return rates */}
                <div className="flex items-center justify-between p-2 rounded-none bg-slate-50 border border-slate-200">
                  <span className="text-[9px] text-slate-400 uppercase font-bold tracking-wider">Performance</span>
                  <div className="flex items-center gap-1.5">
                    <span className={`text-[11px] font-mono font-bold ${
                      isAppreciated ? "text-emerald-600" : isDepreciated ? "text-rose-650" : "text-slate-500"
                    }`}>
                      {isAppreciated ? "+" : ""}
                      R$ {card.valorizacao_absoluta.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                    <span className={`text-[9px] px-1.5 py-0.2 font-mono font-black uppercase underline decoration-2 underline-offset-4 ${
                      isAppreciated 
                        ? "text-emerald-600 font-bold" 
                        : isDepreciated 
                        ? "text-rose-600 font-bold" 
                        : "text-slate-500"
                    }`}>
                      {card.valorizacao_percentual}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Card Edit and Delete overlays/controls */}
            <div className="mt-4 flex gap-2 relative z-10 border-t border-slate-100 pt-3">
              <button
                type="button"
                onClick={() => onEditClick(card)}
                className="flex-1 flex items-center justify-center gap-1 text-[10px] font-bold uppercase tracking-wider text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-300 rounded-none py-2 transition"
                title="Editar Carta"
              >
                <Edit2 className="h-3 w-3" />
                <span>Editar</span>
              </button>
              <button
                type="button"
                onClick={() => onDeleteClick(card.id)}
                className="flex items-center justify-center bg-slate-100 hover:bg-red-50 text-slate-500 hover:text-red-650 border border-slate-300 rounded-none py-2 px-3 transition"
                title="Excluir Carta do Portfólio"
              >
                <Trash2 className="h-3 w-3" />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

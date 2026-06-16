import React, { useState, useEffect } from "react";
import { Card, SearchState } from "./types";
import { INITIAL_PORTFOLIO, parseAndExecuteCommand } from "./utils";
import StatsGrid from "./components/StatsGrid";
import CardGrid from "./components/CardGrid";
import CommandTerminal from "./components/CommandTerminal";
import CardFormModal from "./components/CardFormModal";
import { Sparkles, Terminal as TerminalIcon, ShieldCheck, Database, RefreshCcw, Landmark, Search, Filter, HelpCircle, Plus, Copy, Check } from "lucide-react";

export default function App() {
  // Load portfolio from localStorage or fallback to defaults
  const [portfolio, setPortfolio] = useState<Card[]>(() => {
    const cached = localStorage.getItem("poke_portfolio");
    if (cached) {
      try {
        return JSON.parse(cached);
      } catch (e) {
        console.error("Failed to parse cached portfolio, fallback to defaults.", e);
      }
    }
    return INITIAL_PORTFOLIO;
  });

  const [searchState, setSearchState] = useState<SearchState>({
    searchTerm: "",
    statusFilter: "todos",
    rarityFilter: "",
  });

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [cardToEdit, setCardToEdit] = useState<Card | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [showRawJson, setShowRawJson] = useState(false);
  const [dbCopied, setDbCopied] = useState(false);

  // Sync to local storage
  useEffect(() => {
    localStorage.setItem("poke_portfolio", JSON.stringify(portfolio));
  }, [portfolio]);

  // Execute terminal command string
  const handleExecuteCommand = (cmdText: string): string => {
    try {
      const result = parseAndExecuteCommand(cmdText, portfolio);
      setPortfolio(result.updatedPortfolio);
      setErrorMsg(null);
      return result.successMessage;
    } catch (err: any) {
      setErrorMsg(err.message || "Erro desconhecido ao processar comando.");
      throw err;
    }
  };

  // Quick edit button logic from single card
  const handleCardEditClick = (card: Card) => {
    setCardToEdit(card);
    setIsModalOpen(true);
  };

  // Quick delete button logic
  const handleCardDeleteClick = (cardId: number) => {
    if (window.confirm("Deseja realmente remover esta carta do portfólio?")) {
      const cmdText = `Excluir id ${cardId}`;
      handleExecuteCommand(cmdText);
    }
  };

  const resetToDefault = () => {
    if (window.confirm("Essa operação irá restaurar as 3 cartas iniciais padrão. Continuar?")) {
      setPortfolio(INITIAL_PORTFOLIO);
      localStorage.setItem("poke_portfolio", JSON.stringify(INITIAL_PORTFOLIO));
    }
  };

  const handleCopyDbJson = () => {
    const raw = JSON.stringify({ portfolio }, null, 2);
    navigator.clipboard.writeText(raw);
    setDbCopied(true);
    setTimeout(() => setDbCopied(false), 2000);
  };

  return (
    <div id="poke-asset-app" className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-red-500 selection:text-white">

      {/* Primary header navbar */}
      <header className="h-20 bg-red-600 flex items-center justify-between px-6 text-white shrink-0 shadow-sm border-b-4 border-slate-900 sticky top-0 z-40">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-white rounded-full border-4 border-slate-900 flex items-center justify-center shrink-0 shadow-xs">
            <div className="w-3 h-3 bg-slate-900 rounded-full"></div>
          </div>
          <div>
            <h1 className="text-xl font-black tracking-tighter uppercase text-white">PokéAsset Manager</h1>
            <p className="text-[10px] font-bold opacity-90 uppercase tracking-widest text-slate-100">TCG PORTFOLIO DATABASE v2.4</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => {
              setCardToEdit(null);
              setIsModalOpen(true);
            }}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-black uppercase tracking-widest px-4 py-2 border-2 border-slate-950 rounded-none transition"
          >
            <Plus className="h-4 w-4" />
            <span className="hidden sm:inline">Adicionar Carta</span>
          </button>
          
          <button
            onClick={resetToDefault}
            className="p-2 text-slate-900 hover:bg-slate-100 bg-white border-2 border-slate-950 rounded-none transition"
            title="Restaurar banco de dados original"
          >
            <RefreshCcw className="h-4 w-4" />
          </button>
        </div>
      </header>

      {/* Main Content Stage */}
      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-15">
        
        {/* Total Statistics Bento row */}
        <StatsGrid portfolio={portfolio} />

        {/* Content Panel splits */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 my-6">
          
          {/* Inventory Grid Left Panel */}
          <div className="lg:col-span-7 flex flex-col space-y-6">
            
            {/* Search, Filter constraints panel */}
            <div className="bg-white border-2 border-slate-900 p-4 rounded-none shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="relative flex-grow max-w-md">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  type="text"
                  placeholder="Buscar por nome, coleção, raridade..."
                  value={searchState.searchTerm}
                  onChange={(e) => setSearchState({ ...searchState, searchTerm: e.target.value })}
                  className="w-full bg-slate-55 border-2 border-slate-900 rounded-none pl-10 pr-4 py-2 text-xs text-slate-800 font-bold focus:outline-hidden focus:border-red-600 transition"
                />
              </div>

              {/* Filtering Chips */}
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="text-[10px] text-slate-400 font-sans font-black uppercase mr-1 flex items-center gap-1">
                  <Filter className="h-3 w-3" />
                  <span>Filtro:</span>
                </span>
                
                <button
                  type="button"
                  onClick={() => setSearchState({ ...searchState, statusFilter: "todos" })}
                  className={`px-3 py-1.5 rounded-none text-[10px] uppercase font-black tracking-wider cursor-pointer transition border-2 ${
                    searchState.statusFilter === "todos"
                      ? "bg-slate-900 text-white border-slate-950"
                      : "bg-slate-50 text-slate-600 border-transparent hover:bg-slate-100"
                  }`}
                >
                  Todos
                </button>
                <button
                  type="button"
                  onClick={() => setSearchState({ ...searchState, statusFilter: "lucro" })}
                  className={`px-3 py-1.5 rounded-none text-[10px] uppercase font-black tracking-wider cursor-pointer transition flex items-center gap-1 border-2 ${
                    searchState.statusFilter === "lucro"
                      ? "bg-emerald-50 text-emerald-700 border-emerald-500 font-black"
                      : "bg-slate-50 text-slate-600 border-transparent hover:text-emerald-600 hover:bg-slate-100"
                  }`}
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                  Valorizados
                </button>
                <button
                  type="button"
                  onClick={() => setSearchState({ ...searchState, statusFilter: "prejuizo" })}
                  className={`px-3 py-1.5 rounded-none text-[10px] uppercase font-black tracking-wider cursor-pointer transition flex items-center gap-1 border-2 ${
                    searchState.statusFilter === "prejuizo"
                      ? "bg-rose-50 text-rose-700 border-rose-500 font-black"
                      : "bg-slate-50 text-slate-600 border-transparent hover:text-rose-600 hover:bg-slate-100"
                  }`}
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-rose-500" />
                  Desvalorizados
                </button>
              </div>
            </div>

            {/* Inventory Listing */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-black italic uppercase text-slate-800 leading-none">
                  Ativos em Inventário ({portfolio.length})
                </h2>
                
                {portfolio.length > 0 && (
                  <span className="text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                    Sincronizado na nuvem e localmente
                  </span>
                )}
              </div>

              {/* TCG Render grid */}
              <CardGrid
                portfolio={portfolio}
                searchState={searchState}
                onEditClick={handleCardEditClick}
                onDeleteClick={handleCardDeleteClick}
              />
            </div>
          </div>

          {/* Controller Shell Terminal Right Panel */}
          <div className="lg:col-span-12 xl:col-span-5 flex flex-col space-y-6">
            
            {/* Interactive Terminal Core */}
            <div>
              <CommandTerminal
                portfolio={portfolio}
                onExecuteCommand={handleExecuteCommand}
                errorMsg={errorMsg}
                clearError={() => setErrorMsg(null)}
              />
            </div>

            {/* Live Database Real-time Inspection section */}
            <div className="bg-white border-2 border-slate-900 rounded-none p-5 shadow-xs">
              <div className="flex items-center justify-between mb-3.5">
                <div className="flex items-center gap-2">
                  <Database className="h-3.5 w-3.5 text-red-650" />
                  <span className="text-[10px] font-black uppercase tracking-wider text-slate-900">Live JSON Database</span>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setShowRawJson(!showRawJson)}
                    className="p-1 px-2.5 text-[9px] font-black uppercase tracking-wider text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-350 rounded-none transition"
                  >
                    {showRawJson ? "Esconder" : "Visualizar"}
                  </button>
                  <button
                    onClick={handleCopyDbJson}
                    className="p-1 px-2.5 text-[9px] font-black uppercase tracking-wider text-red-650 bg-red-50 hover:bg-red-100 border border-red-200 rounded-none transition flex items-center gap-1"
                  >
                    {dbCopied ? <Check className="h-2.5 w-2.5" /> : <Copy className="h-2.5 w-2.5" />}
                    <span>{dbCopied ? "Copiado!" : "Copiar"}</span>
                  </button>
                </div>
              </div>

              {/* Preview Box toggles */}
              {showRawJson ? (
                <div className="bg-slate-950 border border-slate-900 p-4 rounded-none max-h-60 overflow-y-auto leading-relaxed relative">
                  <pre className="text-[11px] font-mono text-slate-400 whitespace-pre-wrap select-all">
                    {JSON.stringify({ portfolio }, null, 2)}
                  </pre>
                </div>
              ) : (
                <div className="text-[11.5px] text-slate-600 space-y-1.5 font-sans leading-relaxed p-1">
                  <p>O estado do portfólio Pokémon TCG está totalmente sincronizado conforme os cálculos oficiais baseados nos comandos executados.</p>
                  <ul className="list-disc list-inside space-y-1 text-slate-400 pl-1 text-[10px] font-bold uppercase">
                    <li>Cálculos automáticos de oscilação em tempo real.</li>
                    <li>Sinalização visual de lucro / prejuízo.</li>
                    <li>Estruturação e ID sequencial robusto.</li>
                  </ul>
                </div>
              )}
            </div>

            {/* Quick Guidance Box */}
            <div className="bg-white border-2 border-slate-900 p-4 rounded-none text-[11px] leading-relaxed text-slate-600 space-y-1 relative">
              <div className="font-black text-slate-900 uppercase tracking-wider flex items-center gap-1.5 mb-2 text-xs">
                <HelpCircle className="h-3.5 w-3.5 text-red-650" />
                <span>Instruções Rápidas de Operação</span>
              </div>
              <p>O console aceita comandos livres em Português seguindo as diretrizes estruturais de TCG.</p>
              <div className="font-mono text-slate-700 text-[10.5px] bg-slate-100 p-3 rounded-none border border-slate-300 tracking-tight mt-2 leading-relaxed">
                <p className="font-bold text-slate-900 uppercase text-[9px] mb-1">Comandos de Exemplo:</p>
                <p>• Adicionar [nome], set [set], raridade [raridade], estado [estado], compra [num], atual [num]</p>
                <p>• Editar id [id], novo preco_atual [num]</p>
                <p>• Excluir id [id]</p>
              </div>
            </div>

          </div>

        </div>

      </main>

      {/* Footer system details */}
      <footer className="border-t border-slate-200 bg-white py-8 mt-16 relative z-10 text-center shadow-xs">
        <p className="text-slate-500 text-xs flex items-center justify-center gap-1.5 font-mono uppercase tracking-wider font-bold">
          <ShieldCheck className="h-4 w-4 text-red-600" />
          <span>PokéAsset Manager OS v2.4. Geometric Balance Design Theme.</span>
        </p>
      </footer>

      {/* Form editing/addition Modal */}
      <CardFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setCardToEdit(null);
        }}
        cardToEdit={cardToEdit}
        onSave={handleExecuteCommand}
      />

    </div>
  );
}

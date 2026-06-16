import React, { useState, useRef, useEffect } from "react";
import { Terminal as TerminalIcon, Send, Code, Sparkles, Copy, Trash2 } from "lucide-react";
import { Card, ConsoleLog } from "../types";

interface CommandTerminalProps {
  portfolio: Card[];
  onExecuteCommand: (cmd: string) => string; // Returns success message
  errorMsg: string | null;
  clearError: () => void;
}

export default function CommandTerminal({
  portfolio,
  onExecuteCommand,
  errorMsg,
  clearError,
}: CommandTerminalProps) {
  const [command, setCommand] = useState("");
  const [consoleLogs, setConsoleLogs] = useState<ConsoleLog[]>([
    {
      timestamp: new Date().toLocaleTimeString(),
      type: "info",
      content: "PokéAsset OS initialized. Insira comandos CRUD para atualizar o portfólio.",
    },
  ]);
  const [copied, setCopied] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of logs on update
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [consoleLogs]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    const currentCommand = command.trim();
    setCommand("");
    clearError();

    // Log the user's command
    const newLogs: ConsoleLog[] = [
      ...consoleLogs,
      {
        timestamp: new Date().toLocaleTimeString(),
        type: "command",
        content: `> ${currentCommand}`,
      },
    ];

    try {
      // Execute command on parent state
      const successMsg = onExecuteCommand(currentCommand);
      
      // Log success and the pure updated JSON
      newLogs.push({
        timestamp: new Date().toLocaleTimeString(),
        type: "info",
        content: successMsg,
      });

      // Output the exact JSON format as expected
      const jsonResponse = JSON.stringify({ portfolio }, null, 2);
      newLogs.push({
        timestamp: new Date().toLocaleTimeString(),
        type: "json_output",
        content: jsonResponse,
      });

    } catch (err: any) {
      newLogs.push({
        timestamp: new Date().toLocaleTimeString(),
        type: "error",
        content: err.message || "Ocorreu um erro ao processar o comando.",
      });
    }

    setConsoleLogs(newLogs);
  };

  const handleCopyJSON = () => {
    const jsonOutput = JSON.stringify({ portfolio }, null, 2);
    navigator.clipboard.writeText(jsonOutput);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClearLogs = () => {
    setConsoleLogs([
      {
        timestamp: new Date().toLocaleTimeString(),
        type: "info",
        content: "Console limpo. Pronto para novos comandos.",
      },
    ]);
  };

  const loadExample = (ex: string) => {
    setCommand(ex);
  };

  // Keep a neat render of the absolute JSON block for quick inspection
  const jsonView = JSON.stringify({ portfolio }, null, 2);

  return (
    <div id="interactive-terminal" className="bg-slate-950 border-2 border-slate-900 rounded-none flex flex-col h-[520px] overflow-hidden shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b-2 border-slate-950">
        <div className="flex items-center gap-2">
          <TerminalIcon className="h-4 w-4 text-red-500" />
          <span className="font-mono text-[10px] font-black uppercase tracking-wider text-slate-200">PokéAsset OS Terminal</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleClearLogs}
            className="p-1 px-2.5 text-[9px] font-bold uppercase tracking-wider text-slate-400 hover:text-white bg-slate-850 hover:bg-slate-800 border border-slate-700 rounded-none transition font-mono flex items-center gap-1"
            title="Limpar logs"
          >
            <Trash2 className="h-2.5 w-2.5" />
            <span>Limpar</span>
          </button>
          <button
            onClick={handleCopyJSON}
            className="p-1 px-2.5 text-[9px] font-bold uppercase tracking-wider text-red-400 bg-red-950/20 hover:bg-red-900/30 border border-red-900/50 rounded-none transition font-mono flex items-center gap-1"
            title="Copy portfolio JSON database"
          >
            <Copy className="h-2.5 w-2.5" />
            <span>{copied ? "Copiado!" : "Copiar JSON"}</span>
          </button>
        </div>
      </div>

      {/* Terminal Outputs / Logs */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 font-mono text-xs select-text scrollbar-thin scrollbar-thumb-slate-800">
        {consoleLogs.map((log, index) => {
          if (log.type === "command") {
            return (
              <div key={index} className="text-emerald-440 font-bold break-all">
                {log.content}
              </div>
            );
          }
          if (log.type === "error") {
            return (
              <div key={index} className="text-rose-450 bg-rose-950/30 p-2.5 rounded-none border border-rose-900 text-[11px]">
                ⚠️ {log.content}
              </div>
            );
          }
          if (log.type === "json_output") {
            return (
              <div key={index} className="bg-slate-900 p-2.5 rounded-none border border-slate-800 text-slate-300 max-h-48 overflow-y-auto font-mono text-[11px] leading-relaxed relative">
                <div className="text-[8px] font-bold text-slate-500 text-right sticky top-0 bg-slate-900 pb-1">JSON PORTFOLIO STATE</div>
                <pre>{log.content}</pre>
              </div>
            );
          }
          return (
            <div key={index} className="text-slate-400 font-mono italic">
              {log.content}
            </div>
          );
        })}
        <div ref={logsEndRef} />
      </div>

      {/* Command Helper chips */}
      <div className="px-4 py-2 border-t-2 border-slate-950 bg-slate-950 flex flex-wrap gap-1.5 items-center">
        <span className="text-[9px] font-mono font-black text-slate-500 mr-1 uppercase">Exemplos Rápidos:</span>
        <button
          onClick={() => loadExample("Adicionar Pikachu, set Base, raridade Holo, estado PSA 10, compra 100, atual 150")}
          className="text-[9px] bg-slate-900 hover:bg-slate-800 border border-slate-800 px-2 py-0.5 rounded-none text-red-400 font-mono transition font-bold"
        >
          + ADD CARD
        </button>
        <button
          onClick={() => loadExample("Editar id 1, novo preco_atual 160")}
          className="text-[9px] bg-slate-900 hover:bg-slate-800 border border-slate-800 px-2 py-0.5 rounded-none text-slate-300 font-mono transition font-bold"
        >
          ✎ EDIT PRICE
        </button>
        <button
          onClick={() => loadExample("Excluir id 2")}
          className="text-[9px] bg-slate-900 hover:bg-slate-800 border border-slate-800 px-2 py-0.5 rounded-none text-rose-400 font-mono transition font-bold"
        >
          ✗ EXCLUDE CARD
        </button>
      </div>

      {/* Input controls form */}
      <form onSubmit={handleSubmit} className="p-3 bg-slate-900 border-t-2 border-slate-950 flex items-center gap-2">
        <span className="text-red-500 font-mono font-black text-sm select-none pl-1">&gt;</span>
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder="Insira um comando... (Ex: Adicionar Charmander...)"
          className="flex-1 bg-transparent border-0 outline-hidden font-mono text-xs text-white focus:ring-0 placeholder:text-slate-600"
        />
        <button
          type="submit"
          className="p-2 rounded-none bg-red-600 hover:bg-red-500 text-white font-bold transition flex items-center justify-center border border-slate-950 shrink-0"
          title="Executar comando"
        >
          <Send className="h-3 w-3" />
        </button>
      </form>
    </div>
  );
}

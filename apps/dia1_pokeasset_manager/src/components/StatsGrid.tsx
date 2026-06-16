import { Card } from "../types";
import { TrendingUp, TrendingDown, DollarSign, Wallet, Percent, Database } from "lucide-react";

interface StatsGridProps {
  portfolio: Card[];
}

export default function StatsGrid({ portfolio }: StatsGridProps) {
  const totalInvested = portfolio.reduce((acc, card) => acc + card.preco_compra, 0);
  const totalCurrentValue = portfolio.reduce((acc, card) => acc + card.preco_atual, 0);
  const netProfitLoss = totalCurrentValue - totalInvested;
  
  const percentageYield = totalInvested > 0 
    ? (netProfitLoss / totalInvested) * 100 
    : 0;

  const profitCount = portfolio.filter(c => c.status === "lucro").length;
  const lossCount = portfolio.filter(c => c.status === "prejuizo").length;
  const neutralCount = portfolio.filter(c => c.status === "neutro").length;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {/* Total Invested */}
      <div id="stat-invested" className="bg-white border-2 border-slate-900 rounded-none p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Total Investido</span>
          <div className="p-1.5 bg-slate-100 text-slate-700 border border-slate-200">
            <Wallet className="h-4 w-4" />
          </div>
        </div>
        <div className="flex flex-col">
          <span className="text-xl font-mono font-bold text-slate-900">
            R$ {totalInvested.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
          <span className="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Custo acumulado de aquisição</span>
        </div>
      </div>

      {/* Target Current Value */}
      <div id="stat-current" className="bg-white border-2 border-slate-900 rounded-none p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Valor Atual</span>
          <div className="p-1.5 bg-slate-100 text-slate-700 border border-slate-200">
            <DollarSign className="h-4 w-4" />
          </div>
        </div>
        <div className="flex flex-col">
          <span className="text-xl font-mono font-bold text-slate-900">
            R$ {totalCurrentValue.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
          <span className="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Cotação ativa de mercado</span>
        </div>
      </div>

      {/* Margem Absoluta (Lucro / Prejuízo) */}
      <div id="stat-yield" className={`bg-white border-2 rounded-none p-5 shadow-xs flex flex-col justify-between ${
        netProfitLoss > 0 ? "border-emerald-500" : netProfitLoss < 0 ? "border-rose-500" : "border-slate-900"
      }`}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Rendimento Líquido</span>
          <div className={`p-1.5 rounded-none border ${
            netProfitLoss > 0 ? "bg-emerald-50 text-emerald-600 border-emerald-200" : netProfitLoss < 0 ? "bg-rose-50 text-rose-600 border-rose-200" : "bg-slate-100 text-slate-600 border-slate-200"
          }`}>
            {netProfitLoss >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
          </div>
        </div>
        <div className="flex flex-col">
          <span className={`text-xl font-mono font-bold ${
            netProfitLoss > 0 ? "text-emerald-600 text-shadow-sm" : netProfitLoss < 0 ? "text-rose-600" : "text-slate-800"
          }`}>
            {netProfitLoss > 0 ? "+" : ""}
            R$ {netProfitLoss.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
          <span className="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Saldo atualizado de retornos</span>
        </div>
      </div>

      {/* Returns Combined % */}
      <div id="stat-percent" className={`bg-white border-2 rounded-none p-5 shadow-xs flex flex-col justify-between ${
        percentageYield > 0 ? "border-emerald-500" : percentageYield < 0 ? "border-rose-500" : "border-slate-900"
      }`}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Valorização Global</span>
          <div className={`p-1.5 rounded-none border ${
            percentageYield > 0 ? "bg-emerald-50 text-emerald-600 border-emerald-200" : percentageYield < 0 ? "bg-rose-50 text-rose-600 border-rose-200" : "bg-slate-100 text-slate-600 border-slate-200"
          }`}>
            <Percent className="h-4 w-4" />
          </div>
        </div>
        <div className="flex flex-col">
          <span className={`text-xl font-mono font-bold underline decoration-2 underline-offset-4 ${
            percentageYield > 0 ? "text-emerald-600" : percentageYield < 0 ? "text-rose-600" : "text-slate-800"
          }`}>
            {percentageYield > 0 ? "+" : ""}
            {percentageYield.toFixed(2)}%
          </span>
          <div className="flex gap-2 text-[10px] text-slate-400 font-semibold uppercase mt-1">
            <span className="text-emerald-600">{profitCount} ativos</span>
            <span className="text-rose-600">{lossCount} prejuízo</span>
            <span className="text-slate-500">{neutralCount} neutro</span>
          </div>
        </div>
      </div>
    </div>
  );
}

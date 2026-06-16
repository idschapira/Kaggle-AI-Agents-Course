import React, { useState, useEffect } from "react";
import { Card } from "../types";
import { X, Sparkles, Plus, Check } from "lucide-react";

interface CardFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  cardToEdit: Card | null;
  onSave: (command: string) => void;
}

export default function CardFormModal({ isOpen, onClose, cardToEdit, onSave }: CardFormModalProps) {
  const [formData, setFormData] = useState({
    nome_carta: "",
    set: "",
    raridade: "Holo Rare",
    estado_conservacao: "PSA 10",
    preco_compra: "",
    preco_atual: "",
  });

  useEffect(() => {
    if (cardToEdit) {
      setFormData({
        nome_carta: cardToEdit.nome_carta,
        set: cardToEdit.set,
        raridade: cardToEdit.raridade,
        estado_conservacao: cardToEdit.estado_conservacao,
        preco_compra: String(cardToEdit.preco_compra),
        preco_atual: String(cardToEdit.preco_atual),
      });
    } else {
      setFormData({
        nome_carta: "",
        set: "",
        raridade: "Holo",
        estado_conservacao: "PSA 10",
        preco_compra: "100",
        preco_atual: "120",
      });
    }
  }, [cardToEdit, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.nome_carta.trim()) return;

    if (cardToEdit) {
      // Generate standard EDITAR command: e.g. "Editar id 1, nome Charizard, set Base, raridade Holo, estado PSA 10, preco_compra 100, preco_atual 120"
      // Wait, let's write a simple comma-separated modifier string that our utils robustly parses
      const cmd = `Editar id ${cardToEdit.id}, nome_carta ${formData.nome_carta}, set ${formData.set}, raridade ${formData.raridade}, estado ${formData.estado_conservacao}, preco_compra ${formData.preco_compra}, preco_atual ${formData.preco_atual}`;
      onSave(cmd);
    } else {
      // Generate standard ADICIONAR command
      const cmd = `Adicionar ${formData.nome_carta}, set ${formData.set || "Base"}, raridade ${formData.raridade}, estado ${formData.estado_conservacao}, compra ${formData.preco_compra || "0"}, atual ${formData.preco_atual || "0"}`;
      onSave(cmd);
    }
    onClose();
  };

  return (
    <div id="card-modal" className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-xs">
      <div className="bg-white border-2 border-slate-900 rounded-none w-full max-w-md overflow-hidden shadow-[8px_8px_0px_rgba(15,23,42,1)] relative">
        {/* Top accent bar */}
        <div className="h-2 bg-red-600 w-full" />

        {/* Modal Header */}
        <div className="p-5 border-b-2 border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-red-600 rounded-full border-2 border-slate-900 flex items-center justify-center shrink-0">
              <div className="w-1.5 h-1.5 bg-slate-900 rounded-full"></div>
            </div>
            <h2 className="text-sm font-black uppercase tracking-tight text-slate-900">
              {cardToEdit ? "Editar Carta Pokémon" : "Adicionar Novo Ativo"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-900 transition"
            title="Fechar"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          {/* Card Name */}
          <div>
            <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
              Nome da Carta
            </label>
            <input
              type="text"
              required
              placeholder="Ex: Lugia, Charizard, Blastoise"
              value={formData.nome_carta}
              onChange={(e) => setFormData({ ...formData, nome_carta: e.target.value })}
              className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-4 py-2 text-xs text-slate-950 font-bold uppercase focus:outline-hidden focus:border-red-600 transition"
              autoFocus
            />
          </div>

          {/* Card Set */}
          <div>
            <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
              Coleção / Set
            </label>
            <input
              type="text"
              placeholder="Ex: Base Set, Fossil, Neo Destiny, Skyridge"
              value={formData.set}
              onChange={(e) => setFormData({ ...formData, set: e.target.value })}
              className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-4 py-2 text-xs text-slate-950 font-bold uppercase focus:outline-hidden focus:border-red-600 transition"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Rarity */}
            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
                Raridade
              </label>
              <select
                value={formData.raridade}
                onChange={(e) => setFormData({ ...formData, raridade: e.target.value })}
                className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-3 py-2 text-xs text-slate-955 font-bold uppercase focus:outline-hidden focus:border-red-650 transition cursor-pointer"
              >
                <option value="Holo">Holo</option>
                <option value="Holo Rare">Holo Rare</option>
                <option value="Secret Rare">Secret Rare</option>
                <option value="Ultra Rare">Ultra Rare</option>
                <option value="Promo">Promo</option>
                <option value="Rare">Rare</option>
                <option value="Common">Common</option>
              </select>
            </div>

            {/* Condition grade */}
            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
                Conservação
              </label>
              <select
                value={formData.estado_conservacao}
                onChange={(e) => setFormData({ ...formData, estado_conservacao: e.target.value })}
                className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-3 py-2 text-xs text-slate-955 font-bold uppercase focus:outline-hidden focus:border-red-650 transition cursor-pointer"
              >
                <option value="PSA 10">PSA 10 (Gem Mint)</option>
                <option value="PSA 9">PSA 9 (Mint)</option>
                <option value="PSA 8">PSA 8 (NM-MT)</option>
                <option value="BGS 10">BGS 10 (Pristine)</option>
                <option value="Near Mint">Near Mint (NM)</option>
                <option value="Excellent">Excellent (EX)</option>
                <option value="Played">Played (PL)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Purchase Price */}
            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
                Preço de Compra (R$)
              </label>
              <input
                type="number"
                step="any"
                min="0"
                required
                value={formData.preco_compra}
                onChange={(e) => setFormData({ ...formData, preco_compra: e.target.value })}
                className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-4 py-2 text-xs text-slate-950 font-mono font-bold focus:outline-hidden focus:border-red-600 transition"
              />
            </div>

            {/* Current Price */}
            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1.5">
                Preço Atual (R$)
              </label>
              <input
                type="number"
                step="any"
                min="0"
                required
                value={formData.preco_atual}
                onChange={(e) => setFormData({ ...formData, preco_atual: e.target.value })}
                className="w-full bg-slate-50 border-2 border-slate-900 rounded-none px-4 py-2 text-xs text-slate-955 font-mono font-bold focus:outline-hidden focus:border-red-600 transition"
              />
            </div>
          </div>

          {/* Form Actions */}
          <div className="pt-4 flex gap-3 border-t-2 border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-slate-150 hover:bg-slate-200 text-slate-700 border-2 border-slate-900 rounded-none py-2.5 text-xs font-bold uppercase tracking-wider transition"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 bg-red-600 hover:bg-slate-900 hover:text-white text-white border-2 border-slate-900 rounded-none py-2.5 text-xs font-black uppercase tracking-wider transition flex items-center justify-center gap-1.5"
            >
              {cardToEdit ? (
                <>
                  <Check className="h-4 w-4" />
                  <span>Atualizar</span>
                </>
              ) : (
                <>
                  <Plus className="h-4 w-4" />
                  <span>Cadastrar</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

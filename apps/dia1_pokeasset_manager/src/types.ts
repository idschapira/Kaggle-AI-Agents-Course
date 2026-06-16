export interface Card {
  id: number;
  nome_carta: string;
  set: string;
  raridade: string;
  estado_conservacao: string;
  preco_compra: number;
  preco_atual: number;
  valorizacao_absoluta: number;
  valorizacao_percentual: string;
  status: "lucro" | "prejuizo" | "neutro";
  // Custom metadata for visualization
  sprite_color?: string;
}

export interface SearchState {
  searchTerm: string;
  statusFilter: "todos" | "lucro" | "prejuizo" | "neutro";
  rarityFilter: string;
}

export interface ConsoleLog {
  timestamp: string;
  type: "command" | "json_output" | "error" | "info";
  content: string;
}

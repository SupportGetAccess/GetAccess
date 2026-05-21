import { create } from 'zustand';
import { CartItem, CompradorData } from '../types';

interface CartState {
  items: CartItem[];
  comprador: CompradorData | null;
  total: number;

  addItem: (item: CartItem) => void;
  removeItem: (eventoId: number) => void;
  updateCantidad: (eventoId: number, cantidad: number) => void;
  setComprador: (data: CompradorData | null) => void;
  clearCart: () => void;
  recalculateTotal: () => void;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  comprador: null,
  total: 0,

  addItem: (item) => {
    const items = get().items;
    const existing = items.find((i) => i.evento.id === item.evento.id);
    if (existing) {
      existing.cantidad += item.cantidad;
      set({ items: [...items] });
    } else {
      set({ items: [...items, item] });
    }
    get().recalculateTotal();
  },

  removeItem: (eventoId) => {
    set({ items: get().items.filter((i) => i.evento.id !== eventoId) });
    get().recalculateTotal();
  },

  updateCantidad: (eventoId, cantidad) => {
    const items = get().items.map((i) =>
      i.evento.id === eventoId ? { ...i, cantidad } : i
    );
    set({ items });
    get().recalculateTotal();
  },

  setComprador: (data) => set({ comprador: data }),

  clearCart: () => set({ items: [], total: 0 }),

  recalculateTotal: () => {
    const total = get().items.reduce((sum, i) => {
      const precioConComision = i.evento.precio * (1 + (i.evento.comision || 0) / 100);
      return sum + precioConComision * i.cantidad;
    }, 0);
    set({ total });
  },
}));

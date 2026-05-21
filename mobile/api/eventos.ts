import api from './client';
import { Evento } from '../types';

export const eventosApi = {
  listar: (params?: { categoria?: string; busqueda?: string }) =>
    api.get<Evento[]>('/api/eventos/', { params }),

  obtener: (id: number) =>
    api.get<Evento>(`/api/eventos/${id}`),

  obtenerPorPublicId: (publicId: string) =>
    api.get<{ id: number; public_id: string }>(`/api/eventos/public/${publicId}`),

  buscar: (q: string, limite = 10) =>
    api.get<{ eventos: Evento[]; recintos: string[] }>('/api/eventos/buscar', { params: { q, limite } }),

  categorias: () =>
    api.get<string[]>('/api/eventos/categorias'),
};

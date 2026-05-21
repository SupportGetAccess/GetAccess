import api from './client';
import { Entrada, CompradorData } from '../types';

export const entradasApi = {
  listar: () => api.get<Entrada[]>('/api/entradas/'),

  pendientes: () => api.get<Entrada[]>('/api/entradas/pendientes'),

  crear: (evento_id: number, cantidad: number) =>
    api.post<Entrada>('/api/entradas/', { evento_id, cantidad }),

  crearInvitado: (data: { entradas: { evento_id: number; cantidad: number }[]; comprador: CompradorData }) =>
    api.post<{ entrada_ids: number[]; total: number; estado: string; email: string }>('/api/entradas/invitado', data),

  buscar: (q: string) =>
    api.get<Entrada[]>('/api/entradas/buscar', { params: { q } }),

  confirmarPago: (entrada_id: number) =>
    api.post<{ success: boolean; mensaje: string }>(`/api/entradas/${entrada_id}/confirmar-pago`),

  transferir: (entrada_id: number, email_destino: string) =>
    api.post<{ mensaje: string; token: string }>(`/api/entradas/${entrada_id}/transferir`, { email_destino }),

  aceptarTransferencia: (token: string) =>
    api.post<{ mensaje: string }>(`/api/entradas/aceptar-transferencia?token=${token}`),

  transferenciasPendientes: () =>
    api.get<{ id: number; entrada_id: number; email: string; evento_nombre: string; token: string }[]>('/api/transferencias/pendientes'),
};

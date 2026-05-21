import api from './client';
import { QrPaymentResponse, LinkPaymentResponse, QrStatusResponse, CompradorData } from '../types';

export const pagosApi = {
  qr: (entrada_ids: number[]) =>
    api.post<QrPaymentResponse>('/api/pagos/qr', { entrada_ids }),

  qrInvitado: (data: { entradas: { evento_id: number; cantidad: number }[]; comprador: CompradorData }) =>
    api.post<QrPaymentResponse>('/api/pagos/qr/invitado', data),

  qrStatus: (qr_order_id: string) =>
    api.get<QrStatusResponse>(`/api/pagos/qr/${qr_order_id}/status`),

  qrCancelar: (qr_order_id: string) =>
    api.post<{ success: boolean; entrada_ids: number[] }>(`/api/pagos/qr/${qr_order_id}/cancelar`),

  linkCarrito: (entrada_ids: number[]) =>
    api.post<LinkPaymentResponse>('/api/pagos/carrito', { entrada_ids }),

  linkCarritoInvitado: (data: { entradas: { evento_id: number; cantidad: number }[]; comprador: CompradorData }) =>
    api.post<LinkPaymentResponse>('/api/pagos/carrito/invitado', data),
};

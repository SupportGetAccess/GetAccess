import api from './client';

export interface DashboardData {
  ventas_total: number;
  ingresos_total: number;
  tickets_usados: number;
  precio_promedio: number;
  por_categoria: { categoria: string; cantidad: number }[];
  top_eventos: { id: number; nombre: string; vendidos: number; ingresos: number }[];
  ventas_por_dia: { fecha: string; cantidad: number }[];
  proyeccion: {
    probabilidad_agotar: number;
    dias_promedio_venta: number;
    tendencia: string;
  };
}

export interface SolicitudOrganizer {
  id: number;
  usuario_id: number;
  estado: string;
  motivo_rechazo: string | null;
  created_at: string;
  email: string;
  nombre: string;
  apellido: string;
}

export interface Validacion {
  id: number;
  entrada_id: number;
  timestamp: string;
  scanner: string;
  evento_id: number;
  evento_nombre: string;
}

export const adminApi = {
  dashboard: () =>
    api.get<DashboardData>('/api/analytics/general'),

  solicitudes: () =>
    api.get<SolicitudOrganizer[]>('/api/admin/solicitudes-organizer'),

  aprobarOrganizer: (solicitud_id: number) =>
    api.post<{ message: string }>('/api/admin/aprobar-organizer', { solicitud_id }),

  rechazarOrganizer: (solicitud_id: number, motivo?: string) =>
    api.post<{ message: string }>('/api/admin/rechazar-organizer', { solicitud_id, motivo }),

  validaciones: (evento_id?: number) =>
    api.get<Validacion[]>('/api/validaciones/historial', { params: evento_id ? { evento_id } : {} }),
};

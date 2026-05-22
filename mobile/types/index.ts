export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  verificado: boolean;
  rol: 'usuario' | 'admin' | 'organizer';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: Usuario;
}

export interface Evento {
  id: number;
  nombre: string;
  descripcion: string;
  fecha: string;
  lugar: string;
  precio: number;
  capacidad: number;
  vendidos: number;
  disponibles: number;
  imagen: string;
  imagenes?: { id: number; url: string; orden: number }[];
  categoria: string;
  comision: number;
  public_id: string;
  creado_por?: number;
}

export interface Entrada {
  id: number;
  evento_id: number;
  usuario_id: number | null;
  cantidad: number;
  total: number;
  estado: 'pendiente' | 'pagada' | 'expirada';
  preference_id: string;
  payment_id: string;
  payment_order_id: string;
  creada_en: string;
  expira_en: string;
  usada: boolean;
  transferida: boolean;
  email_comprador: string | null;
  nombre_comprador: string | null;
  apellido_comprador: string | null;
  telefono_comprador: string | null;
  evento_nombre?: string;
  evento_fecha?: string;
  evento_lugar?: string;
}

export interface CompradorData {
  nombre: string;
  apellido: string;
  email: string;
  email_confirm: string;
  telefono: string;
}

export interface CartItem {
  evento: Evento;
  cantidad: number;
}

export interface QrPaymentResponse {
  qr_order_id: string;
  qr_code: string;
  total: number;
  expires_in: number;
  entradas: number[];
}

export interface LinkPaymentResponse {
  init_point: string;
  preference_id: string;
  entrada_ids: number[];
  total: number;
}

export interface QrStatusResponse {
  estado: 'pendiente' | 'pagado' | 'expirado';
  qr_order_id: string;
  email_comprador?: string;
  total?: number;
}

import api from './client';
import { AuthResponse, Usuario } from '../types';

export const authApi = {
  login: (email: string, password: string) =>
    api.post<AuthResponse>('/api/auth/login', { email, password }),

  register: (data: { email: string; nombre: string; apellido: string; password: string }) =>
    api.post<{ message: string; email: string; codigo: string; requires_verification: boolean }>(
      '/api/auth/registro', data
    ),

  verify: (email: string, codigo: string) =>
    api.post<AuthResponse>('/api/auth/verificar', { email, codigo }),

  me: () => api.get<Usuario>('/api/auth/me'),

  updateProfile: (data: Partial<{ nombre: string; apellido: string; email: string; password_actual: string; password_nuevo: string }>) =>
    api.put<{ message: string; email: string; nombre: string; apellido: string }>('/api/auth/perfil', data),

  solicitarOrganizer: () => api.post<{ message: string }>('/api/auth/solicitar-organizer'),

  recuperarPassword: (email: string) =>
    api.post<{ message: string }>('/api/auth/recuperar', { email }),

  restablecerPassword: (token: string, nueva_password: string) =>
    api.post<{ message: string }>('/api/auth/restablecer', { token, nueva_password }),
};

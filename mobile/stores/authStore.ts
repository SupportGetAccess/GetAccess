import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { Usuario } from '../types';
import { authApi } from '../api/auth';

interface AuthState {
  user: Usuario | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; nombre: string; apellido: string; password: string }) => Promise<{ email: string; codigo: string }>;
  verify: (email: string, codigo: string) => Promise<void>;
  logout: () => Promise<void>;
  loadStoredAuth: () => Promise<void>;
  updateUser: (user: Usuario) => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: true,
  isAuthenticated: false,

  login: async (email, password) => {
    const res = await authApi.login(email, password);
    const { access_token, user } = res.data;
    await SecureStore.setItemAsync('auth_token', access_token);
    set({ user, token: access_token, isAuthenticated: true });
  },

  register: async (data) => {
    const res = await authApi.register(data);
    return { email: res.data.email, codigo: res.data.codigo };
  },

  verify: async (email, codigo) => {
    const res = await authApi.verify(email, codigo);
    const { access_token, user } = res.data;
    await SecureStore.setItemAsync('auth_token', access_token);
    set({ user, token: access_token, isAuthenticated: true });
  },

  logout: async () => {
    await SecureStore.deleteItemAsync('auth_token');
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadStoredAuth: async () => {
    try {
      const token = await SecureStore.getItemAsync('auth_token');
      if (token) {
        const res = await authApi.me();
        set({ user: res.data, token, isAuthenticated: true, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch {
      await SecureStore.deleteItemAsync('auth_token');
      set({ isLoading: false });
    }
  },

  updateUser: (user) => set({ user }),
}));

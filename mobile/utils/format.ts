import Constants from 'expo-constants';

export function formatPrecio(precio: number): string {
  return `$${precio.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

const API_URL = Constants.expoConfig?.extra?.apiUrl || 'https://getaccess.com.ar';

export function getImageUrl(imagen?: string | null): string | null {
  if (!imagen) return null;
  if (imagen.startsWith('http://') || imagen.startsWith('https://')) return imagen;
  return `${API_URL}${imagen.startsWith('/') ? '' : '/'}${imagen}`;
}

export function parseFecha(fechaStr: string): string {
  try {
    const date = new Date(fechaStr);
    return date.toLocaleDateString('es-AR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return fechaStr;
  }
}

export function parseFechaCorta(fechaStr: string): string {
  try {
    const date = new Date(fechaStr);
    return date.toLocaleDateString('es-AR', {
      day: 'numeric',
      month: 'short',
    });
  } catch {
    return fechaStr;
  }
}

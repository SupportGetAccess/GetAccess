import Constants from 'expo-constants';

export function formatPrecio(precio: number): string {
  return `$${precio.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

const API_URL = Constants.expoConfig?.extra?.apiUrl || 'https://getaccess.com.ar';

export function getImageUrl(imagen?: string | null): string | null {
  if (!imagen) return null;

  // El backend puede devolver un JSON array string: '["https://..."]' o '["url1","url2"]'
  if (typeof imagen === 'string' && (imagen.trim().startsWith('[') || imagen.trim().startsWith('"'))) {
    try {
      const parsed = JSON.parse(imagen.trim());
      if (Array.isArray(parsed)) {
        const url = parsed.find((u) => u && typeof u === 'string' && (u.startsWith('http://') || u.startsWith('https://')));
        if (url) return url;
      }
      if (typeof parsed === 'string' && (parsed.startsWith('http://') || parsed.startsWith('https://'))) return parsed;
    } catch {}
  }

  if (imagen.startsWith('http://') || imagen.startsWith('https://')) return imagen;
  return `${API_URL}${imagen.startsWith('/') ? '' : '/'}${imagen}`;
}

export function isEventoFinalizado(fechaStr: string): boolean {
  try {
    return new Date(fechaStr) < new Date();
  } catch {
    return false;
  }
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

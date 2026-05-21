export function formatPrecio(precio: number): string {
  return `$${precio.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
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

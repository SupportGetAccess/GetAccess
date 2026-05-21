export function validarEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validarTelefono(tel: string): boolean {
  return /^\d{8,15}$/.test(tel);
}

export function validarPassword(password: string): string | null {
  if (password.length < 8) return 'Mínimo 8 caracteres';
  if (!/[A-Z]/.test(password)) return 'Debe contener una mayúscula';
  if (!/[a-z]/.test(password)) return 'Debe contener una minúscula';
  if (!/[0-9]/.test(password)) return 'Debe contener un número';
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) return 'Debe contener un símbolo';
  return null;
}

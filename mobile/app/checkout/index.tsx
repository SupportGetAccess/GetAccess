import { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Alert, ActivityIndicator, TextInput, Image, Platform } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as WebBrowser from 'expo-web-browser';
import { colors } from '../../theme';
import { useCartStore } from '../../stores/cartStore';
import { useAuthStore } from '../../stores/authStore';
import { pagosApi } from '../../api/pagos';
import { entradasApi } from '../../api/entradas';
import { formatPrecio } from '../../utils/format';
import { validarEmail, validarTelefono } from '../../utils/validators';

export default function CheckoutScreen() {
  const items = useCartStore((s) => s.items);
  const total = useCartStore((s) => s.total);
  const clearCart = useCartStore((s) => s.clearCart);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const [pagoMethod, setPagoMethod] = useState<'qr' | 'link'>('qr');
  const [loading, setLoading] = useState(false);
  const [qrCode, setQrCode] = useState('');
  const [qrOrderId, setQrOrderId] = useState('');
  const [qrStatus, setQrStatus] = useState<'idle' | 'pending' | 'pagado' | 'expirado'>('idle');
  const [countdown, setCountdown] = useState(600);
  const pollingRef = useRef<ReturnType<typeof setInterval>>(undefined);

  // Guest data form
  const [guestNombre, setGuestNombre] = useState('');
  const [guestApellido, setGuestApellido] = useState('');
  const [guestEmail, setGuestEmail] = useState('');
  const [guestEmailConfirm, setGuestEmailConfirm] = useState('');
  const [guestTelefono, setGuestTelefono] = useState('');

  const isGuest = !isAuthenticated;

  const getCompradorData = () => ({
    nombre: guestNombre,
    apellido: guestApellido,
    email: guestEmail,
    email_confirm: guestEmailConfirm,
    telefono: guestTelefono,
  });

  const validateGuestFields = () => {
    if (guestNombre.length < 2) { Alert.alert('Error', 'Nombre debe tener al menos 2 caracteres'); return false; }
    if (guestApellido.length < 2) { Alert.alert('Error', 'Apellido debe tener al menos 2 caracteres'); return false; }
    if (!validarEmail(guestEmail)) { Alert.alert('Error', 'Email inválido'); return false; }
    if (guestEmail !== guestEmailConfirm) { Alert.alert('Error', 'Los emails no coinciden'); return false; }
    if (!validarTelefono(guestTelefono)) { Alert.alert('Error', 'Teléfono inválido (8-15 dígitos)'); return false; }
    return true;
  };

  const crearEntradas = async () => {
    const payload = {
      entradas: items.map((i) => ({ evento_id: i.evento.id, cantidad: i.cantidad })),
    };
    if (isGuest) {
      return entradasApi.crearInvitado({ ...payload, comprador: getCompradorData() });
    }
    const results = await Promise.all(
      items.map((i) => entradasApi.crear(i.evento.id, i.cantidad))
    );
    return { data: { entrada_ids: results.map((r) => r.data.id), total } };
  };

  const handlePagar = async () => {
    if (isGuest && !validateGuestFields()) return;
    if (items.length === 0) { Alert.alert('Error', 'Carrito vacío'); return; }
    setLoading(true);
    try {
      const entradasRes = await crearEntradas();
      const entradaIds = entradasRes.data.entrada_ids;

      if (pagoMethod === 'qr') {
        let orderId = '';
        if (isGuest) {
          const payload = { entradas: items.map((i) => ({ evento_id: i.evento.id, cantidad: i.cantidad })), comprador: getCompradorData() };
          const res = await pagosApi.qrInvitado(payload);
          setQrCode(res.data.qr_code);
          orderId = res.data.qr_order_id;
          setQrOrderId(orderId);
        } else {
          const res = await pagosApi.qr(entradaIds);
          setQrCode(res.data.qr_code);
          orderId = res.data.qr_order_id;
          setQrOrderId(orderId);
        }
        setQrStatus('pending');
        setCountdown(600);
        startPolling(orderId);
      } else {
        if (isGuest) {
          const payload = { entradas: items.map((i) => ({ evento_id: i.evento.id, cantidad: i.cantidad })), comprador: getCompradorData() };
          const res = await pagosApi.linkCarritoInvitado(payload);
          await WebBrowser.openBrowserAsync(res.data.init_point);
        } else {
          const res = await pagosApi.linkCarrito(entradaIds);
          await WebBrowser.openBrowserAsync(res.data.init_point);
        }
      }
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al procesar el pago');
    } finally {
      setLoading(false);
    }
  };

  const startPolling = (orderId: string) => {
    pollingRef.current = setInterval(async () => {
      try {
        const res = await pagosApi.qrStatus(orderId);
        if (res.data.estado === 'pagado') {
          setQrStatus('pagado');
          clearInterval(pollingRef.current);
          clearCart();
        }
      } catch {}
    }, 3000);
  };

  useEffect(() => {
    return () => clearInterval(pollingRef.current);
  }, []);

  useEffect(() => {
    if (qrStatus !== 'pending') return;
    if (countdown <= 0) {
      clearInterval(pollingRef.current);
      pagosApi.qrCancelar(qrOrderId).catch(() => {});
      setQrStatus('expirado');
      return;
    }
    const timer = setInterval(() => setCountdown((c) => c - 1), 1000);
    return () => clearInterval(timer);
  }, [countdown, qrStatus]);

  if (qrStatus === 'pagado') {
    return (
      <View style={styles.center}>
        <Ionicons name="checkmark-circle" size={80} color={colors.success} />
        <Text style={styles.successTitle}>¡Compra Exitosa!</Text>
        <Text style={styles.successText}>Recibirás tus entradas por email</Text>
        <TouchableOpacity style={styles.button} onPress={() => { clearCart(); router.replace('/(tabs)/eventos'); }}>
          <Text style={styles.buttonText}>Volver a Eventos</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (qrStatus === 'pending') {
    const minutes = Math.floor(countdown / 60);
    const seconds = countdown % 60;
    return (
      <View style={styles.center}>
        <Text style={styles.qrTitle}>Escaneá el QR para pagar</Text>
        <Text style={styles.qrTotal}>Total: {formatPrecio(total)}</Text>
        <View style={styles.qrContainer}>
          {qrCode ? (
            <Image source={{ uri: `https://quickchart.io/qr?size=250&text=${encodeURIComponent(qrCode)}` }} style={styles.qrImage} />
          ) : (
            <ActivityIndicator size="large" color={colors.primary} />
          )}
        </View>
        <Text style={styles.qrTimer}>
          {minutes}:{seconds.toString().padStart(2, '0')}
        </Text>
        <TouchableOpacity style={styles.cancelButton} onPress={() => {
          clearInterval(pollingRef.current);
          pagosApi.qrCancelar(qrOrderId).catch(() => {});
          setQrStatus('expirado');
        }}>
          <Text style={styles.cancelText}>Cancelar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Pago</Text>
      <View style={styles.resumen}>
        <Text style={styles.sectionTitle}>Resumen</Text>
        {items.map((item) => (
          <View key={item.evento.id} style={styles.resumenRow}>
            <Text style={styles.resumenNombre} numberOfLines={1}>{item.evento.nombre} x{item.cantidad}</Text>
            <Text style={styles.resumenPrecio}>{formatPrecio(item.evento.precio * item.cantidad)}</Text>
          </View>
        ))}
        <View style={styles.totalRow}>
          <Text style={styles.totalLabel}>Total</Text>
          <Text style={styles.totalValue}>{formatPrecio(total)}</Text>
        </View>
      </View>
      {isGuest && (
        <View style={styles.guestForm}>
          <Text style={styles.sectionTitle}>Datos del Comprador</Text>
          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Nombre</Text>
              <TextInput style={styles.input} placeholder="Juan" placeholderTextColor={colors.textMuted} value={guestNombre} onChangeText={setGuestNombre} />
            </View>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Apellido</Text>
              <TextInput style={styles.input} placeholder="Pérez" placeholderTextColor={colors.textMuted} value={guestApellido} onChangeText={setGuestApellido} />
            </View>
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Email</Text>
            <TextInput style={styles.input} placeholder="tu@email.com" placeholderTextColor={colors.textMuted} value={guestEmail} onChangeText={setGuestEmail} keyboardType="email-address" autoCapitalize="none" />
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Repetir Email</Text>
            <TextInput style={styles.input} placeholder="tu@email.com" placeholderTextColor={colors.textMuted} value={guestEmailConfirm} onChangeText={setGuestEmailConfirm} keyboardType="email-address" autoCapitalize="none" />
            {guestEmailConfirm && guestEmail !== guestEmailConfirm && (
              <Text style={styles.fieldError}>Los emails no coinciden</Text>
            )}
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Teléfono</Text>
            <TextInput style={styles.input} placeholder="1123456789" placeholderTextColor={colors.textMuted} value={guestTelefono} onChangeText={(t) => setGuestTelefono(t.replace(/[^0-9]/g, ''))} keyboardType="number-pad" />
          </View>
        </View>
      )}
      <View style={styles.pagoMethods}>
        <Text style={styles.sectionTitle}>Método de Pago</Text>
        <View style={styles.methodRow}>
          <TouchableOpacity
            style={[styles.methodButton, pagoMethod === 'qr' && styles.methodActive]}
            onPress={() => setPagoMethod('qr')}
          >
            <Ionicons name="qr-code" size={24} color={pagoMethod === 'qr' ? colors.white : colors.textSecondary} />
            <Text style={[styles.methodText, pagoMethod === 'qr' && styles.methodTextActive]}>Pagar con QR</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.methodButton, pagoMethod === 'link' && styles.methodActive]}
            onPress={() => setPagoMethod('link')}
          >
            <Ionicons name="card" size={24} color={pagoMethod === 'link' ? colors.white : colors.textSecondary} />
            <Text style={[styles.methodText, pagoMethod === 'link' && styles.methodTextActive]}>Link de Pago</Text>
          </TouchableOpacity>
        </View>
      </View>
      <TouchableOpacity style={[styles.pagarButton, loading && styles.buttonDisabled]} onPress={handlePagar} disabled={loading}>
        {loading ? (
          <ActivityIndicator color={colors.white} />
        ) : (
          <Text style={styles.pagarText}>Pagar {formatPrecio(total)}</Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: 16, paddingTop: 80, paddingBottom: 40 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  backButton: { position: 'absolute', top: 40, left: 16, zIndex: 10 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: 12 },
  resumen: { backgroundColor: colors.card, borderRadius: 12, padding: 16, marginBottom: 20 },
  resumenRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  resumenNombre: { color: colors.text, flex: 1, fontSize: 14 },
  resumenPrecio: { color: colors.textSecondary, fontSize: 14, marginLeft: 8 },
  totalRow: { flexDirection: 'row', justifyContent: 'space-between', borderTopWidth: 1, borderTopColor: colors.border, paddingTop: 12, marginTop: 4 },
  totalLabel: { color: colors.text, fontSize: 16, fontWeight: 'bold' },
  totalValue: { color: colors.primary, fontSize: 16, fontWeight: 'bold' },
  guestForm: { backgroundColor: colors.card, borderRadius: 12, padding: 16, marginBottom: 20, gap: 12 },
  row: { flexDirection: 'row', gap: 12 },
  inputGroup: { gap: 4 },
  label: { color: colors.textSecondary, fontSize: 12 },
  input: {
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 8,
    padding: 12,
    color: colors.text,
    fontSize: 14,
  },
  fieldError: { color: colors.error, fontSize: 11, marginTop: 2 },
  pagoMethods: { marginBottom: 20 },
  methodRow: { flexDirection: 'row', gap: 12 },
  methodButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.card,
    padding: 14,
    borderRadius: 10,
    gap: 8,
  },
  methodActive: { backgroundColor: colors.primary },
  methodText: { color: colors.textSecondary, fontSize: 14, fontWeight: '500' },
  methodTextActive: { color: colors.white },
  pagarButton: {
    backgroundColor: colors.primary,
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
  },
  pagarText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
  buttonDisabled: { opacity: 0.6 },
  button: { backgroundColor: colors.primary, paddingHorizontal: 32, paddingVertical: 14, borderRadius: 8, marginTop: 20 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: '600' },
  successTitle: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginTop: 16 },
  successText: { color: colors.textSecondary, fontSize: 14, marginTop: 8, textAlign: 'center' },
  qrTitle: { fontSize: 18, fontWeight: '600', color: colors.text, marginBottom: 8 },
  qrTotal: { color: colors.primary, fontSize: 20, fontWeight: 'bold', marginBottom: 20 },
  qrContainer: {
    backgroundColor: colors.white,
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  qrImage: { width: 250, height: 250 },
  qrTimer: { color: colors.textSecondary, fontSize: 32, fontWeight: 'bold', marginBottom: 20 },
  cancelButton: { padding: 12 },
  cancelText: { color: colors.error, fontSize: 14 },
});

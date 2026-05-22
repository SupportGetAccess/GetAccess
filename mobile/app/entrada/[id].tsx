import { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Share, Alert, TextInput, Modal, KeyboardAvoidingView, Platform } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import QRCode from 'react-native-qrcode-svg';
import { entradasApi } from '../../api/entradas';
import { colors } from '../../theme';
import { formatPrecio, parseFecha } from '../../utils/format';
import { useAuthStore } from '../../stores/authStore';
import { validarEmail } from '../../utils/validators';

export default function EntradaDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const queryClient = useQueryClient();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [showTransfer, setShowTransfer] = useState(false);
  const [transferEmail, setTransferEmail] = useState('');

  const { data: entrada } = useQuery({
    queryKey: ['entrada', id],
    queryFn: async () => {
      const res = await entradasApi.listar();
      return res.data.find((e) => e.id === Number(id));
    },
    enabled: !!id,
  });

  const transferMutation = useMutation({
    mutationFn: ({ entrada_id, email }: { entrada_id: number; email: string }) =>
      entradasApi.transferir(entrada_id, email),
    onSuccess: () => {
      setShowTransfer(false);
      setTransferEmail('');
      queryClient.invalidateQueries({ queryKey: ['mis-entradas'] });
      Alert.alert('Transferida', 'Entrada transferida exitosamente');
    },
    onError: (err: any) => {
      Alert.alert('Error', err.response?.data?.detail || 'Error al transferir');
    },
  });

  if (!entrada) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>Entrada no encontrada</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.back()}>
          <Text style={styles.buttonText}>Volver</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleCompartir = async () => {
    try {
      await Share.share({
        message: `Get Access - Entrada: ${entrada.preference_id}`,
      });
    } catch {}
  };

  const handleTransferir = () => {
    if (!validarEmail(transferEmail)) {
      Alert.alert('Error', 'Email inválido');
      return;
    }
    transferMutation.mutate({ entrada_id: entrada.id, email: transferEmail });
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <View style={styles.content}>
        <Text style={styles.eventoNombre}>{entrada.evento_nombre || `Entrada #${entrada.id}`}</Text>
        {entrada.evento_fecha && <Text style={styles.fecha}>{parseFecha(entrada.evento_fecha)}</Text>}
        {entrada.evento_lugar && <Text style={styles.lugar}>{entrada.evento_lugar}</Text>}
        <Text style={styles.cantidad}>{entrada.cantidad} entrada(s) · {formatPrecio(entrada.total)}</Text>
        <View style={styles.qrContainer}>
          {entrada.preference_id ? (
            <QRCode
              value={entrada.preference_id}
              size={220}
              backgroundColor={colors.white}
              color={colors.black}
            />
          ) : (
            <Ionicons name="qr-code" size={120} color={colors.textMuted} />
          )}
        </View>
        <Text style={styles.codigo}>{entrada.preference_id}</Text>
        <View style={styles.estadoBadge}>
          <Text style={styles.estadoText}>{entrada.estado.toUpperCase()}</Text>
        </View>
        <View style={styles.actionsRow}>
          <TouchableOpacity style={styles.actionButton} onPress={handleCompartir}>
            <Ionicons name="share-outline" size={20} color={colors.white} />
            <Text style={styles.actionText}>Compartir</Text>
          </TouchableOpacity>
          {isAuthenticated && entrada.estado === 'pagada' && !entrada.transferida && (
            <TouchableOpacity style={[styles.actionButton, styles.transferButton]} onPress={() => setShowTransfer(true)}>
              <Ionicons name="send-outline" size={20} color={colors.white} />
              <Text style={styles.actionText}>Transferir</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      <Modal visible={showTransfer} transparent animationType="fade">
        <KeyboardAvoidingView style={styles.modalOverlay} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Transferir Entrada</Text>
            <Text style={styles.modalSubtitle}>Ingresá el email del destinatario</Text>
            <TextInput
              style={styles.modalInput}
              placeholder="email@ejemplo.com"
              placeholderTextColor={colors.textMuted}
              value={transferEmail}
              onChangeText={setTransferEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
            <View style={styles.modalActions}>
              <TouchableOpacity style={styles.modalCancel} onPress={() => { setShowTransfer(false); setTransferEmail(''); }}>
                <Text style={styles.modalCancelText}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalConfirm, transferMutation.isPending && { opacity: 0.6 }]}
                onPress={handleTransferir}
                disabled={transferMutation.isPending}
              >
                <Text style={styles.modalConfirmText}>Transferir</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  backButton: { position: 'absolute', top: 60, left: 16, zIndex: 10 },
  content: { flex: 1, alignItems: 'center', padding: 20, paddingTop: 100 },
  eventoNombre: { fontSize: 22, fontWeight: 'bold', color: colors.text, textAlign: 'center', marginBottom: 8 },
  fecha: { color: colors.textSecondary, fontSize: 14, marginBottom: 4 },
  lugar: { color: colors.textSecondary, fontSize: 14, marginBottom: 12 },
  cantidad: { color: colors.primary, fontSize: 15, fontWeight: '600', marginBottom: 24 },
  qrContainer: {
    backgroundColor: colors.white,
    padding: 16,
    borderRadius: 16,
    marginBottom: 16,
  },
  codigo: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 2,
    marginBottom: 12,
  },
  estadoBadge: {
    backgroundColor: colors.success,
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 16,
    marginBottom: 24,
  },
  estadoText: { color: colors.white, fontSize: 12, fontWeight: 'bold', letterSpacing: 1 },
  actionsRow: { flexDirection: 'row', gap: 12, marginTop: 8 },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.cardLight,
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    gap: 8,
  },
  transferButton: { backgroundColor: colors.info },
  actionText: { color: colors.white, fontSize: 14, fontWeight: '500' },
  errorText: { color: colors.textMuted, fontSize: 16, marginBottom: 16 },
  button: { backgroundColor: colors.primary, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  buttonText: { color: colors.white, fontSize: 14, fontWeight: '600' },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.overlay,
  },
  modalContent: {
    backgroundColor: colors.card,
    borderRadius: 16,
    padding: 24,
    width: '85%',
    maxWidth: 400,
  },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: colors.text, marginBottom: 8 },
  modalSubtitle: { color: colors.textSecondary, fontSize: 14, marginBottom: 20 },
  modalInput: {
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 10,
    padding: 14,
    color: colors.text,
    fontSize: 15,
    marginBottom: 20,
  },
  modalActions: { flexDirection: 'row', gap: 12 },
  modalCancel: {
    flex: 1,
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  modalCancelText: { color: colors.textSecondary, fontSize: 15, fontWeight: '500' },
  modalConfirm: {
    flex: 1,
    backgroundColor: colors.primary,
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  modalConfirmText: { color: colors.white, fontSize: 15, fontWeight: '600' },
});

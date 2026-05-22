import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { router } from 'expo-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { entradasApi } from '../../api/entradas';

export default function TransferenciasPendientesScreen() {
  const queryClient = useQueryClient();

  const { data: transfers, isLoading } = useQuery({
    queryKey: ['transferencias-pendientes'],
    queryFn: () => entradasApi.transferenciasPendientes().then((r) => r.data),
  });

  const acceptMutation = useMutation({
    mutationFn: (token: string) => entradasApi.aceptarTransferencia(token),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transferencias-pendientes'] });
      queryClient.invalidateQueries({ queryKey: ['mis-entradas'] });
      Alert.alert('Aceptada', 'Transferencia aceptada correctamente');
    },
    onError: (err: any) => {
      Alert.alert('Error', err.response?.data?.detail || 'Error al aceptar transferencia');
    },
  });

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Transferencias Pendientes</Text>
      <FlatList
        data={transfers || []}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="swap-horizontal" size={24} color={colors.info} />
              <View style={styles.cardInfo}>
                <Text style={styles.eventoNombre}>{item.evento_nombre}</Text>
                <Text style={styles.emailText}>De: {item.email}</Text>
              </View>
            </View>
            <TouchableOpacity
              style={[styles.acceptButton, acceptMutation.isPending && { opacity: 0.6 }]}
              onPress={() => acceptMutation.mutate(item.token)}
              disabled={acceptMutation.isPending}
            >
              <Ionicons name="checkmark" size={20} color={colors.white} />
              <Text style={styles.acceptText}>Aceptar</Text>
            </TouchableOpacity>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="swap-horizontal-outline" size={48} color={colors.textMuted} />
            <Text style={styles.emptyText}>No tenés transferencias pendientes</Text>
          </View>
        }
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  back: { padding: 16, paddingTop: 60, paddingBottom: 0 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, paddingHorizontal: 16, marginBottom: 16 },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 12 },
  cardInfo: { flex: 1 },
  eventoNombre: { color: colors.text, fontSize: 15, fontWeight: '600' },
  emailText: { color: colors.textSecondary, fontSize: 13, marginTop: 2 },
  acceptButton: {
    flexDirection: 'row',
    backgroundColor: colors.success,
    padding: 12,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  acceptText: { color: colors.white, fontSize: 14, fontWeight: '600' },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { color: colors.textMuted, fontSize: 16, marginTop: 12 },
});

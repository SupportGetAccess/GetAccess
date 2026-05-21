import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { entradasApi } from '../../api/entradas';
import { colors } from '../../theme';
import { useAuthStore } from '../../stores/authStore';
import { formatPrecio, parseFecha } from '../../utils/format';

export default function MisEntradasScreen() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const { data: entradas, isLoading } = useQuery({
    queryKey: ['mis-entradas'],
    queryFn: () => entradasApi.listar().then((r) => r.data),
    enabled: isAuthenticated,
  });

  if (!isAuthenticated) {
    return (
      <View style={styles.center}>
        <Ionicons name="lock-closed" size={48} color={colors.textMuted} />
        <Text style={styles.title}>Mis Entradas</Text>
        <Text style={styles.subtitle}>Iniciá sesión para ver tus entradas</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/(auth)/login')}>
          <Text style={styles.buttonText}>Iniciar Sesión</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.linkButton} onPress={() => router.push('/buscar-entradas')}>
          <Text style={styles.linkText}>Buscar por email</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  const pagadas = (entradas || []).filter((e) => e.estado === 'pagada');
  const pendientes = (entradas || []).filter((e) => e.estado === 'pendiente');

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mis Entradas</Text>
      </View>
      {pendientes.length > 0 && (
        <View style={styles.pendientesBanner}>
          <Ionicons name="alert-circle" size={20} color={colors.warning} />
          <Text style={styles.pendientesText}>{pendientes.length} pendiente(s) de pago</Text>
        </View>
      )}
      <FlatList
        data={pagadas}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.card}
            onPress={() => router.push(`/entrada/${item.id}`)}
            activeOpacity={0.7}
          >
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle} numberOfLines={1}>{item.evento_nombre || `Entrada #${item.id}`}</Text>
              <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
            </View>
            <Text style={styles.cardCode}>{item.preference_id}</Text>
            <View style={styles.cardMeta}>
              <Text style={styles.cardMetaText}>{item.cantidad} entrada(s)</Text>
              <Text style={styles.cardPrecio}>{formatPrecio(item.total)}</Text>
            </View>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="ticket-outline" size={48} color={colors.textMuted} />
            <Text style={styles.emptyText}>No tenés entradas aún</Text>
          </View>
        }
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  header: { paddingHorizontal: 16, paddingTop: 60, paddingBottom: 16, backgroundColor: colors.backgroundLight },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text },
  subtitle: { color: colors.textSecondary, marginTop: 8, fontSize: 14, textAlign: 'center' },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  cardTitle: { fontSize: 16, fontWeight: '600', color: colors.text, flex: 1 },
  cardCode: { color: colors.primary, fontSize: 14, fontWeight: 'bold', marginBottom: 8, letterSpacing: 1 },
  cardMeta: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  cardMetaText: { color: colors.textSecondary, fontSize: 13 },
  cardPrecio: { color: colors.success, fontSize: 14, fontWeight: 'bold' },
  pendientesBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#3a3000',
    padding: 12,
    marginHorizontal: 12,
    marginTop: 12,
    borderRadius: 8,
    gap: 8,
  },
  pendientesText: { color: colors.warning, fontSize: 13 },
  button: {
    backgroundColor: colors.primary,
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: '600' },
  linkButton: { marginTop: 12 },
  linkText: { color: colors.primary, fontSize: 14 },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { color: colors.textMuted, fontSize: 16, marginTop: 12 },
});

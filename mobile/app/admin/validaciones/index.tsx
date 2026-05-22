import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { adminApi, Validacion } from '../../../api/admin';
import { parseFecha } from '../../../utils/format';

export default function ValidacionesScreen() {
  const { data: validaciones, isLoading } = useQuery({
    queryKey: ['validaciones'],
    queryFn: () => adminApi.validaciones().then((r) => r.data),
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
      <Text style={styles.title}>Validaciones</Text>
      <Text style={styles.subtitle}>Últimos 7 días</Text>
      <FlatList
        data={validaciones || []}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="scan" size={22} color={colors.success} />
              <View style={styles.cardInfo}>
                <Text style={styles.eventoNombre}>{item.evento_nombre}</Text>
                <Text style={styles.scannerName}>Escaneado por: {item.scanner}</Text>
              </View>
            </View>
            <View style={styles.cardMeta}>
              <Ionicons name="time-outline" size={14} color={colors.textSecondary} />
              <Text style={styles.metaText}>{parseFecha(item.timestamp)}</Text>
            </View>
            <Text style={styles.entradaId}>Entrada #{item.entrada_id}</Text>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="scan-outline" size={48} color={colors.textMuted} />
            <Text style={styles.emptyText}>No hay validaciones en los últimos 7 días</Text>
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
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, paddingHorizontal: 16 },
  subtitle: { color: colors.textSecondary, fontSize: 13, paddingHorizontal: 16, marginBottom: 16, marginTop: 4 },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 8 },
  cardInfo: { flex: 1 },
  eventoNombre: { color: colors.text, fontSize: 15, fontWeight: '600' },
  scannerName: { color: colors.textSecondary, fontSize: 12, marginTop: 2 },
  cardMeta: { flexDirection: 'row', alignItems: 'center', gap: 4, marginBottom: 4 },
  metaText: { color: colors.textSecondary, fontSize: 12 },
  entradaId: { color: colors.primary, fontSize: 12, fontWeight: '500' },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { color: colors.textMuted, fontSize: 16, marginTop: 12 },
});

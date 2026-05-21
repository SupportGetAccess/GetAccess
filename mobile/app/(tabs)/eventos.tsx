import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { eventosApi } from '../../api/eventos';
import { colors } from '../../theme';
import { formatPrecio, parseFechaCorta } from '../../utils/format';
import { Evento } from '../../types';

function EventoCard({ evento }: { evento: Evento }) {
  const disponibles = evento.capacidad - evento.vendidos;
  const agotado = disponibles <= 0;

  return (
    <TouchableOpacity
      style={[styles.card, agotado && styles.cardAgotado]}
      onPress={() => router.push(`/evento/${evento.id}`)}
      activeOpacity={0.7}
    >
      <View style={styles.cardContent}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardTitle} numberOfLines={2}>{evento.nombre}</Text>
          <Text style={styles.cardPrecio}>{formatPrecio(evento.precio)}</Text>
        </View>
        <View style={styles.cardMeta}>
          <Ionicons name="calendar-outline" size={14} color={colors.textSecondary} />
          <Text style={styles.cardMetaText}>{parseFechaCorta(evento.fecha)}</Text>
          <Ionicons name="location-outline" size={14} color={colors.textSecondary} style={{ marginLeft: 12 }} />
          <Text style={styles.cardMetaText} numberOfLines={1}>{evento.lugar}</Text>
        </View>
        <View style={styles.cardFooter}>
          {agotado ? (
            <Text style={styles.agotadoTag}>AGOTADO</Text>
          ) : (
            <Text style={styles.disponiblesText}>{disponibles} disponibles</Text>
          )}
          {evento.categoria && (
            <View style={styles.categoriaTag}>
              <Text style={styles.categoriaText}>{evento.categoria}</Text>
            </View>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
}

export default function EventosScreen() {
  const { data: eventos, isLoading, error } = useQuery({
    queryKey: ['eventos'],
    queryFn: () => eventosApi.listar().then((r) => r.data),
  });

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Ionicons name="cloud-offline" size={48} color={colors.textMuted} />
        <Text style={styles.errorText}>Error al cargar eventos</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Get Access</Text>
        <TouchableOpacity onPress={() => router.push('/(auth)/login')}>
          <Ionicons name="person-circle-outline" size={28} color={colors.primary} />
        </TouchableOpacity>
      </View>
      <FlatList
        data={eventos || []}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => <EventoCard evento={item} />}
        contentContainerStyle={styles.list}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 60,
    paddingBottom: 16,
    backgroundColor: colors.backgroundLight,
  },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.primary },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    marginBottom: 12,
    overflow: 'hidden',
  },
  cardAgotado: { opacity: 0.6 },
  cardContent: { padding: 16 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 },
  cardTitle: { flex: 1, fontSize: 16, fontWeight: '600', color: colors.text, marginRight: 8 },
  cardPrecio: { fontSize: 16, fontWeight: 'bold', color: colors.primary },
  cardMeta: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  cardMetaText: { color: colors.textSecondary, fontSize: 13, marginLeft: 4 },
  cardFooter: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  agotadoTag: {
    backgroundColor: colors.error,
    color: colors.white,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    fontSize: 11,
    fontWeight: 'bold',
    overflow: 'hidden',
  },
  disponiblesText: { color: colors.success, fontSize: 12 },
  categoriaTag: {
    backgroundColor: colors.cardLight,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  categoriaText: { color: colors.textSecondary, fontSize: 11 },
  errorText: { color: colors.textMuted, marginTop: 12, fontSize: 16 },
});

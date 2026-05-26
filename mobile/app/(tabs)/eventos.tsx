import { useState, useCallback, useMemo } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, Image, RefreshControl } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { eventosApi } from '../../api/eventos';
import { colors } from '../../theme';
import { formatPrecio, parseFechaCorta, getImageUrl, isEventoFinalizado } from '../../utils/format';
import { Evento } from '../../types';
import { useAuthStore } from '../../stores/authStore';

function EventoCard({ evento }: { evento: Evento }) {
  const disponibles = evento.capacidad - evento.vendidos;
  const agotado = disponibles <= 0;
  const finalizado = isEventoFinalizado(evento.fecha);
  const imageUrl = getImageUrl(evento.imagen);

  return (
    <TouchableOpacity
      style={[styles.card, (agotado || finalizado) && styles.cardAgotado]}
      onPress={() => router.push(`/evento/${evento.id}`)}
      activeOpacity={0.7}
    >
      {imageUrl && (
        <Image source={{ uri: imageUrl }} style={styles.cardImage} resizeMode="cover" />
      )}
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
          {finalizado ? (
            <Text style={styles.finalizadoTag}>FINALIZADO</Text>
          ) : agotado ? (
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
  const [refreshing, setRefreshing] = useState(false);
  const { data: eventos, isLoading, error, refetch } = useQuery({
    queryKey: ['eventos'],
    queryFn: () => eventosApi.listar().then((r) => r.data),
  });

  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const eventosOrdenados = useMemo(
    () => (eventos ? [...eventos].sort((a, b) => {
      const fa = new Date(a.fecha).getTime();
      const fb = new Date(b.fecha).getTime();
      const ahora = Date.now();
      const aPasado = fa < ahora;
      const bPasado = fb < ahora;
      if (aPasado !== bPasado) return aPasado ? 1 : -1;
      return fa - fb;
    }) : []),
    [eventos],
  );

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  }, [refetch]);

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
        <View style={styles.headerLeft}>
          <Image source={require('../../Logo PNG transparencia.png')} style={styles.logo} resizeMode="contain" />
          <Text style={styles.title}>GET ACCESS</Text>
        </View>
        <TouchableOpacity onPress={() => router.push(isAuthenticated ? '/(tabs)/perfil' : '/(auth)/login')}>
          <Text style={{ fontSize: 24 }}>👤</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={eventosOrdenados}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => <EventoCard evento={item} />}
        contentContainerStyle={styles.list}
        showsVerticalScrollIndicator={false}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
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
    backgroundColor: 'rgba(30, 30, 63, 0.85)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(99, 102, 241, 0.2)',
  },
  headerLeft: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  logo: { width: 28, height: 28 },
  title: { fontSize: 24, fontWeight: '800', color: '#6366f1', letterSpacing: -0.5 },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    marginBottom: 12,
    overflow: 'hidden',
  },
  cardAgotado: { opacity: 0.6 },
  cardImage: { width: '100%', height: 140 },
  cardContent: { padding: 16 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 },
  cardTitle: { flex: 1, fontSize: 16, fontWeight: '600', color: colors.text, marginRight: 8 },
  cardPrecio: { fontSize: 16, fontWeight: 'bold', color: colors.primary },
  cardMeta: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  cardMetaText: { color: colors.textSecondary, fontSize: 13, marginLeft: 4 },
  cardFooter: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  finalizadoTag: {
    backgroundColor: colors.textMuted,
    color: colors.white,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    fontSize: 11,
    fontWeight: 'bold',
    overflow: 'hidden',
  },
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

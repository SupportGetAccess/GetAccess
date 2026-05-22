import { View, Text, ScrollView, TouchableOpacity, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import { useState, useCallback } from 'react';
import { router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { adminApi } from '../../../api/admin';
import { formatPrecio } from '../../../utils/format';

export default function DashboardScreen() {
  const [refreshing, setRefreshing] = useState(false);

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['admin-dashboard'],
    queryFn: () => adminApi.dashboard().then((r) => r.data),
  });

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  }, []);

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  const cards = [
    { icon: 'ticket', label: 'Entradas Vendidas', value: String(data?.ventas_total ?? 0), color: colors.primary },
    { icon: 'cash', label: 'Ingresos Totales', value: formatPrecio(data?.ingresos_total ?? 0), color: colors.success },
    { icon: 'checkmark-circle', label: 'Tickets Usados', value: String(data?.tickets_usados ?? 0), color: colors.info },
    { icon: 'trending-up', label: 'Ticket Promedio', value: formatPrecio(data?.precio_promedio ?? 0), color: colors.warning },
  ];

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
    >
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Dashboard</Text>
      <View style={styles.cardsGrid}>
        {cards.map((card) => (
          <View key={card.label} style={styles.card}>
            <Ionicons name={card.icon as any} size={28} color={card.color} />
            <Text style={styles.cardValue}>{card.value}</Text>
            <Text style={styles.cardLabel}>{card.label}</Text>
          </View>
        ))}
      </View>
      {data?.proyeccion && (
        <View style={styles.proyeccionCard}>
          <Ionicons name="analytics" size={22} color={colors.primary} />
          <View style={styles.proyeccionContent}>
            <Text style={styles.proyeccionLabel}>Tendencia: <Text style={{ color: colors.primary }}>{data.proyeccion.tendencia}</Text></Text>
            <Text style={styles.proyeccionLabel}>Probabilidad de agotar: {data.proyeccion.probabilidad_agotar}%</Text>
          </View>
        </View>
      )}
      {data?.top_eventos && data.top_eventos.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Top Eventos</Text>
          {data.top_eventos.map((ev, i) => (
            <View key={ev.id} style={styles.topRow}>
              <Text style={styles.topPos}>#{i + 1}</Text>
              <View style={styles.topInfo}>
                <Text style={styles.topNombre} numberOfLines={1}>{ev.nombre}</Text>
                <Text style={styles.topMeta}>{ev.vendidos} vendidos · {formatPrecio(ev.ingresos)}</Text>
              </View>
            </View>
          ))}
        </View>
      )}
      {data?.por_categoria && data.por_categoria.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Por Categoría</Text>
          {data.por_categoria.map((cat) => (
            <View key={cat.categoria} style={styles.catRow}>
              <Text style={styles.catNombre}>{cat.categoria}</Text>
              <Text style={styles.catCantidad}>{cat.cantidad} entradas</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  back: { marginBottom: 12 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  cardsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 20 },
  card: {
    width: '47%',
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    gap: 8,
  },
  cardValue: { fontSize: 20, fontWeight: 'bold', color: colors.text },
  cardLabel: { fontSize: 12, color: colors.textSecondary, textAlign: 'center' },
  proyeccionCard: {
    flexDirection: 'row',
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    gap: 12,
    alignItems: 'center',
  },
  proyeccionContent: { flex: 1, gap: 4 },
  proyeccionLabel: { color: colors.textSecondary, fontSize: 13 },
  section: { marginBottom: 20 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: 12 },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.card,
    borderRadius: 10,
    padding: 12,
    marginBottom: 8,
    gap: 12,
  },
  topPos: { color: colors.primary, fontSize: 16, fontWeight: 'bold', width: 28 },
  topInfo: { flex: 1 },
  topNombre: { color: colors.text, fontSize: 14, fontWeight: '500' },
  topMeta: { color: colors.textSecondary, fontSize: 12, marginTop: 2 },
  catRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: colors.card,
    borderRadius: 10,
    padding: 12,
    marginBottom: 6,
  },
  catNombre: { color: colors.text, fontSize: 14 },
  catCantidad: { color: colors.primary, fontSize: 14, fontWeight: '600' },
});

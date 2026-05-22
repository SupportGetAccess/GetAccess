import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { router } from 'expo-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { eventosApi } from '../../../api/eventos';
import { formatPrecio, parseFechaCorta } from '../../../utils/format';
import { Evento } from '../../../types';

export default function MisEventosScreen() {
  const queryClient = useQueryClient();

  const { data: eventos, isLoading } = useQuery({
    queryKey: ['mis-eventos-admin'],
    queryFn: () => eventosApi.listar({ mis_eventos: true }).then((r) => r.data),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => eventosApi.eliminar(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mis-eventos-admin'] });
    },
  });

  const handleDelete = (evento: Evento) => {
    Alert.alert('Eliminar Evento', `¿Eliminar "${evento.nombre}"?`, [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Eliminar', style: 'destructive', onPress: () => deleteMutation.mutate(evento.id) },
    ]);
  };

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
      <Text style={styles.title}>Mis Eventos</Text>
      <FlatList
        data={eventos || []}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle} numberOfLines={2}>{item.nombre}</Text>
              <View style={styles.cardActions}>
                <TouchableOpacity onPress={() => router.push(`/admin/crear-evento?id=${item.id}`)}>
                  <Ionicons name="create-outline" size={22} color={colors.primary} />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => handleDelete(item)}>
                  <Ionicons name="trash-outline" size={22} color={colors.error} />
                </TouchableOpacity>
              </View>
            </View>
            <View style={styles.cardMeta}>
              <Ionicons name="calendar-outline" size={14} color={colors.textSecondary} />
              <Text style={styles.metaText}>{parseFechaCorta(item.fecha)}</Text>
              <Ionicons name="location-outline" size={14} color={colors.textSecondary} style={{ marginLeft: 10 }} />
              <Text style={styles.metaText} numberOfLines={1}>{item.lugar}</Text>
            </View>
            <View style={styles.cardFooter}>
              <Text style={styles.precio}>{formatPrecio(item.precio)}</Text>
              <Text style={styles.vendidos}>{item.vendidos} / {item.capacidad} vendidos</Text>
            </View>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Ionicons name="calendar-outline" size={48} color={colors.textMuted} />
            <Text style={styles.emptyText}>No tenés eventos creados</Text>
            <TouchableOpacity style={styles.createButton} onPress={() => router.push('/admin/crear-evento')}>
              <Text style={styles.createText}>Crear Evento</Text>
            </TouchableOpacity>
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
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, paddingHorizontal: 16, paddingBottom: 16 },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  cardTitle: { flex: 1, fontSize: 16, fontWeight: '600', color: colors.text, marginRight: 12 },
  cardActions: { flexDirection: 'row', gap: 12, alignItems: 'center' },
  cardMeta: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  metaText: { color: colors.textSecondary, fontSize: 13, marginLeft: 4 },
  cardFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  precio: { color: colors.primary, fontSize: 16, fontWeight: 'bold' },
  vendidos: { color: colors.textSecondary, fontSize: 13 },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { color: colors.textMuted, fontSize: 16, marginTop: 12, marginBottom: 20 },
  createButton: { backgroundColor: colors.primary, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  createText: { color: colors.white, fontSize: 14, fontWeight: '600' },
});

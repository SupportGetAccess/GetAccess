import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { router } from 'expo-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { adminApi, SolicitudOrganizer } from '../../../api/admin';

export default function SolicitudesScreen() {
  const queryClient = useQueryClient();

  const { data: solicitudes, isLoading } = useQuery({
    queryKey: ['solicitudes-organizer'],
    queryFn: () => adminApi.solicitudes().then((r) => r.data),
  });

  const aprobarMutation = useMutation({
    mutationFn: (id: number) => adminApi.aprobarOrganizer(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['solicitudes-organizer'] }),
  });

  const rechazarMutation = useMutation({
    mutationFn: (id: number) => adminApi.rechazarOrganizer(id, 'Solicitud rechazada'),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['solicitudes-organizer'] }),
  });

  const handleAprobar = (s: SolicitudOrganizer) => {
    Alert.alert('Aprobar', `¿Aprobar a ${s.nombre} ${s.apellido} como organizador?`, [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Aprobar', onPress: () => aprobarMutation.mutate(s.id) },
    ]);
  };

  const handleRechazar = (s: SolicitudOrganizer) => {
    Alert.alert('Rechazar', `¿Rechazar a ${s.nombre} ${s.apellido}?`, [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Rechazar', style: 'destructive', onPress: () => rechazarMutation.mutate(s.id) },
    ]);
  };

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  const pendientes = (solicitudes || []).filter((s) => s.estado === 'pendiente');
  const resueltas = (solicitudes || []).filter((s) => s.estado !== 'pendiente');

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Solicitudes</Text>
      {pendientes.length === 0 ? (
        <Text style={styles.emptyText}>No hay solicitudes pendientes</Text>
      ) : (
        <FlatList
          data={pendientes}
          keyExtractor={(item) => String(item.id)}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="person-circle" size={32} color={colors.primary} />
                <View style={styles.cardInfo}>
                  <Text style={styles.cardName}>{item.nombre} {item.apellido}</Text>
                  <Text style={styles.cardEmail}>{item.email}</Text>
                </View>
              </View>
              <View style={styles.cardActions}>
                <TouchableOpacity style={styles.aprobarBtn} onPress={() => handleAprobar(item)}>
                  <Ionicons name="checkmark" size={20} color={colors.white} />
                  <Text style={styles.btnText}>Aprobar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.rechazarBtn} onPress={() => handleRechazar(item)}>
                  <Ionicons name="close" size={20} color={colors.white} />
                  <Text style={styles.btnText}>Rechazar</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
          ListHeaderComponent={() => (
            pendientes.length > 0 ? <Text style={styles.sectionTitle}>{pendientes.length} pendiente(s)</Text> : null
          )}
          ListFooterComponent={() =>
            resueltas.length > 0 ? (
              <View style={{ marginTop: 24 }}>
                <Text style={styles.sectionTitle}>Resueltas</Text>
                {resueltas.map((item) => (
                  <View key={item.id} style={[styles.card, styles.cardResuelta]}>
                    <View style={styles.cardHeader}>
                      <Ionicons name="person-circle" size={28} color={colors.textMuted} />
                      <View style={styles.cardInfo}>
                        <Text style={[styles.cardName, { color: colors.textMuted }]}>{item.nombre} {item.apellido}</Text>
                        <Text style={styles.cardEmail}>{item.email}</Text>
                        <Text style={[styles.estadoTag, item.estado === 'aprobado' ? styles.aprobado : styles.rechazado]}>
                          {item.estado.toUpperCase()}
                        </Text>
                      </View>
                    </View>
                  </View>
                ))}
              </View>
            ) : null
          }
          contentContainerStyle={styles.list}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  back: { padding: 16, paddingTop: 60, paddingBottom: 0 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, paddingHorizontal: 16, paddingBottom: 16 },
  sectionTitle: { fontSize: 16, fontWeight: '600', color: colors.text, marginBottom: 12 },
  list: { padding: 12, paddingBottom: 40 },
  emptyText: { color: colors.textMuted, fontSize: 14, textAlign: 'center', marginTop: 40 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
  },
  cardResuelta: { opacity: 0.6 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 12 },
  cardInfo: { flex: 1 },
  cardName: { color: colors.text, fontSize: 15, fontWeight: '600' },
  cardEmail: { color: colors.textSecondary, fontSize: 13, marginTop: 2 },
  cardActions: { flexDirection: 'row', gap: 10 },
  aprobarBtn: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: colors.success,
    padding: 10,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  rechazarBtn: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: colors.error,
    padding: 10,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  btnText: { color: colors.white, fontSize: 14, fontWeight: '600' },
  estadoTag: { fontSize: 11, fontWeight: 'bold', marginTop: 4 },
  aprobado: { color: colors.success },
  rechazado: { color: colors.error },
});

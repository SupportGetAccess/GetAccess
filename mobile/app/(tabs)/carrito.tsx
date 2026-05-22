import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { useCartStore } from '../../stores/cartStore';
import { formatPrecio } from '../../utils/format';

export default function CarritoTab() {
  const items = useCartStore((s) => s.items);
  const total = useCartStore((s) => s.total);

  if (items.length === 0) {
    return (
      <View style={styles.center}>
        <Ionicons name="cart-outline" size={64} color={colors.textMuted} />
        <Text style={styles.title}>Carrito</Text>
        <Text style={styles.subtitle}>Agregá entradas desde un evento</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/(tabs)/eventos')}>
          <Text style={styles.buttonText}>Ver Eventos</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Carrito</Text>
        <Text style={styles.totalText}>Total: {formatPrecio(total)}</Text>
      </View>
      <FlatList
        data={items}
        keyExtractor={(item) => String(item.evento.id)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.cardRow}>
              <Text style={styles.cardTitle} numberOfLines={1}>{item.evento.nombre}</Text>
              <TouchableOpacity onPress={() => useCartStore.getState().removeItem(item.evento.id)}>
                <Ionicons name="trash-outline" size={20} color={colors.error} />
              </TouchableOpacity>
            </View>
            <View style={styles.cardRow}>
              <Text style={styles.cardPrecio}>{formatPrecio(item.evento.precio)} c/u</Text>
              <View style={styles.cantidadRow}>
                <TouchableOpacity
                  onPress={() => {
                    if (item.cantidad > 1) {
                      useCartStore.getState().updateCantidad(item.evento.id, item.cantidad - 1);
                    }
                  }}
                  style={styles.qtyBtn}
                >
                  <Ionicons name="remove" size={16} color={colors.text} />
                </TouchableOpacity>
                <Text style={styles.qtyText}>{item.cantidad}</Text>
                <TouchableOpacity
                  onPress={() => useCartStore.getState().updateCantidad(item.evento.id, item.cantidad + 1)}
                  style={styles.qtyBtn}
                >
                  <Ionicons name="add" size={16} color={colors.text} />
                </TouchableOpacity>
              </View>
            </View>
          </View>
        )}
        contentContainerStyle={styles.list}
      />
      <View style={styles.footer}>
        <TouchableOpacity
          style={styles.pagarButton}
          onPress={() => router.push('/checkout')}
        >
          <Text style={styles.pagarText}>Continuar al Pago</Text>
          <Ionicons name="arrow-forward" size={20} color={colors.white} />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 60,
    paddingBottom: 16,
    backgroundColor: colors.backgroundLight,
  },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text },
  totalText: { color: colors.primary, fontSize: 16, fontWeight: 'bold' },
  subtitle: { color: colors.textSecondary, marginTop: 8, fontSize: 14, textAlign: 'center' },
  list: { padding: 12 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  cardRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  cardTitle: { fontSize: 16, fontWeight: '600', color: colors.text, flex: 1 },
  cardPrecio: { color: colors.primary, fontSize: 14 },
  cantidadRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  qtyBtn: {
    backgroundColor: colors.cardLight,
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  qtyText: { color: colors.text, fontSize: 16, fontWeight: '600', minWidth: 20, textAlign: 'center' },
  footer: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    backgroundColor: colors.backgroundLight,
  },
  pagarButton: {
    backgroundColor: colors.primary,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  pagarText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
  button: {
    backgroundColor: colors.primary,
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: '600' },
});

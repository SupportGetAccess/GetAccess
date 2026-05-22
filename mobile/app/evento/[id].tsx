import { View, Text, TouchableOpacity, StyleSheet, ScrollView, ActivityIndicator, Alert, Image, Dimensions, SafeAreaView } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { useRef, useState } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { eventosApi } from '../../api/eventos';
import { colors } from '../../theme';
import { formatPrecio, parseFecha, getImageUrl, isEventoFinalizado } from '../../utils/format';
import { useCartStore } from '../../stores/cartStore';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const IMAGE_HEIGHT = 200;

export default function EventoDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [cantidad, setCantidad] = useState(1);
  const [imgIndex, setImgIndex] = useState(0);
  const scrollRef = useRef<ScrollView>(null);
  const addItem = useCartStore((s) => s.addItem);

  const { data: evento, isLoading } = useQuery({
    queryKey: ['evento', id],
    queryFn: () => eventosApi.obtener(Number(id)).then((r) => r.data),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!evento) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>Evento no encontrado</Text>
      </View>
    );
  }

  const imagenes = [
    ...(evento.imagenes?.length ? evento.imagenes.map((i) => i.url) : []),
    ...(getImageUrl(evento.imagen) ? [getImageUrl(evento.imagen)!] : []),
  ];

  const disponibles = evento.capacidad - evento.vendidos;
  const agotado = disponibles <= 0;
  const finalizado = isEventoFinalizado(evento.fecha);
  const precioConComision = evento.precio * (1 + (evento.comision || 0) / 100);
  const total = precioConComision * cantidad;

  const handleAgregar = () => {
    addItem({ evento, cantidad });
    Alert.alert('Agregado', `${cantidad} entrada(s) agregada(s) al carrito`, [
      { text: 'Seguir viendo', style: 'cancel' },
      { text: 'Ir al Carrito', onPress: () => router.push('/(tabs)/carrito') },
    ]);
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <ScrollView style={styles.scroll} contentContainerStyle={styles.content}>
        {imagenes.length > 0 ? (
          <View>
            <ScrollView
              ref={scrollRef}
              horizontal
              pagingEnabled
              showsHorizontalScrollIndicator={false}
              onMomentumScrollEnd={(e) => {
                const idx = Math.round(e.nativeEvent.contentOffset.x / SCREEN_WIDTH);
                setImgIndex(idx);
              }}
            >
              {imagenes.map((url, i) => (
                <Image key={i} source={{ uri: url }} style={[styles.image, { width: SCREEN_WIDTH - 32 }]} resizeMode="cover" />
              ))}
            </ScrollView>
            {imagenes.length > 1 && (
              <View style={styles.dotsRow}>
                {imagenes.map((_, i) => (
                  <View key={i} style={[styles.dot, i === imgIndex && styles.dotActive]} />
                ))}
              </View>
            )}
          </View>
        ) : (
          <View style={styles.imagePlaceholder}>
            <Ionicons name="calendar" size={48} color={colors.textMuted} />
          </View>
        )}
        <Text style={styles.nombre}>{evento.nombre}</Text>
        {evento.categoria && (
          <View style={styles.categoriaBadge}>
            <Text style={styles.categoriaText}>{evento.categoria}</Text>
          </View>
        )}
        <View style={styles.metaSection}>
          <View style={styles.metaRow}>
            <Ionicons name="calendar-outline" size={18} color={colors.primary} />
            <Text style={styles.metaText}>{parseFecha(evento.fecha)}</Text>
          </View>
          <View style={styles.metaRow}>
            <Ionicons name="location-outline" size={18} color={colors.primary} />
            <Text style={styles.metaText}>{evento.lugar}</Text>
          </View>
          <View style={styles.metaRow}>
            <Ionicons name="pricetag-outline" size={18} color={colors.primary} />
            <Text style={styles.metaText}>{formatPrecio(evento.precio)} por persona</Text>
          </View>
        </View>
        {evento.descripcion && (
          <Text style={styles.descripcion}>{evento.descripcion}</Text>
        )}
        {finalizado ? (
          <View style={styles.finalizadoBanner}>
            <Ionicons name="flag" size={20} color={colors.textSecondary} />
            <Text style={styles.finalizadoText}>Evento finalizado</Text>
          </View>
        ) : agotado ? (
          <View style={styles.agotadoBanner}>
            <Ionicons name="close-circle" size={20} color={colors.error} />
            <Text style={styles.agotadoText}>Entradas agotadas</Text>
          </View>
        ) : (
          <Text style={styles.disponibles}>{disponibles} disponibles</Text>
        )}
      </ScrollView>
      {!agotado && !finalizado && (
        <SafeAreaView style={styles.footer}>
          <View style={styles.cantidadRow}>
            <TouchableOpacity onPress={() => setCantidad(Math.max(1, cantidad - 1))} style={styles.qtyBtn}>
              <Ionicons name="remove" size={20} color={colors.text} />
            </TouchableOpacity>
            <Text style={styles.qtyText}>{cantidad}</Text>
            <TouchableOpacity onPress={() => setCantidad(Math.min(disponibles, cantidad + 1))} style={styles.qtyBtn}>
              <Ionicons name="add" size={20} color={colors.text} />
            </TouchableOpacity>
          </View>
          <TouchableOpacity style={styles.addButton} onPress={handleAgregar}>
            <Text style={styles.addText}>Agregar · {formatPrecio(total)}</Text>
          </TouchableOpacity>
        </SafeAreaView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  scroll: { flex: 1 },
  content: { padding: 16, paddingTop: 100 },
  backButton: { position: 'absolute', top: 60, left: 16, zIndex: 10 },
  imagePlaceholder: {
    height: 200,
    backgroundColor: colors.card,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  image: { width: '100%', height: IMAGE_HEIGHT, borderRadius: 12, marginBottom: 0 },
  dotsRow: { flexDirection: 'row', justifyContent: 'center', gap: 6, marginTop: 8, marginBottom: 20 },
  dot: { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.border },
  dotActive: { backgroundColor: colors.primary, width: 10, height: 10, borderRadius: 5 },
  nombre: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginBottom: 8 },
  categoriaBadge: {
    alignSelf: 'flex-start',
    backgroundColor: colors.cardLight,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    marginBottom: 16,
  },
  categoriaText: { color: colors.primary, fontSize: 12, fontWeight: '500' },
  metaSection: { gap: 10, marginBottom: 20 },
  metaRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  metaText: { color: colors.textSecondary, fontSize: 14, flex: 1 },
  descripcion: { color: colors.textSecondary, fontSize: 14, lineHeight: 22, marginBottom: 20 },
  agotadoBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2a0000',
    padding: 14,
    borderRadius: 10,
    gap: 8,
  },
  agotadoText: { color: colors.error, fontSize: 14, fontWeight: '600' },
  finalizadoBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.cardLight,
    padding: 14,
    borderRadius: 10,
    gap: 8,
  },
  finalizadoText: { color: colors.textSecondary, fontSize: 14, fontWeight: '600' },
  disponibles: { color: colors.success, fontSize: 14, fontWeight: '500', marginBottom: 20 },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    backgroundColor: colors.backgroundLight,
    gap: 12,
  },
  cantidadRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  qtyBtn: {
    backgroundColor: colors.cardLight,
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  qtyText: { color: colors.text, fontSize: 18, fontWeight: 'bold', minWidth: 24, textAlign: 'center' },
  addButton: {
    flex: 1,
    backgroundColor: colors.primary,
    padding: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  addText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
  errorText: { color: colors.textMuted, fontSize: 16 },
});

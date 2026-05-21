import { View, Text, TouchableOpacity, StyleSheet, Share } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import QRCode from 'react-native-qrcode-svg';
import { entradasApi } from '../../api/entradas';
import { colors } from '../../theme';
import { formatPrecio, parseFecha } from '../../utils/format';

export default function EntradaDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: entrada } = useQuery({
    queryKey: ['entrada', id],
    queryFn: async () => {
      const res = await entradasApi.listar();
      return res.data.find((e) => e.id === Number(id));
    },
    enabled: !!id,
  });

  if (!entrada) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>Entrada no encontrada</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.back()}>
          <Text style={styles.buttonText}>Volver</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleCompartir = async () => {
    try {
      await Share.share({
        message: `Get Access - Entrada: ${entrada.preference_id}`,
      });
    } catch {}
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <View style={styles.content}>
        <Text style={styles.eventoNombre}>{entrada.evento_nombre || `Entrada #${entrada.id}`}</Text>
        {entrada.evento_fecha && <Text style={styles.fecha}>{parseFecha(entrada.evento_fecha)}</Text>}
        {entrada.evento_lugar && <Text style={styles.lugar}>{entrada.evento_lugar}</Text>}
        <Text style={styles.cantidad}>{entrada.cantidad} entrada(s) · {formatPrecio(entrada.total)}</Text>
        <View style={styles.qrContainer}>
          {entrada.preference_id ? (
            <QRCode
              value={entrada.preference_id}
              size={220}
              backgroundColor={colors.white}
              color={colors.black}
            />
          ) : (
            <Ionicons name="qr-code" size={120} color={colors.textMuted} />
          )}
        </View>
        <Text style={styles.codigo}>{entrada.preference_id}</Text>
        <View style={styles.estadoBadge}>
          <Text style={styles.estadoText}>{entrada.estado.toUpperCase()}</Text>
        </View>
        <TouchableOpacity style={styles.compartirButton} onPress={handleCompartir}>
          <Ionicons name="share-outline" size={20} color={colors.white} />
          <Text style={styles.compartirText}>Compartir</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  backButton: { position: 'absolute', top: 60, left: 16, zIndex: 10 },
  content: { flex: 1, alignItems: 'center', padding: 20, paddingTop: 100 },
  eventoNombre: { fontSize: 22, fontWeight: 'bold', color: colors.text, textAlign: 'center', marginBottom: 8 },
  fecha: { color: colors.textSecondary, fontSize: 14, marginBottom: 4 },
  lugar: { color: colors.textSecondary, fontSize: 14, marginBottom: 12 },
  cantidad: { color: colors.primary, fontSize: 15, fontWeight: '600', marginBottom: 24 },
  qrContainer: {
    backgroundColor: colors.white,
    padding: 16,
    borderRadius: 16,
    marginBottom: 16,
  },
  codigo: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 2,
    marginBottom: 12,
  },
  estadoBadge: {
    backgroundColor: colors.success,
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 16,
    marginBottom: 24,
  },
  estadoText: { color: colors.white, fontSize: 12, fontWeight: 'bold', letterSpacing: 1 },
  compartirButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.cardLight,
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    gap: 8,
  },
  compartirText: { color: colors.white, fontSize: 14, fontWeight: '500' },
  errorText: { color: colors.textMuted, fontSize: 16, marginBottom: 16 },
  button: { backgroundColor: colors.primary, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  buttonText: { color: colors.white, fontSize: 14, fontWeight: '600' },
});

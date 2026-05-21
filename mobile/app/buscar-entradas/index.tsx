import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { entradasApi } from '../../api/entradas';
import { Entrada } from '../../types';
import { formatPrecio } from '../../utils/format';

export default function BuscarEntradasScreen() {
  const [email, setEmail] = useState('');
  const [entradas, setEntradas] = useState<Entrada[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleBuscar = async () => {
    if (!email) return;
    setLoading(true);
    setSearched(true);
    try {
      const res = await entradasApi.buscar(email);
      setEntradas(res.data);
    } catch {
      setEntradas([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Buscar Mis Entradas</Text>
      <Text style={styles.subtitle}>Ingresá tu email para buscar tus entradas</Text>
      <View style={styles.searchRow}>
        <TextInput
          style={styles.input}
          placeholder="tu@email.com"
          placeholderTextColor={colors.textMuted}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TouchableOpacity style={styles.searchButton} onPress={handleBuscar} disabled={loading}>
          {loading ? <ActivityIndicator color={colors.white} /> : <Ionicons name="search" size={22} color={colors.white} />}
        </TouchableOpacity>
      </View>
      {searched && !loading && entradas.length === 0 && (
        <Text style={styles.noResults}>No se encontraron entradas para este email</Text>
      )}
      <FlatList
        data={entradas}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => router.push(`/entrada/${item.id}`)}>
            <Text style={styles.cardTitle}>{item.evento_nombre || `Entrada #${item.id}`}</Text>
            <Text style={styles.cardCodigo}>{item.preference_id || item.payment_order_id}</Text>
            <Text style={styles.cardTotal}>{formatPrecio(item.total)}</Text>
          </TouchableOpacity>
        )}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  back: { marginBottom: 16 },
  title: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginBottom: 8 },
  subtitle: { color: colors.textSecondary, fontSize: 14, marginBottom: 20 },
  searchRow: { flexDirection: 'row', gap: 8, marginBottom: 20 },
  input: {
    flex: 1,
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 10,
    padding: 14,
    color: colors.text,
    fontSize: 15,
  },
  searchButton: {
    backgroundColor: colors.primary,
    width: 48,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  noResults: { color: colors.textMuted, fontSize: 14, textAlign: 'center', marginTop: 40 },
  list: { paddingBottom: 20 },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
  },
  cardTitle: { color: colors.text, fontSize: 15, fontWeight: '600', marginBottom: 4 },
  cardCodigo: { color: colors.primary, fontSize: 13, marginBottom: 4 },
  cardTotal: { color: colors.success, fontSize: 14, fontWeight: '600' },
});

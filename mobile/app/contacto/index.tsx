import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import api from '../../api/client';

export default function ContactoScreen() {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [asunto, setAsunto] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [loading, setLoading] = useState(false);

  const handleEnviar = async () => {
    if (!nombre || !email || !mensaje) { Alert.alert('Error', 'Completá los campos obligatorios'); return; }
    setLoading(true);
    try {
      await api.post('/api/contacto/enviar', { nombre, email, asunto, mensaje });
      Alert.alert('Enviado', 'Mensaje enviado correctamente');
      router.back();
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al enviar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Contacto</Text>
      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Nombre" placeholderTextColor={colors.textMuted} value={nombre} onChangeText={setNombre} />
        <TextInput style={styles.input} placeholder="Email" placeholderTextColor={colors.textMuted} value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" />
        <TextInput style={styles.input} placeholder="Asunto" placeholderTextColor={colors.textMuted} value={asunto} onChangeText={setAsunto} />
        <TextInput style={[styles.input, styles.textArea]} placeholder="Mensaje" placeholderTextColor={colors.textMuted} value={mensaje} onChangeText={setMensaje} multiline numberOfLines={5} />
        <TouchableOpacity style={styles.button} onPress={handleEnviar} disabled={loading}>
          {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Enviar Mensaje</Text>}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  back: { marginBottom: 16 },
  title: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  form: { gap: 12 },
  input: {
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 10,
    padding: 14,
    color: colors.text,
    fontSize: 15,
  },
  textArea: { height: 120, textAlignVertical: 'top' },
  button: { backgroundColor: colors.primary, padding: 16, borderRadius: 10, alignItems: 'center', marginTop: 8 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
});

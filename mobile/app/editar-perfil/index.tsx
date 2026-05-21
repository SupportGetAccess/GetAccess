import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator, KeyboardAvoidingView, Platform } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { useAuthStore } from '../../stores/authStore';
import { authApi } from '../../api/auth';

export default function EditarPerfilScreen() {
  const user = useAuthStore((s) => s.user);
  const updateUser = useAuthStore((s) => s.updateUser);
  const [nombre, setNombre] = useState(user?.nombre || '');
  const [apellido, setApellido] = useState(user?.apellido || '');
  const [loading, setLoading] = useState(false);

  const handleGuardar = async () => {
    if (!nombre || !apellido) { Alert.alert('Error', 'Completá todos los campos'); return; }
    setLoading(true);
    try {
      const res = await authApi.updateProfile({ nombre, apellido });
      if (user) updateUser({ ...user, nombre: res.data.nombre, apellido: res.data.apellido });
      Alert.alert('Guardado', 'Perfil actualizado correctamente');
      router.back();
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al actualizar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Editar Perfil</Text>
      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Nombre" placeholderTextColor={colors.textMuted} value={nombre} onChangeText={setNombre} />
        <TextInput style={styles.input} placeholder="Apellido" placeholderTextColor={colors.textMuted} value={apellido} onChangeText={setApellido} />
        <TextInput style={[styles.input, { color: colors.textMuted }]} value={user?.email} editable={false} />
        <TouchableOpacity style={[styles.button, loading && { opacity: 0.6 }]} onPress={handleGuardar} disabled={loading}>
          {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Guardar Cambios</Text>}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  back: { marginBottom: 20 },
  title: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginBottom: 24 },
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
  button: { backgroundColor: colors.primary, padding: 16, borderRadius: 10, alignItems: 'center', marginTop: 8 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
});

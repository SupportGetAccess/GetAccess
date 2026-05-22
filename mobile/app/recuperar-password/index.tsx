import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { authApi } from '../../api/auth';

export default function RecuperarPasswordScreen() {
  const { token } = useLocalSearchParams<{ token: string }>();
  const [email, setEmail] = useState('');
  const [nuevaPassword, setNuevaPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [resetDone, setResetDone] = useState(false);

  const handleRecuperar = async () => {
    if (!email) { Alert.alert('Error', 'Ingresá tu email'); return; }
    setLoading(true);
    try {
      await authApi.recuperarPassword(email);
      setSent(true);
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al enviar');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (nuevaPassword.length < 8) { Alert.alert('Error', 'Mínimo 8 caracteres'); return; }
    setLoading(true);
    try {
      await authApi.restablecerPassword(token!, nuevaPassword);
      setResetDone(true);
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al restablecer');
    } finally {
      setLoading(false);
    }
  };

  if (token) {
    return (
      <View style={styles.container}>
        <TouchableOpacity style={styles.back} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        {resetDone ? (
          <>
            <Ionicons name="checkmark-circle" size={48} color={colors.success} />
            <Text style={styles.title}>Contraseña Restablecida</Text>
            <Text style={styles.subtitle}>Ya podés iniciar sesión con tu nueva contraseña</Text>
            <TouchableOpacity style={styles.button} onPress={() => router.push('/(auth)/login')}>
              <Text style={styles.buttonText}>Iniciar Sesión</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.title}>Nueva Contraseña</Text>
            <Text style={styles.subtitle}>Ingresá tu nueva contraseña</Text>
            <TextInput style={styles.input} placeholder="••••••••" placeholderTextColor={colors.textMuted} value={nuevaPassword} onChangeText={setNuevaPassword} secureTextEntry />
            <TouchableOpacity style={styles.button} onPress={handleReset} disabled={loading}>
              {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Restablecer</Text>}
            </TouchableOpacity>
          </>
        )}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      {sent ? (
        <>
          <Ionicons name="mail" size={48} color={colors.primary} />
          <Text style={styles.title}>Email Enviado</Text>
          <Text style={styles.subtitle}>Revisá tu bandeja de entrada para restablecer tu contraseña</Text>
        </>
      ) : (
        <>
          <Text style={styles.title}>Recuperar Contraseña</Text>
          <Text style={styles.subtitle}>Te enviaremos un link para restablecer tu contraseña</Text>
          <TextInput style={styles.input} placeholder="tu@email.com" placeholderTextColor={colors.textMuted} value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" />
          <TouchableOpacity style={styles.button} onPress={handleRecuperar} disabled={loading}>
            {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Enviar</Text>}
          </TouchableOpacity>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 24, paddingTop: 80, alignItems: 'center' },
  back: { position: 'absolute', top: 40, left: 16 },
  title: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginBottom: 8, textAlign: 'center' },
  subtitle: { color: colors.textSecondary, fontSize: 14, marginBottom: 24, textAlign: 'center' },
  input: {
    width: '100%',
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 10,
    padding: 14,
    color: colors.text,
    fontSize: 15,
    marginBottom: 16,
  },
  button: { backgroundColor: colors.primary, width: '100%', padding: 16, borderRadius: 10, alignItems: 'center' },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
});

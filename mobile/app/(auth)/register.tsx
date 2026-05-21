import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Alert, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { useAuthStore } from '../../stores/authStore';
import { validarEmail, validarPassword } from '../../utils/validators';

export default function RegisterScreen() {
  const [step, setStep] = useState<'form' | 'verify'>('form');
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [codigo, setCodigo] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const register = useAuthStore((s) => s.register);
  const verify = useAuthStore((s) => s.verify);

  const handleRegister = async () => {
    if (!nombre || !apellido || !email || !password) {
      Alert.alert('Error', 'Completá todos los campos');
      return;
    }
    if (!validarEmail(email)) {
      Alert.alert('Error', 'Email inválido');
      return;
    }
    const passwordError = validarPassword(password);
    if (passwordError) {
      Alert.alert('Error', passwordError);
      return;
    }
    setLoading(true);
    try {
      await register({ email, nombre, apellido, password });
      setStep('verify');
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al registrarse');
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    if (codigo.length !== 6) {
      Alert.alert('Error', 'Ingresá el código de 6 dígitos');
      return;
    }
    setLoading(true);
    try {
      await verify(email, codigo);
      Alert.alert('¡Registro exitoso!', 'Tu cuenta fue verificada correctamente.', [
        { text: 'OK', onPress: () => router.replace('/(tabs)/eventos') },
      ]);
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Código inválido');
    } finally {
      setLoading(false);
    }
  };

  if (step === 'verify') {
    return (
      <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View style={styles.content}>
          <TouchableOpacity style={styles.back} onPress={() => setStep('form')}>
            <Ionicons name="arrow-back" size={24} color={colors.text} />
          </TouchableOpacity>
          <Text style={styles.title}>Verificar Email</Text>
          <Text style={styles.subtitle}>Ingresá el código que enviamos a {email}</Text>
          <View style={styles.form}>
            <TextInput
              style={styles.codeInput}
              placeholder="000000"
              placeholderTextColor={colors.textMuted}
              value={codigo}
              onChangeText={setCodigo}
              keyboardType="number-pad"
              maxLength={6}
            />
            <TouchableOpacity style={[styles.button, loading && styles.buttonDisabled]} onPress={handleVerify} disabled={loading}>
              {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Verificar</Text>}
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    );
  }

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView style={styles.scroll} contentContainerStyle={styles.content}>
        <TouchableOpacity style={styles.back} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={styles.title}>Crear Cuenta</Text>
        <Text style={styles.subtitle}>Completá tus datos para registrarte</Text>
        <View style={styles.form}>
          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Nombre</Text>
              <TextInput style={styles.input} placeholder="Juan" placeholderTextColor={colors.textMuted} value={nombre} onChangeText={setNombre} />
            </View>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Apellido</Text>
              <TextInput style={styles.input} placeholder="Pérez" placeholderTextColor={colors.textMuted} value={apellido} onChangeText={setApellido} />
            </View>
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Email</Text>
            <TextInput style={styles.input} placeholder="tu@email.com" placeholderTextColor={colors.textMuted} value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" />
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Contraseña</Text>
            <View style={styles.passwordContainer}>
              <TextInput style={[styles.input, { flex: 1 }]} placeholder="••••••••" placeholderTextColor={colors.textMuted} value={password} onChangeText={setPassword} secureTextEntry={!showPassword} />
              <TouchableOpacity onPress={() => setShowPassword(!showPassword)} style={styles.eyeButton}>
                <Ionicons name={showPassword ? 'eye-off' : 'eye'} size={22} color={colors.textMuted} />
              </TouchableOpacity>
            </View>
          </View>
          <TouchableOpacity style={[styles.button, loading && styles.buttonDisabled]} onPress={handleRegister} disabled={loading}>
            {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>Crear Cuenta</Text>}
          </TouchableOpacity>
        </View>
        <View style={styles.footer}>
          <Text style={styles.footerText}>¿Ya tenés cuenta? </Text>
          <TouchableOpacity onPress={() => router.replace('/(auth)/login')}>
            <Text style={styles.footerLink}>Iniciá Sesión</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  scroll: { flex: 1 },
  content: { padding: 24, paddingTop: 80, flexGrow: 1 },
  back: { position: 'absolute', top: 40, left: 16 },
  title: { fontSize: 28, fontWeight: 'bold', color: colors.text, marginBottom: 8 },
  subtitle: { color: colors.textSecondary, fontSize: 14, marginBottom: 32 },
  form: { gap: 16 },
  row: { flexDirection: 'row', gap: 12 },
  inputGroup: { gap: 6 },
  label: { color: colors.textSecondary, fontSize: 13, fontWeight: '500' },
  input: {
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.inputBorder,
    borderRadius: 10,
    padding: 14,
    color: colors.text,
    fontSize: 15,
  },
  codeInput: {
    backgroundColor: colors.inputBg,
    borderWidth: 1,
    borderColor: colors.primary,
    borderRadius: 10,
    padding: 16,
    color: colors.text,
    fontSize: 24,
    textAlign: 'center',
    letterSpacing: 8,
    fontWeight: 'bold',
  },
  passwordContainer: { flexDirection: 'row', alignItems: 'center' },
  eyeButton: { position: 'absolute', right: 14 },
  button: { backgroundColor: colors.primary, padding: 16, borderRadius: 10, alignItems: 'center', marginTop: 8 },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
  footer: { flexDirection: 'row', justifyContent: 'center', marginTop: 24 },
  footerText: { color: colors.textSecondary, fontSize: 14 },
  footerLink: { color: colors.primary, fontSize: 14, fontWeight: '600' },
});

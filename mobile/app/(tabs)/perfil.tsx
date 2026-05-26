import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Alert } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { useAuthStore } from '../../stores/authStore';

export default function PerfilScreen() {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    Alert.alert('Cerrar Sesión', '¿Estás seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Cerrar Sesión', style: 'destructive', onPress: logout },
    ]);
  };

  if (!isAuthenticated) {
    return (
      <View style={styles.center}>
        <Ionicons name="person-circle-outline" size={64} color={colors.textMuted} />
        <Text style={styles.title}>Perfil</Text>
        <Text style={styles.subtitle}>Iniciá sesión para acceder a tu perfil</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.push('/(auth)/login')}>
          <Text style={styles.buttonText}>Iniciar Sesión</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.linkButton} onPress={() => router.push('/(auth)/register')}>
          <Text style={styles.linkText}>Crear Cuenta</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="person-circle" size={64} color={colors.primary} />
        <Text style={styles.name}>{user?.nombre} {user?.apellido}</Text>
        <Text style={styles.email}>{user?.email}</Text>
        <View style={styles.rolBadge}>
          <Text style={styles.rolText}>{user?.rol?.toUpperCase()}</Text>
        </View>
      </View>
      <View style={styles.section}>
        <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/editar-perfil')}>
          <Ionicons name="create-outline" size={22} color={colors.text} />
          <Text style={styles.menuText}>Editar Perfil</Text>
          <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
        </TouchableOpacity>
        {(user?.rol === 'admin' || user?.rol === 'organizer') && (
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/admin/index')}>
            <Ionicons name="shield-outline" size={22} color={colors.primary} />
            <Text style={styles.menuText}>Panel Admin</Text>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        )}
        {(user?.rol === 'admin' || user?.rol === 'organizer') && (
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/scanner')}>
            <Ionicons name="qr-code-outline" size={22} color={colors.success} />
            <Text style={styles.menuText}>Escanear Entradas</Text>
            <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
          </TouchableOpacity>
        )}
        <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/contacto')}>
          <Ionicons name="mail-outline" size={22} color={colors.text} />
          <Text style={styles.menuText}>Contacto</Text>
          <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/transferencias-pendientes')}>
          <Ionicons name="swap-horizontal-outline" size={22} color={colors.info} />
          <Text style={styles.menuText}>Transferencias Pendientes</Text>
          <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/privacidad')}>
          <Ionicons name="shield-checkmark-outline" size={22} color={colors.textMuted} />
          <Text style={styles.menuText}>Política de Privacidad</Text>
          <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
        </TouchableOpacity>
      </View>
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Ionicons name="log-out-outline" size={22} color={colors.error} />
        <Text style={styles.logoutText}>Cerrar Sesión</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  header: {
    alignItems: 'center',
    paddingTop: 80,
    paddingBottom: 24,
    backgroundColor: colors.backgroundLight,
  },
  name: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginTop: 12 },
  email: { color: colors.textSecondary, fontSize: 14, marginTop: 4 },
  rolBadge: {
    backgroundColor: colors.primary,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  rolText: { color: colors.white, fontSize: 11, fontWeight: 'bold', letterSpacing: 1 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginTop: 12 },
  subtitle: { color: colors.textSecondary, marginTop: 8, fontSize: 14, textAlign: 'center' },
  section: { padding: 16, gap: 1 },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.card,
    padding: 16,
    borderRadius: 12,
    marginBottom: 8,
    gap: 12,
  },
  menuText: { flex: 1, color: colors.text, fontSize: 15 },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 40,
    gap: 8,
    backgroundColor: '#2a0000',
    borderRadius: 12,
  },
  logoutText: { color: colors.error, fontSize: 15, fontWeight: '600' },
  button: {
    backgroundColor: colors.primary,
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: '600' },
  linkButton: { marginTop: 12 },
  linkText: { color: colors.primary, fontSize: 14 },
});

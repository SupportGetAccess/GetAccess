import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import { useAuthStore } from '../../stores/authStore';

export default function AdminPanelScreen() {
  const user = useAuthStore((s) => s.user);
  const isAdmin = user?.rol === 'admin';

  if (!user || (user.rol !== 'admin' && user.rol !== 'organizer')) {
    return (
      <View style={styles.center}>
        <Ionicons name="shield-outline" size={48} color={colors.textMuted} />
        <Text style={styles.title}>Acceso Restringido</Text>
        <Text style={styles.subtitle}>Solo administradores y organizadores</Text>
        <TouchableOpacity style={styles.button} onPress={() => router.back()}>
          <Text style={styles.buttonText}>Volver</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const menuItems = [
    { icon: 'stats-chart', label: 'Dashboard', route: '/admin/dashboard', adminOnly: false },
    { icon: 'calendar', label: 'Mis Eventos', route: '/admin/mis-eventos', adminOnly: false },
    { icon: 'add-circle', label: 'Crear Evento', route: '/admin/crear-evento', adminOnly: false },
    { icon: 'people', label: 'Solicitudes Organizer', route: '/admin/solicitudes', adminOnly: true },
    { icon: 'checkmark-circle', label: 'Validaciones', route: '/admin/validaciones', adminOnly: false },
  ];

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Panel Admin</Text>
      <View style={styles.menu}>
        {menuItems
          .filter((item) => !item.adminOnly || isAdmin)
          .map((item) => (
            <TouchableOpacity key={item.route} style={styles.menuItem} onPress={() => router.push(item.route)}>
              <Ionicons name={item.icon as any} size={24} color={colors.primary} />
              <Text style={styles.menuLabel}>{item.label}</Text>
              <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
            </TouchableOpacity>
          ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  backButton: { marginBottom: 16 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  subtitle: { color: colors.textSecondary, fontSize: 14, textAlign: 'center', marginTop: 8, marginBottom: 20 },
  menu: { gap: 8 },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.card,
    padding: 16,
    borderRadius: 12,
    gap: 14,
  },
  menuLabel: { flex: 1, color: colors.text, fontSize: 15, fontWeight: '500' },
  button: { backgroundColor: colors.primary, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  buttonText: { color: colors.white, fontSize: 14, fontWeight: '600' },
});

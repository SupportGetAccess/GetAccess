import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';

export default function SolicitudesScreen() {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.back} onPress={() => router.back()}>
        <Ionicons name="arrow-back" size={24} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.title}>Solicitudes Organizer</Text>
      <Text style={styles.placeholder}>Próximamente</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16, paddingTop: 60 },
  back: { marginBottom: 16 },
  title: { fontSize: 22, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  placeholder: { color: colors.textMuted, fontSize: 14, textAlign: 'center', marginTop: 40 },
});

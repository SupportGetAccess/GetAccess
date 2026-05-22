import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';

export default function PrivacidadScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={styles.title}>Política de Privacidad</Text>
      </View>
      <ScrollView style={styles.scroll} contentContainerStyle={styles.content}>
        <Text style={styles.lastUpdate}>Última actualización: 27/04/2026</Text>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>1. Aspectos Generales</Text>
          <Text style={styles.boxText}>
            La presente política de privacidad se aplica al sitio web getaccess.com.ar y al scanner QR de acceso a eventos, ambos servicios de titularidad de Get Access.
          </Text>
          <Text style={styles.boxText}>
            Conforme a la legislación vigente en materia de Protección de Datos de Carácter Personal (Ley 25.326 Argentina y GDPR), Get Access informa a los Usuarios acerca de la política de privacidad que aplicará en el tratamiento de los datos personales.
          </Text>
          <Text style={styles.boxText}>
            Para navegar en el sitio no es necesario revelar datos personales. En ciertos casos, como realizar una compra o registrarte, requeriremos tu nombre, apellido, dirección de correo electrónico y teléfono.
          </Text>
          <Text style={styles.boxText}>
            La utilización del sitio por parte de los Usuarios implica necesariamente el conocimiento y aceptación de la presente Política de Privacidad.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>2. Tratamiento de Datos Personales</Text>
          <Text style={styles.boxText}>
            Para realizar compras en el sitio y utilizar el sistema de entradas, los Usuarios deberán proporcionar algunos datos personales, los cuales deben ser veraces. El Usuario, al proporcionar sus datos, consiente expresamente que Get Access pueda tratar esos datos en los términos establecidos.
          </Text>
          <Text style={styles.boxText}>
            Get Access podrá también recopilar la dirección IP del Usuario así como los datos de navegación con el fin de identificar posibles usos fraudulentos, así como adaptar el contenido y mejorar la experiencia del usuario.
          </Text>
          <Text style={styles.boxText}>
            Los datos voluntariamente facilitados serán incorporados a un archivo debidamente protegido con la finalidad de identificarle y contactarle para posibilitar la correcta prestación de los servicios.
          </Text>
          <Text style={styles.boxText}>
            Los datos están alojados en servicios de cloud (Supabase, Render) con medidas técnicas y organizativas de seguridad.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>3. Derechos del Usuario</Text>
          <Text style={styles.boxText}>El titular de los datos personales tiene la facultad de:</Text>
          <Text style={styles.bullet}>Acceso a sus datos en forma gratuita y a intervalos no inferiores a seis meses.</Text>
          <Text style={styles.bullet}>Rectificación de datos inexactos.</Text>
          <Text style={styles.bullet}>Supresión de datos cuando corresponda.</Text>
          <Text style={styles.bullet}>Oposición al tratamiento de sus datos.</Text>
          <Text style={styles.boxText}>Para ejercer estos derechos, contactenos a: soporte@getaccess.com.ar</Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>4. Cesión de Datos</Text>
          <Text style={styles.boxText}>
            Los datos personales facilitados por los Usuarios podrán ser cedidos a los Organizadores de los eventos y espectáculos a los que el Usuario asista con la finalidad de que estos puedan mantenerle informado de información relativa al evento.
          </Text>
          <Text style={styles.boxText}>
            Si el Usuario no desea que sus datos sean cedidos a los Organizadores, podrá revocar su consentimiento mediante comunicación a soporte@getaccess.com.ar.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>5. Comunicaciones Comerciales</Text>
          <Text style={styles.boxText}>
            Con la utilización del sitio, el Usuario consiente la recepción de comunicaciones comerciales vía correo electrónico relacionadas con los productos o servicios que ofrece Get Access.
          </Text>
          <Text style={styles.boxText}>
            El Usuario podrá renunciar en cualquier momento a recibir comunicaciones enviando un email a soporte@getaccess.com.ar.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>6. Menores de Edad</Text>
          <Text style={styles.boxText}>
            Los servicios del sitio solo están disponibles para mayores de edad. Las personas que no cumplan con esta condición deberán abstenerse de suministrar información personal.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>7. Cookies</Text>
          <Text style={styles.boxText}>
            El sitio utiliza cookies para mejorar la experiencia del usuario y recopilar datos estadísticos anónimos de uso.
          </Text>
          <Text style={styles.boxText}>
            El usuario puede configurar su navegador para rechazar cookies, aunque esto puede afectar el funcionamiento del sitio.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>8. Protección de Datos</Text>
          <Text style={styles.bullet}>Contraseñas hasheadas con bcrypt</Text>
          <Text style={styles.bullet}>Conexión HTTPS (SSL/TLS)</Text>
          <Text style={styles.bullet}>Credenciales en variables de entorno</Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>9. Retención de Datos</Text>
          <Text style={styles.bullet}>Cuentas inactivas: eliminadas después de 12 meses</Text>
          <Text style={styles.bullet}>Datos de compras: retenidos por el tiempo requerido por ley</Text>
          <Text style={styles.bullet}>Backups: almacenados en GitHub (accesible solo por admins)</Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>10. Denuncias</Text>
          <Text style={styles.boxText}>
            Para denunciar una violación de derechos con respecto al tratamiento de datos personales, podrá comunicarse escribiendo a soporte@getaccess.com.ar.
          </Text>
          <Text style={styles.boxText}>
            También puede dirigirse a la Agencia de Acceso a la Información Pública (AAIP), sita en Av. Pte. Gral. Julio A. Roca 710, piso 3 - Ciudad Autónoma de Buenos Aires - República Argentina.
          </Text>
        </View>

        <View style={styles.box}>
          <Text style={styles.boxTitle}>11. Modificaciones</Text>
          <Text style={styles.boxText}>
            Get Access se reserva el derecho de modificar la presente Política de Privacidad de acuerdo con la legislación aplicable. Se recomienda al Usuario que revise periódicamente los términos.
          </Text>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Get Access - Plataforma de gestión de entradas y accesos a eventos</Text>
          <Text style={styles.footerText}>Web: https://getaccess.com.ar | Email: soporte@getaccess.com.ar</Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 16,
    paddingBottom: 16,
    backgroundColor: colors.backgroundLight,
  },
  backButton: { marginRight: 12 },
  title: { fontSize: 20, fontWeight: 'bold', color: colors.text },
  scroll: { flex: 1 },
  content: { padding: 16, paddingBottom: 40 },
  lastUpdate: { color: colors.textMuted, fontSize: 13, marginBottom: 20 },
  box: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  boxTitle: { fontSize: 16, fontWeight: 'bold', color: colors.primary, marginBottom: 10 },
  boxText: { color: colors.textSecondary, fontSize: 14, lineHeight: 22, marginBottom: 8 },
  bullet: { color: colors.textSecondary, fontSize: 14, lineHeight: 22, marginBottom: 4, paddingLeft: 16 },
  footer: { alignItems: 'center', padding: 20, borderTopWidth: 1, borderTopColor: colors.border, marginTop: 8 },
  footerText: { color: colors.textMuted, fontSize: 12, textAlign: 'center', lineHeight: 20 },
});

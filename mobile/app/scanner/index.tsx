import { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, Vibration } from 'react-native';
import { router } from 'expo-router';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../theme';
import api from '../../api/client';

export default function ScannerScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [scanning, setScanning] = useState(true);
  const [lastResult, setLastResult] = useState<{ success: boolean; mensaje: string } | null>(null);

  if (!permission) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>Solicitando permiso de cámara...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.center}>
        <Ionicons name="camera-outline" size={48} color={colors.textMuted} />
        <Text style={styles.text}>Permiso de cámara denegado</Text>
        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Solicitar Permiso</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleScan = async (data: string) => {
    if (!scanning) return;
    setScanning(false);
    try {
      const res = await api.post('/api/validar-entrada', { codigo: data });
      setLastResult(res.data);
      Vibration.vibrate(res.data.valida ? 200 : 500);
    } catch {
      setLastResult({ success: false, mensaje: 'Error al validar' });
      Vibration.vibrate(500);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Ionicons name="close" size={28} color={colors.white} />
      </TouchableOpacity>
      <Text style={styles.title}>Escanear Entrada</Text>
      <View style={styles.cameraContainer}>
        <CameraView
          style={styles.camera}
          facing="back"
          barcodeScannerSettings={{ barcodeTypes: ['qr'] }}
          onBarcodeScanned={scanning ? (result) => handleScan(result.data) : undefined}
        />
        <View style={styles.overlay}>
          <View style={styles.scanFrame} />
        </View>
      </View>
      {lastResult && (
        <View style={[styles.resultBanner, lastResult.success ? styles.successBanner : styles.errorBanner]}>
          <Ionicons name={lastResult.success ? 'checkmark-circle' : 'close-circle'} size={24} color={colors.white} />
          <Text style={styles.resultText}>{lastResult.mensaje}</Text>
        </View>
      )}
      <TouchableOpacity style={styles.scanAgain} onPress={() => { setScanning(true); setLastResult(null); }}>
        <Text style={styles.scanAgainText}>Escanear Otro</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.black },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background, padding: 20 },
  backButton: { position: 'absolute', top: 60, left: 16, zIndex: 10 },
  title: { color: colors.white, fontSize: 18, fontWeight: '600', textAlign: 'center', paddingTop: 60, paddingBottom: 16 },
  cameraContainer: { flex: 1, marginHorizontal: 16, borderRadius: 12, overflow: 'hidden' },
  camera: { flex: 1 },
  overlay: { ...StyleSheet.absoluteFill as object, justifyContent: 'center', alignItems: 'center' },
  scanFrame: {
    width: 240,
    height: 240,
    borderWidth: 2,
    borderColor: colors.primary,
    borderRadius: 16,
    backgroundColor: 'transparent',
  },
  resultBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    marginHorizontal: 16,
    marginTop: 12,
    borderRadius: 10,
    gap: 8,
  },
  successBanner: { backgroundColor: colors.success },
  errorBanner: { backgroundColor: colors.error },
  resultText: { color: colors.white, fontSize: 14, fontWeight: '500', flex: 1 },
  scanAgain: { alignItems: 'center', padding: 16, marginBottom: 20 },
  scanAgainText: { color: colors.primary, fontSize: 16, fontWeight: '600' },
  text: { color: colors.text, fontSize: 16, textAlign: 'center', marginBottom: 16 },
  button: { backgroundColor: colors.primary, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 8 },
  buttonText: { color: colors.white, fontSize: 14, fontWeight: '600' },
});

import { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert, ActivityIndicator, Image, KeyboardAvoidingView, Platform } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import { colors } from '../../../theme';
import { eventosApi } from '../../../api/eventos';
import { useQuery } from '@tanstack/react-query';

export default function CrearEventoScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const isEditing = !!id;

  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [fecha, setFecha] = useState('');
  const [hora, setHora] = useState('20:00');
  const [lugar, setLugar] = useState('');
  const [precio, setPrecio] = useState('');
  const [capacidad, setCapacidad] = useState('');
  const [categoria, setCategoria] = useState('');
  const [comision, setComision] = useState('0');
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const { data: categorias } = useQuery({
    queryKey: ['categorias'],
    queryFn: () => eventosApi.categorias().then((r) => r.data),
  });

  const { data: eventoExistente } = useQuery({
    queryKey: ['evento', id],
    queryFn: () => eventosApi.obtener(Number(id)).then((r) => r.data),
    enabled: isEditing,
  });

  useEffect(() => {
    if (eventoExistente) {
      setNombre(eventoExistente.nombre);
      setDescripcion(eventoExistente.descripcion || '');
      const fechaParts = eventoExistente.fecha.split(' ');
      setFecha(fechaParts[0] || '');
      setHora(fechaParts[1]?.substring(0, 5) || '20:00');
      setLugar(eventoExistente.lugar);
      setPrecio(String(eventoExistente.precio));
      setCapacidad(String(eventoExistente.capacidad));
      setCategoria(eventoExistente.categoria || '');
      setComision(String(eventoExistente.comision || 0));
    }
  }, [eventoExistente]);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsMultipleSelection: true,
      selectionLimit: 4 - images.length,
      quality: 0.8,
    });
    if (!result.canceled) {
      setImages((prev) => [...prev, ...result.assets.map((a) => a.uri)]);
    }
  };

  const removeImage = (index: number) => {
    setImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (!nombre || !fecha || !lugar || !precio || !capacidad) {
      Alert.alert('Error', 'Completá los campos obligatorios (nombre, fecha, lugar, precio, capacidad)');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('nombre', nombre);
      formData.append('descripcion', descripcion);
      formData.append('fecha', `${fecha} ${hora}:00`);
      formData.append('lugar', lugar);
      formData.append('precio', precio);
      formData.append('capacidad', capacidad);
      formData.append('categoria', categoria);
      formData.append('comision', comision);

      for (let i = 0; i < images.length; i++) {
        const uri = images[i];
        const filename = uri.split('/').pop() || `image_${i}.jpg`;
        const match = /\.(\w+)$/.exec(filename);
        const ext = match?.[1] || 'jpg';
        formData.append(`imagen_${i + 1}`, {
          uri,
          type: `image/${ext}`,
          name: filename,
        } as any);
      }

      if (isEditing) {
        await eventosApi.actualizar(Number(id), formData);
        Alert.alert('Actualizado', 'Evento actualizado correctamente');
      } else {
        await eventosApi.crear(formData);
        Alert.alert('Creado', 'Evento creado correctamente');
      }
      router.back();
    } catch (err: any) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al guardar el evento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView contentContainerStyle={styles.content}>
        <TouchableOpacity style={styles.back} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={styles.title}>{isEditing ? 'Editar Evento' : 'Crear Evento'}</Text>
        <View style={styles.form}>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Nombre *</Text>
            <TextInput style={styles.input} placeholder="Nombre del evento" placeholderTextColor={colors.textMuted} value={nombre} onChangeText={setNombre} />
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Descripción</Text>
            <TextInput style={[styles.input, styles.textArea]} placeholder="Descripción del evento" placeholderTextColor={colors.textMuted} value={descripcion} onChangeText={setDescripcion} multiline numberOfLines={4} />
          </View>
          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 2 }]}>
              <Text style={styles.label}>Fecha *</Text>
              <TextInput style={styles.input} placeholder="2026-06-15" placeholderTextColor={colors.textMuted} value={fecha} onChangeText={setFecha} />
            </View>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Hora</Text>
              <TextInput style={styles.input} placeholder="20:00" placeholderTextColor={colors.textMuted} value={hora} onChangeText={setHora} />
            </View>
          </View>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Lugar *</Text>
            <TextInput style={styles.input} placeholder="Lugar del evento" placeholderTextColor={colors.textMuted} value={lugar} onChangeText={setLugar} />
          </View>
          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Precio *</Text>
              <TextInput style={styles.input} placeholder="0" placeholderTextColor={colors.textMuted} value={precio} onChangeText={setPrecio} keyboardType="decimal-pad" />
            </View>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Capacidad *</Text>
              <TextInput style={styles.input} placeholder="0" placeholderTextColor={colors.textMuted} value={capacidad} onChangeText={setCapacidad} keyboardType="number-pad" />
            </View>
          </View>
          <View style={styles.row}>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Categoría</Text>
              <TextInput style={styles.input} placeholder="Ej: Música, Deportes" placeholderTextColor={colors.textMuted} value={categoria} onChangeText={setCategoria} />
            </View>
            <View style={[styles.inputGroup, { flex: 1 }]}>
              <Text style={styles.label}>Comisión %</Text>
              <TextInput style={styles.input} placeholder="0" placeholderTextColor={colors.textMuted} value={comision} onChangeText={setComision} keyboardType="decimal-pad" />
            </View>
          </View>
          {categorias && categorias.length > 0 && (
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Categorías disponibles</Text>
              <View style={styles.chipRow}>
                {categorias.map((cat) => (
                  <TouchableOpacity key={cat} style={[styles.chip, categoria === cat && styles.chipActive]} onPress={() => setCategoria(cat)}>
                    <Text style={[styles.chipText, categoria === cat && styles.chipTextActive]}>{cat}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Imágenes (máx 4)</Text>
            <View style={styles.imageRow}>
              {images.map((uri, i) => (
                <View key={i} style={styles.imageContainer}>
                  <Image source={{ uri }} style={styles.thumb} />
                  <TouchableOpacity style={styles.removeImage} onPress={() => removeImage(i)}>
                    <Ionicons name="close-circle" size={22} color={colors.error} />
                  </TouchableOpacity>
                </View>
              ))}
              {images.length < 4 && (
                <TouchableOpacity style={styles.addImage} onPress={pickImage}>
                  <Ionicons name="camera" size={28} color={colors.textMuted} />
                </TouchableOpacity>
              )}
            </View>
          </View>
          <TouchableOpacity style={[styles.button, loading && { opacity: 0.6 }]} onPress={handleSubmit} disabled={loading}>
            {loading ? <ActivityIndicator color={colors.white} /> : <Text style={styles.buttonText}>{isEditing ? 'Guardar Cambios' : 'Crear Evento'}</Text>}
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: 16, paddingTop: 60, paddingBottom: 40 },
  back: { marginBottom: 16 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text, marginBottom: 20 },
  form: { gap: 14 },
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
  textArea: { height: 100, textAlignVertical: 'top' },
  row: { flexDirection: 'row', gap: 12 },
  chipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: {
    backgroundColor: colors.card,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  chipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  chipText: { color: colors.textSecondary, fontSize: 13 },
  chipTextActive: { color: colors.white, fontWeight: '600' },
  imageRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  imageContainer: { position: 'relative' },
  thumb: { width: 80, height: 80, borderRadius: 8, backgroundColor: colors.card },
  removeImage: { position: 'absolute', top: -6, right: -6 },
  addImage: {
    width: 80,
    height: 80,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.card,
  },
  button: { backgroundColor: colors.primary, padding: 16, borderRadius: 10, alignItems: 'center', marginTop: 8 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: 'bold' },
});

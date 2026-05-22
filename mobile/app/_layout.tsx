import { useEffect, useRef } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { QueryClient } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import * as Linking from 'expo-linking';
import { useAuthStore } from '../stores/authStore';
import { colors } from '../theme';
import { ActivityIndicator, View, StyleSheet } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { registerForPushNotifications, savePushToken } from '../utils/notifications';

SplashScreen.preventAutoHideAsync();

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2,
      retry: 2,
      gcTime: 1000 * 60 * 60 * 24,
    },
  },
});

const asyncStoragePersister = createAsyncStoragePersister({
  storage: AsyncStorage,
  key: 'GETACCESS_QUERY_CACHE',
});

function RootLayoutContent() {
  const isLoading = useAuthStore((s) => s.isLoading);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const loadStoredAuth = useAuthStore((s) => s.loadStoredAuth);
  const pushRegistered = useRef(false);

  useEffect(() => {
    loadStoredAuth().finally(() => SplashScreen.hideAsync());
  }, []);

  useEffect(() => {
    if (isAuthenticated && !pushRegistered.current) {
      pushRegistered.current = true;
      registerForPushNotifications().then((token) => {
        if (token) savePushToken(token);
      });
    }
  }, [isAuthenticated]);

  useEffect(() => {
    const handleDeepLink = (event: Linking.EventType) => {
      const url = event.url;
      if (url.includes('recuperar-password') || url.includes('restablecer')) {
        const token = Linking.parse(url).queryParams?.token;
        if (token) {
          setTimeout(() => {
            (Linking as any).openURL?.(`/recuperar-password?token=${token}`);
          }, 500);
        }
      }
    };
    const subscription = Linking.addEventListener('url', handleDeepLink);
    Linking.getInitialURL().then((url) => {
      if (url && (url.includes('recuperar-password') || url.includes('restablecer'))) {
        const token = Linking.parse(url).queryParams?.token;
        if (token) {
          setTimeout(() => {
            (Linking as any).openURL?.(`/recuperar-password?token=${token}`);
          }, 500);
        }
      }
    });
    return () => subscription.remove();
  }, []);

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.background },
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="(auth)" options={{ animation: 'slide_from_bottom' }} />
      <Stack.Screen name="evento/[id]" />
      <Stack.Screen name="carrito/index" />
      <Stack.Screen name="entrada/[id]" />
      <Stack.Screen name="scanner/index" />
      <Stack.Screen name="admin/index" />
      <Stack.Screen name="transferencias-pendientes/index" />
    </Stack>
  );
}

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PersistQueryClientProvider
        client={queryClient}
        persistOptions={{
          persister: asyncStoragePersister,
          maxAge: 1000 * 60 * 60 * 24,
        }}
      >
        <StatusBar style="light" />
        <RootLayoutContent />
      </PersistQueryClientProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
});

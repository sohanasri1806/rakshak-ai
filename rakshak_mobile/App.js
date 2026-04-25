import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import LoginScreen from './src/screens/LoginScreen.js';
import DashboardScreen from './src/screens/DashboardScreen.js';
import WebViewScreen from './src/screens/WebViewScreen.js';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: '#f0f0f0',
          },
          headerTintColor: '#000',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ title: '🚨 Rakshak AI', headerBackVisible: false }}
        />
        <Stack.Screen
          name="Dashboard"
          component={DashboardScreen}
          options={{ title: '📊 Dashboard', headerBackVisible: false }}
        />
        <Stack.Screen
          name="WebView"
          component={WebViewScreen}
          options={{ title: '🌐 Website' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

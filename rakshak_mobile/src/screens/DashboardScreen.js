import React, { useState } from 'react';
import { View, Button, Alert, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { simulate } from '../api';

export default function DashboardScreen({ navigation, route }) {
  const userName = route.params?.userName || 'User';
  const [simData, setSimData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await simulate();
      setSimData(res.data);
      Alert.alert('Success', `Received ${res.data.length} disaster simulation records`);
    } catch (err) {
      Alert.alert('Error', 'Failed to fetch simulation data: ' + err.message);
      console.log('Simulate error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Welcome, {userName}!</Text>
      <Text style={styles.subtitle}>Rakshak AI Dashboard</Text>

      <View style={styles.buttonGroup}>
        <Button
          title={loading ? 'Loading...' : '📊 Simulate Disaster Data'}
          onPress={handleSimulate}
          disabled={loading}
        />
      </View>

      {loading && <ActivityIndicator size="large" color="#0000ff" style={{ marginTop: 20 }} />}

      {simData && (
        <View style={styles.dataBox}>
          <Text style={styles.dataTitle}>Simulation Results:</Text>
          <Text style={styles.dataText}>{JSON.stringify(simData.slice(0, 3), null, 2)}</Text>
        </View>
      )}

      <View style={styles.spacer} />

      <View style={styles.buttonGroup}>
        <Button title="🌐 Open Website" onPress={() => navigation.navigate('WebView')} />
      </View>

      <View style={styles.buttonGroup}>
        <Button title="🚪 Logout" onPress={() => navigation.navigate('Login')} color="red" />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  buttonGroup: {
    marginBottom: 15,
  },
  dataBox: {
    marginTop: 20,
    padding: 15,
    backgroundColor: 'white',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  dataTitle: {
    fontWeight: 'bold',
    marginBottom: 10,
  },
  dataText: {
    fontSize: 12,
    color: '#333',
  },
  spacer: {
    height: 20,
  },
});

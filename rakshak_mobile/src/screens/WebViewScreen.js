import React from 'react';
import { View, Text } from 'react-native';
import { WebView } from 'react-native-webview';

export default function WebViewScreen() {
  const BASE_URL = 'http://192.168.16.81:5000'; // CHANGE THIS TO YOUR PC IP OR PUBLIC URL

  if (!BASE_URL) {
    return <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}><Text>Please configure BASE_URL in src/screens/WebViewScreen.js</Text></View>;
  }

  return (
    <View style={{ flex: 1 }}>
      <WebView
        source={{ uri: BASE_URL }}
        startInLoadingState={true}
        javaScriptEnabled={true}
      />
    </View>
  );
}

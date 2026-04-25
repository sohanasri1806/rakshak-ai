# Rakshak Mobile (Expo SDK 54)

This folder contains the mobile app code for Rakshak AI, built with Expo and React Native.

## Target environment
- Expo Go client: 54.0.6
- Expo SDK: 54
- React: 18.2.0
- React Native: 0.71.8

## Quick setup
1. Install dependencies:
   ```bash
   cd rakshak_mobile
   npm install
   ```
2. Start Expo:
   ```bash
   npm run start
   ```
3. Open Expo Go on your phone and scan QR code.

## Backend API
- `src/api.js` and `src/screens/WebViewScreen.js` use `BASE_URL = 'http://192.168.16.81:5000'` by default.
- Update to your local machine IP or public URL accessible by your phone:
  - `src/api.js` `BASE_URL`
  - `src/screens/WebViewScreen.js` `BASE_URL`

## Common issues
- If the app does not connect, ensure the backend is running and CORS is enabled (`app.py` uses `CORS(app)`).
- For simulator/emulator use `localhost` or `10.0.2.2` depending on platform.

## Important
- Ensure your phone and backend machine are on same network when using local IP.

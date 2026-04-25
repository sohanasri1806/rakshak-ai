import axios from 'axios';

const BASE_URL = 'http://192.168.16.81:5000'; // CHANGE THIS TO YOUR PC IP FROM ipconfig

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 12000,
});

export const signup = (data) => api.post('/signup', data);
export const login = (data) => api.post('/login', data);
export const simulate = () => api.get('/api/simulate');
export const analyzeUrl = (url) => api.post('/api/analyze_url', { url });
export const chat = (message) => api.post('/api/chat', { message });
export const nearbyPlaces = (lat, lng) => api.post('/api/nearby_safe_places', { lat, lng });

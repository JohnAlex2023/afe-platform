import axios from 'axios';
import { API_BASE_URL, API_TIMEOUT } from '../config/api';

/**
 * API Client - Centralized Axios instance
 *
 * All HTTP requests to the backend MUST go through this instance.
 * It automatically handles:
 *   - Base URL resolution (via VITE_API_URL env variable)
 *   - JWT Bearer token injection
 *   - Multi-tenant X-Grupo-Id header
 *   - 401 redirect to /login
 *
 * Usage:
 *   import apiClient from '@/services/api';
 *   apiClient.get('/auth/login');           →  GET  {VITE_API_URL}/auth/login
 *   apiClient.post('/facturas/', data);     →  POST {VITE_API_URL}/facturas/
 *
 * IMPORTANT: Route paths are RELATIVE (no /api/v1 prefix needed).
 *   ✔  apiClient.post('/auth/login', ...)
 *   ✗  apiClient.post('/api/v1/auth/login', ...)   ← WRONG, baseURL already includes /api/v1
 */

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ─── Request Interceptor ────────────────────────────────────────────────────
apiClient.interceptors.request.use(
  (config) => {
    // 1. Inject JWT Bearer token
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // 2. MULTI-TENANT: Inject grupo_id header
    const grupoId = localStorage.getItem('grupo_id');
    if (grupoId) {
      config.headers['X-Grupo-Id'] = grupoId;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ─── Response Interceptor ───────────────────────────────────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect when there was a stored token (session expired).
      // Avoid redirect loop on the login page itself.
      const currentPath = window.location.pathname;
      const hasToken = localStorage.getItem('access_token');

      if (currentPath !== '/login' && hasToken) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('grupo_id');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

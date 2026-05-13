/**
 * API Configuration - Central source of truth
 *
 * All API-related configuration is defined here.
 * Environment variables:
 *   VITE_API_URL     → Full backend base URL including /api/v1 prefix
 *   VITE_API_TIMEOUT → Request timeout in ms (default: 30000)
 *
 * Local development (.env):
 *   VITE_API_URL=http://localhost:8000/api/v1
 *
 * Production / Vercel:
 *   VITE_API_URL=https://afe-platform.onrender.com/api/v1
 */

/** Full backend API base URL (e.g. http://localhost:8000/api/v1) */
export const API_BASE_URL: string =
  import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/** Request timeout in milliseconds */
export const API_TIMEOUT: number =
  Number(import.meta.env.VITE_API_TIMEOUT) || 30000;

/** Current environment */
export const ENVIRONMENT: string =
  import.meta.env.VITE_ENVIRONMENT || 'development';

/** Whether we are running in production */
export const IS_PRODUCTION: boolean = ENVIRONMENT === 'production';

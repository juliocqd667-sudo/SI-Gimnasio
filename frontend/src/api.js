const envUrl = import.meta.env.VITE_API_URL;

let API_URL;
if (envUrl) {
  API_URL = envUrl.includes('://') ? envUrl : `https://${envUrl}/api`;
} else if (import.meta.env.DEV) {
  // Local development fallback when frontend and backend are separate
  API_URL = 'http://127.0.0.1:8000/api';
} else {
  // Production / same-origin deployment
  API_URL = '/api';
}

export default API_URL;

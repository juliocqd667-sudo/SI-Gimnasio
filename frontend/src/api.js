// If VITE_API_URL is set and doesn't contain protocol, assume it's a domain and construct full URL
// Otherwise, use it as-is (for full URL) or fallback to localhost
let API_URL = import.meta.env.VITE_API_URL;

if (API_URL) {
  // If it doesn't contain ://, assume it's just a domain and construct API URL
  if (!API_URL.includes('://')) {
    API_URL = `https://${API_URL}/api`;
  }
  // If it already contains ://, use it as-is (assuming it's already a full URL)
} else {
  // Fallback for development
  API_URL = 'http://127.0.0.1:8000/api';
}

export default API_URL;

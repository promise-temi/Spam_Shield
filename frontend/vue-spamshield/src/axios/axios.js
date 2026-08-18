import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  headers: {
    "X-API-Key": import.meta.env.VITE_BACKEND_API_KEY
  }
});

export default api;
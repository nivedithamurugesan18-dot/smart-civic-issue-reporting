import axios from "axios";

const DEFAULT_API_URL = "http://127.0.0.1:8000";
const configuredApiUrl =
  import.meta.env.VITE_API_URL || DEFAULT_API_URL;
const apiBaseUrl =
  configuredApiUrl.trim().replace(/\/+$/, "") || DEFAULT_API_URL;

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (
      typeof FormData !== "undefined" &&
      config.data instanceof FormData
    ) {
      delete config.headers["Content-Type"];
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

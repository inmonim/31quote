import axios from "axios";

const backendApi = axios.create({
  baseURL: 'http://localhost:5051/api/v1'
})

backendApi.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('accessToken');

    try {
      if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
      }
      return config
    } catch (error) {
      console.error("[_axios.interceptors.request] config : " + error.message)
    }
    return config;
  },
  (error) => {

    return Promise.reject(error);
  }
);

export default backendApi
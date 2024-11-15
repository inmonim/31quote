import axios from "axios";

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_REACT_APP_API_BASE_URL, // 기본 URL
  timeout: 5000, // 요청 타임아웃 설정
  headers: {
    "Content-Type": "application/json",
  },
  paramsSerializer: (params) => {
    const searchParams = new URLSearchParams();
    Object.keys(params).forEach((key) => {
      const value = params[key];
      if (Array.isArray(value)) {
        // 배열 처리
        value.forEach((v) => searchParams.append(key, v));
      } else {
        searchParams.append(key, value);
      }
    });
    return searchParams.toString();
  },
});

// 요청 전 인터셉터 (Optional)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken"); // 예: JWT 토큰
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 후 인터셉터 (Optional)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // 에러 처리 예: 인증 실패 시 로그아웃
    if (error.response && error.response.status === 401) {
      console.error("Unauthorized! Redirecting to login...");
      // 로그아웃 또는 리다이렉션 로직 추가
    }
    return Promise.reject(error);
  }
);

export default apiClient;
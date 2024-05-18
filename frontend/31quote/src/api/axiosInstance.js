import axios from "axios";

const backendApi = axios.create({
  baseURL: 'http://localhost:5051/api/v1'
})

backendApi.interceptors.request.use(
  (config) => {
    console.log('엑세스 토큰 검증')
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

// 리프레시 토큰으로 새로운 액세스 토큰을 요청하는 함수
const refreshAccessToken = async () => {
  console.log('리프레시!')
  const refreshToken = localStorage.getItem('refreshToken');
  const accessToken = localStorage.getItem('accessToken')
  try {
    console.log(refreshToken)
    console.log(accessToken)
    const response = await axios.post('http://localhost:5051/api/v1/user/refresh',
                                      { access_token : accessToken, refresh_token : refreshToken });
    const newAccessToken = response.data.access_token;
    localStorage.setItem('accessToken', newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error('Failed to refresh access token:', error);
    return null;
  }
};

// 응답 인터셉터 추가
backendApi.interceptors.response.use(
  (response) => {
    console.log("리스폰 응답")
    return response;
  },
  async (error) => {
    console.log("에러 응답")
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      // 재시도 플래그로 무한 루프 방지
      originalRequest._retry = true;
      const newAccessToken = await refreshAccessToken();
      if (newAccessToken) {
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);

export default backendApi
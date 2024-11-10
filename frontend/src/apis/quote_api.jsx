import apiClient from "./basic_api";

// 사용자 로그인
export const login = async (email, password) => {
  const response = await apiClient.post("/user/login", { email, password });
  return response.data;
};

// 사용자 프로필 가져오기
export const getUserProfile = async () => {
  const response = await apiClient.get("/user/profile");

  return response.data;
};

// 사용자 목록 가져오기
export const getUsers = async () => {
  const response = await apiClient.get("/users");
  return response.data;
};

export const getAllRandomQuote = async () => {
  const response = await apiClient.get("/quote/all_random");
  if (response.status != 200) {
    console.log("동작 안함 ㅋㅋ")
  }
  return response
}

export const getCategoryRandomQuote = async () => {
  const response = await apiClient.get("/quote/category_random");
  return response.data;
}

export const getCategoryListRnadomQuote = async () => {
  const response = await apiClient.get("/quote/category_list_random");
  return response.data;
}
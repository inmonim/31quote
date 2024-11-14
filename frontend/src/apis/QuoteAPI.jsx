import apiClient from "./BasicAPI";

export const getAllRandomQuote = async () => {
  const response = await apiClient.get("/quote/all_random");
  return response
}

export const getCategoryRandomQuote = async () => {
  const response = await apiClient.get("/quote/category_random");
  return response
}

export const getCategoryListRnadomQuote = async (categoryIds) => {
  const response = await apiClient.get("/quote/category_list_random", {
    params : {
      category_ids : categoryIds
    }
  })
  return response
}

export const getCategoryList = async () => {
  const response = await apiClient.get("/category/category_list");
  return response
}
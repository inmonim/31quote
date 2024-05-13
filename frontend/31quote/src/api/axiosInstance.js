import axios from "axios";

const backendApi = axios.create({
  baseURL: 'http://localhost:5051/api/v1'
})

export default backendApi
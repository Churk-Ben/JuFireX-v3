import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  timeout: Number(import.meta.env.VITE_TIMEOUT || 5000),
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => Promise.reject(err)
)

export default http
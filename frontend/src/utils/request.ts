import axios from 'axios'

declare global {
  interface ImportMetaEnv {
    readonly VITE_API_BASE?: string
    readonly VITE_TIMEOUT?: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  timeout: Number(import.meta.env.VITE_TIMEOUT || 5000),
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => Promise.reject(err)
)

export default http
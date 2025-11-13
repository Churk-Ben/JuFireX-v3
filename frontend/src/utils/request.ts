import axios, { AxiosError, AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

declare global {
  interface ImportMetaEnv {
    readonly VITE_API_BASE?: string
    readonly VITE_TIMEOUT?: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}

// 创建axios实例
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: Number(import.meta.env.VITE_TIMEOUT || 10000),
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    // 添加认证token
    const token = getAuthToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 请求日志
    console.log('🚀 HTTP请求', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      headers: config.headers,
      data: config.data,
      timestamp: new Date().toISOString()
    })

    return config
  },
  (error) => {
    console.error('❌ 请求拦截器错误', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>): ApiResponse => {
    // 响应日志
    console.log('✅ HTTP响应', {
      status: response.status,
      statusText: response.statusText,
      url: response.config.url,
      data: response.data,
      timestamp: new Date().toISOString()
    })

    // 检查业务状态码
    if (response.data && response.data.code !== undefined) {
      if (response.data.code === 401) {
        // 未授权，清除token并跳转到登录页
        clearAuthToken()
        window.location.href = '/login'
        throw new Error('未授权访问')
      }
      
      if (response.data.code !== 200) {
        console.warn('⚠️ 业务错误', {
          code: response.data.code,
          message: response.data.message,
          url: response.config.url
        })
      }
    }

    return response.data
  },
  (error: AxiosError) => {
    // 错误日志
    console.error('❌ HTTP响应错误', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      message: error.message,
      data: error.response?.data,
      timestamp: new Date().toISOString()
    })

    // 处理网络错误
    if (!error.response) {
      console.error('🌐 网络连接错误', error.message)
      return Promise.reject(new Error('网络连接失败，请检查网络设置'))
    }

    // 处理HTTP状态码错误
    const status = error.response.status
    switch (status) {
      case 400:
        return Promise.reject(new Error('请求参数错误'))
      case 401:
        clearAuthToken()
        window.location.href = '/login'
        return Promise.reject(new Error('未授权访问'))
      case 403:
        return Promise.reject(new Error('权限不足'))
      case 404:
        return Promise.reject(new Error('请求的资源不存在'))
      case 500:
        return Promise.reject(new Error('服务器内部错误'))
      case 502:
        return Promise.reject(new Error('网关错误'))
      case 503:
        return Promise.reject(new Error('服务暂时不可用'))
      default:
        return Promise.reject(new Error(`请求失败 (${status})`))
    }
  }
)

// Token管理函数
function getAuthToken(): string | null {
  // 优先从localStorage获取
  const token = localStorage.getItem('auth_token')
  if (token) {
    return token
  }
  
  // 从cookie获取
  const cookies = document.cookie.split(';')
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=')
    if (name === 'session_token') {
      return value
    }
  }
  
  return null
}

function setAuthToken(token: string): void {
  localStorage.setItem('auth_token', token)
  console.log('🔐 设置认证token', { 
    token: token.substring(0, 10) + '...', 
    timestamp: new Date().toISOString() 
  })
}

function clearAuthToken(): void {
  localStorage.removeItem('auth_token')
  // 清除cookie
  document.cookie = 'session_token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'
  console.log('🗑️ 清除认证token', { 
    timestamp: new Date().toISOString() 
  })
}

// 导出工具函数
export { setAuthToken, clearAuthToken, getAuthToken }
export default http
export type Maybe<T> = T | null | undefined

// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  nickname: string
  email: string
  avatar: string | null
  permission: number
  createdAt: string
  updatedAt: string
}

// 用户session信息接口
export interface UserSession {
  isLoggedIn: boolean
  user: UserInfo | null
}

// API响应基础接口
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}
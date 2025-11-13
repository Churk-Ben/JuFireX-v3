export type Maybe<T> = T | null | undefined

export type PermissionLevel = 0 | 1 | 2 | 3 | 4;

// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  nickname: string
  email?: string
  avatar: string | null
  permission: PermissionLevel
  createdAt?: string
  updatedAt?: string
  created_at?: string
  updated_at?: string
}

// 用户session信息接口
export interface UserSession {
  isLoggedIn?: boolean
  is_authenticated?: boolean
  user: UserInfo | null
  session?: {
    token: string | null
    created_at: string | null
    expires_at: string | null
  } | null
}

// API响应基础接口
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 认证相关响应类型
export interface LoginData {
  token: string
  user: Pick<UserInfo, 'id' | 'username' | 'nickname' | 'avatar' | 'permission'>
  expires_at: string
}

export interface RefreshData {
  token: string
  expires_at: string
  refreshed_at: string
}

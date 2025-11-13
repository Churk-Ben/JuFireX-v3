import http from "@/utils/request";
import type { UserSession, UserInfo, ApiResponse, LoginData, RefreshData } from "@/types";

// 用户注册接口
export async function register(userData: {
  username: string;
  nickname: string;
  email: string;
  password: string;
  avatar?: string;
  permission?: number;
}): Promise<ApiResponse<UserInfo>> {
  return await http.post("/auth/register", userData);
}

// 获取当前用户session信息
export async function getUserSession(): Promise<ApiResponse<UserSession>> {
  return await http.get("/user/session");
}

// 获取用户详细信息
export async function getUserInfo(): Promise<ApiResponse<UserInfo>> {
  return await http.get("/user/info");
}

// 用户登录
export async function login(credentials: {
  username: string;
  password: string;
}): Promise<ApiResponse<LoginData>> {
  return await http.post("/auth/login", credentials);
}

// 用户登出
export async function logout(): Promise<ApiResponse<null>> {
  return await http.post("/auth/logout");
}

// 检查登录状态
export async function checkAuthStatus(): Promise<ApiResponse<UserSession>> {
  return await http.get("/auth/status");
}

// 刷新会话令牌
export async function refreshToken(): Promise<ApiResponse<RefreshData>> {
  return await http.post("/auth/refresh");
}

// 验证令牌
export async function validateToken(token: string): Promise<ApiResponse<UserSession>> {
  return await http.post("/auth/validate", { token });
}

import http from "@/utils/request";
import type { UserSession, UserInfo, ApiResponse } from "@/types";

// 获取当前用户session信息
export async function getUserSession(): Promise<ApiResponse<UserSession>> {
  return await http.get("/api/user/session");
}

// 获取用户详细信息
export async function getUserInfo(): Promise<ApiResponse<UserInfo>> {
  return await http.get("/api/user/info");
}

// 用户登录
export async function login(credentials: {
  username: string;
  password: string;
}): Promise<ApiResponse<UserInfo>> {
  return await http.post("/api/auth/login", credentials);
}

// 用户登出
export async function logout(): Promise<ApiResponse<null>> {
  return await http.post("/api/auth/logout");
}

// 检查登录状态
export async function checkAuthStatus(): Promise<ApiResponse<UserSession>> {
  return await http.get("/api/auth/status");
}
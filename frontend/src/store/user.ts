import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, UserSession } from '@/types'
import { getUserSession, getUserInfo, login, logout, checkAuthStatus } from '@/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref<UserInfo | null>(null)
  const isLoggedIn = ref<boolean>(false)
  const isLoading = ref<boolean>(false)

  // 计算属性
  const nickname = computed(() => userInfo.value?.nickname || '')
  const avatar = computed(() => userInfo.value?.avatar || null)
  const permission = computed(() => userInfo.value?.permission || 0)
  const username = computed(() => userInfo.value?.username || '')

  // 初始化用户状态
  async function initUserState() {
    isLoading.value = true
    try {
      const response = await checkAuthStatus()
      if (response.code === 200 && response.data) {
        isLoggedIn.value = response.data.isLoggedIn
        userInfo.value = response.data.user
      } else {
        // 如果检查失败，清除状态
        clearUserState()
      }
    } catch (error) {
      console.error('检查用户状态失败:', error)
      clearUserState()
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户session信息
  async function fetchUserSession() {
    isLoading.value = true
    try {
      const response = await getUserSession()
      if (response.code === 200 && response.data) {
        isLoggedIn.value = response.data.isLoggedIn
        userInfo.value = response.data.user
        return response.data
      } else {
        throw new Error(response.message || '获取用户session失败')
      }
    } catch (error) {
      console.error('获取用户session失败:', error)
      clearUserState()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户详细信息
  async function fetchUserInfo() {
    if (!isLoggedIn.value) return null
    
    isLoading.value = true
    try {
      const response = await getUserInfo()
      if (response.code === 200 && response.data) {
        userInfo.value = response.data
        return response.data
      } else {
        throw new Error(response.message || '获取用户信息失败')
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 用户登录
  async function userLogin(credentials: { username: string; password: string }) {
    isLoading.value = true
    try {
      const response = await login(credentials)
      if (response.code === 200 && response.data) {
        isLoggedIn.value = true
        userInfo.value = response.data
        return response.data
      } else {
        throw new Error(response.message || '登录失败')
      }
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 用户登出
  async function userLogout() {
    isLoading.value = true
    try {
      const response = await logout()
      if (response.code === 200) {
        clearUserState()
      } else {
        throw new Error(response.message || '登出失败')
      }
    } catch (error) {
      console.error('登出失败:', error)
      // 即使登出请求失败，也清除本地状态
      clearUserState()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 清除用户状态
  function clearUserState() {
    isLoggedIn.value = false
    userInfo.value = null
  }

  // 更新用户信息
  function updateUserInfo(newUserInfo: Partial<UserInfo>) {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...newUserInfo }
    }
  }

  return {
    // 状态
    userInfo,
    isLoggedIn,
    isLoading,
    
    // 计算属性
    nickname,
    avatar,
    permission,
    username,
    
    // 方法
    initUserState,
    fetchUserSession,
    fetchUserInfo,
    userLogin,
    userLogout,
    clearUserState,
    updateUserInfo
  }
})
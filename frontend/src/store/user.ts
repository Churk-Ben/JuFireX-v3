import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, UserSession, LoginData } from '@/types'
import { getUserSession, getUserInfo, login, logout, checkAuthStatus } from '@/api/user'
import { setAuthToken, clearAuthToken, getAuthToken } from '@/utils/request'

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
      console.log('🔄 初始化用户状态', {
        timestamp: new Date().toISOString()
      })

      const token = getAuthToken()
      if (!token) {
        clearUserState()
        return
      }
      const response = await checkAuthStatus()
      if (response.code === 200 && response.data) {
        isLoggedIn.value = Boolean(response.data.isLoggedIn ?? response.data.is_authenticated)
        userInfo.value = response.data.user
        
        console.log('✅ 用户状态初始化成功', {
          isLoggedIn: isLoggedIn.value,
          user: userInfo.value,
          timestamp: new Date().toISOString()
        })
      } else {
        // 如果检查失败，清除状态
        clearUserState()
        console.log('⚠️ 用户未登录或状态检查失败', {
          response,
          timestamp: new Date().toISOString()
        })
      }
    } catch (error) {
      console.error('❌ 检查用户状态失败', {
        error: error,
        timestamp: new Date().toISOString()
      })
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
        isLoggedIn.value = Boolean(response.data.user)
        userInfo.value = response.data.user
        
        console.log('✅ 获取用户session成功', {
          session: response.data,
          timestamp: new Date().toISOString()
        })
        
        return response.data
      } else {
        throw new Error(response.message || '获取用户session失败')
      }
    } catch (error: any) {
      console.error('❌ 获取用户session失败', {
        error: error.message || error,
        timestamp: new Date().toISOString()
      })
      clearUserState()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户详细信息
  async function fetchUserInfo() {
    isLoading.value = true
    try {
      const response = await getUserInfo()
      if (response.code === 200 && response.data) {
        userInfo.value = response.data
        
        console.log('✅ 获取用户信息成功', {
          user: response.data,
          timestamp: new Date().toISOString()
        })
        
        return response.data
      } else {
        throw new Error(response.message || '获取用户信息失败')
      }
    } catch (error: any) {
      console.error('❌ 获取用户信息失败', {
        error: error.message || error,
        timestamp: new Date().toISOString()
      })
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 用户登录
  async function userLogin(credentials: { username: string; password: string }) {
    isLoading.value = true
    try {
      console.log('🚀 开始用户登录', {
        username: credentials.username,
        timestamp: new Date().toISOString()
      })

      const response = await login(credentials)
      if (response.code === 200 && response.data) {
        isLoggedIn.value = true
        const data = response.data as LoginData
        userInfo.value = data.user as unknown as UserInfo
        setAuthToken(data.token)
        
        console.log('✅ 用户登录成功', {
          user: response.data,
          timestamp: new Date().toISOString()
        })
        
        return data.user
      } else {
        throw new Error(response.message || '登录失败')
      }
    } catch (error: any) {
      console.error('❌ 用户登录失败', {
        error: error.message || error,
        username: credentials.username,
        timestamp: new Date().toISOString()
      })
      clearUserState()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 用户登出
  async function userLogout() {
    isLoading.value = true
    try {
      console.log('🚪 开始用户登出', {
        username: userInfo.value?.username,
        timestamp: new Date().toISOString()
      })

      const response = await logout()
      if (response.code === 200) {
        console.log('✅ 用户登出成功', {
          timestamp: new Date().toISOString()
        })
      } else {
        console.warn('⚠️ 登出响应异常', {
          response,
          timestamp: new Date().toISOString()
        })
      }
    } catch (error: any) {
      console.error('❌ 用户登出失败', {
        error: error.message || error,
        timestamp: new Date().toISOString()
      })
    } finally {
      // 无论登出API是否成功，都清除本地状态
      clearUserState()
      isLoading.value = false
    }
  }

  // 清除用户状态
  function clearUserState() {
    isLoggedIn.value = false
    userInfo.value = null
    clearAuthToken()
    
    console.log('🗑️ 清除用户状态', {
      timestamp: new Date().toISOString()
    })
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

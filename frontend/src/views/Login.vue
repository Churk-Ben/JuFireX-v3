<template>
  <div class="login-container d-flex align-items-center justify-content-center min-vh-100">
    <n-card embedded title="登录" class="col-12 col-md-6 col-lg-4 mx-auto">
      <!-- 登录表单 -->
      <n-form ref="formRef" :model="modelRef" :rules="rules" @submit.prevent="handleLogin">
        <n-form-item path="username" label="用户名">
          <n-input 
            v-model:value="modelRef.username" 
            placeholder="请输入用户名" 
            :disabled="isLoading"
            @keydown.enter.prevent="handleLogin" 
          />
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input 
            v-model:value="modelRef.password" 
            type="password" 
            placeholder="请输入密码" 
            :disabled="isLoading"
            @keydown.enter.prevent="handleLogin" 
          />
        </n-form-item>
      </n-form>

      <!-- 底部链接 -->
      <template #footer>
        <p class="mb-0 text-center">
          还没有账号？
          <router-link to="/register" class="text-decoration-none">立即注册</router-link>
        </p>
      </template>

      <template #action>
        <n-button 
          type="primary" 
          block 
          size="large" 
          :loading="isLoading"
          :disabled="isLoading"
          @click="handleLogin"
        >
          <i class="fas fa-sign-in-alt me-2"></i>
          {{ isLoading ? '登录中...' : '登录' }}
        </n-button>
      </template>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'
import { NButton, NCard, NForm, NFormItem, NInput } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

interface ModelType {
  username: string | null
  password: string | null
}

const formRef = ref<FormInst | null>(null)
const message = useMessage()
const router = useRouter()
const userStore = useUserStore()

const modelRef = ref<ModelType>({
  username: null,
  password: null
})

// 从store获取loading状态
const isLoading = computed(() => userStore.isLoading)

const rules: FormRules = {
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: ['input', 'blur']
    },
    {
      min: 3,
      max: 50,
      message: '用户名长度应在3-50个字符之间',
      trigger: ['input', 'blur']
    }
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: ['input', 'blur']
    },
    {
      min: 6,
      message: '密码长度至少6个字符',
      trigger: ['input', 'blur']
    }
  ]
}

async function handleLogin() {
  try {
    // 表单验证
    await formRef.value?.validate()
    
    if (!modelRef.value.username || !modelRef.value.password) {
      message.error('请填写完整的登录信息')
      return
    }

    console.log('🚀 开始登录流程', {
      username: modelRef.value.username,
      timestamp: new Date().toISOString()
    })

    // 调用用户store进行登录
    const result = await userStore.userLogin({
      username: modelRef.value.username,
      password: modelRef.value.password
    })

    console.log('✅ 登录成功', {
      user: result,
      timestamp: new Date().toISOString()
    })

    message.success(`欢迎回来，${result.nickname || result.username}！`)
    
    // 登录成功后跳转到首页
    await router.push('/')
    
  } catch (error: any) {
    console.error('❌ 登录失败', {
      error: error.message || error,
      username: modelRef.value.username,
      timestamp: new Date().toISOString()
    })
    
    message.error(error.message || '登录失败，请检查用户名和密码')
  }
}
</script>
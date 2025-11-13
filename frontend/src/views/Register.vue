<template>
  <div class="register-container d-flex align-items-center justify-content-center min-vh-100">
    <n-card embedded title="用户注册" class="col-12 col-md-8 col-lg-6 mx-auto">
      <!-- 注册步骤指示器 -->
      <n-steps :current="currentStep" :status="stepStatus" class="mb-4">
        <n-step title="基本信息" description="填写用户名、昵称和邮箱" />
        <n-step title="设置密码" description="设置安全的登录密码" />
        <n-step title="完成注册" description="确认信息并完成注册" />
      </n-steps>

      <!-- 步骤1: 基本信息 -->
      <div v-if="currentStep === 0">
        <n-form ref="basicFormRef" :model="registerForm" :rules="basicRules">
          <n-form-item path="username" label="用户名">
            <n-input 
              v-model:value="registerForm.username" 
              placeholder="请输入用户名（3-50个字符）"
              :disabled="isLoading"
            />
          </n-form-item>
          <n-form-item path="nickname" label="昵称">
            <n-input 
              v-model:value="registerForm.nickname" 
              placeholder="请输入昵称"
              :disabled="isLoading"
            />
          </n-form-item>
          <n-form-item path="email" label="邮箱">
            <n-input 
              v-model:value="registerForm.email" 
              placeholder="请输入邮箱地址"
              :disabled="isLoading"
            />
          </n-form-item>
        </n-form>
      </div>

      <!-- 步骤2: 设置密码 -->
      <div v-if="currentStep === 1">
        <n-form ref="passwordFormRef" :model="registerForm" :rules="passwordRules">
          <n-form-item path="password" label="密码">
            <n-input 
              v-model:value="registerForm.password" 
              type="password"
              placeholder="请输入密码（至少6个字符）"
              :disabled="isLoading"
            />
          </n-form-item>
          <n-form-item path="confirmPassword" label="确认密码">
            <n-input 
              v-model:value="registerForm.confirmPassword" 
              type="password"
              placeholder="请再次输入密码"
              :disabled="isLoading"
            />
          </n-form-item>
        </n-form>
      </div>

      <!-- 步骤3: 确认信息 -->
      <div v-if="currentStep === 2">
        <n-descriptions title="注册信息确认" bordered :column="1">
          <n-descriptions-item label="用户名">{{ registerForm.username }}</n-descriptions-item>
          <n-descriptions-item label="昵称">{{ registerForm.nickname }}</n-descriptions-item>
          <n-descriptions-item label="邮箱">{{ registerForm.email }}</n-descriptions-item>
        </n-descriptions>
      </div>

      <!-- 操作按钮 -->
      <template #action>
        <n-space justify="space-between">
          <n-button 
            v-if="currentStep > 0" 
            @click="prevStep"
            :disabled="isLoading"
          >
            <i class="fas fa-arrow-left me-2"></i>
            上一步
          </n-button>
          <div v-else></div>

          <n-button 
            v-if="currentStep < 2" 
            type="primary" 
            @click="nextStep"
            :disabled="isLoading"
          >
            下一步
            <i class="fas fa-arrow-right ms-2"></i>
          </n-button>
          <n-button 
            v-else 
            type="primary" 
            :loading="isLoading"
            :disabled="isLoading"
            @click="handleRegister"
          >
            <i class="fas fa-user-plus me-2"></i>
            {{ isLoading ? '注册中...' : '完成注册' }}
          </n-button>
        </n-space>
      </template>

      <!-- 底部链接 -->
      <template #footer>
        <p class="mb-0 text-center">
          已有账号？
          <router-link to="/login" class="text-decoration-none">立即登录</router-link>
        </p>
      </template>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import type { FormInst, FormRules } from 'naive-ui'
import { 
  NButton, 
  NCard, 
  NForm, 
  NFormItem, 
  NInput, 
  NSteps, 
  NStep, 
  NSpace,
  NDescriptions,
  NDescriptionsItem
} from 'naive-ui'
import { useMessage } from 'naive-ui'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/user'

interface RegisterForm {
  username: string
  nickname: string
  email: string
  password: string
  confirmPassword: string
}

const basicFormRef = ref<FormInst | null>(null)
const passwordFormRef = ref<FormInst | null>(null)
const message = useMessage()
const router = useRouter()

const currentStep = ref(0)
const stepStatus = ref<'process' | 'finish' | 'error' | 'wait'>('process')
const isLoading = ref(false)

const registerForm = ref<RegisterForm>({
  username: '',
  nickname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 基本信息验证规则
const basicRules: FormRules = {
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
    },
    {
      pattern: /^[a-zA-Z0-9_]+$/,
      message: '用户名只能包含字母、数字和下划线',
      trigger: ['input', 'blur']
    }
  ],
  nickname: [
    {
      required: true,
      message: '请输入昵称',
      trigger: ['input', 'blur']
    },
    {
      min: 1,
      max: 100,
      message: '昵称长度应在1-100个字符之间',
      trigger: ['input', 'blur']
    }
  ],
  email: [
    {
      required: true,
      message: '请输入邮箱地址',
      trigger: ['input', 'blur']
    },
    {
      type: 'email',
      message: '请输入有效的邮箱地址',
      trigger: ['input', 'blur']
    }
  ]
}

// 密码验证规则
const passwordRules: FormRules = {
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
  ],
  confirmPassword: [
    {
      required: true,
      message: '请确认密码',
      trigger: ['input', 'blur']
    },
    {
      validator: (rule, value) => {
        return value === registerForm.value.password
      },
      message: '两次输入的密码不一致',
      trigger: ['input', 'blur']
    }
  ]
}

async function nextStep() {
  try {
    if (currentStep.value === 0) {
      // 验证基本信息
      await basicFormRef.value?.validate()
    } else if (currentStep.value === 1) {
      // 验证密码
      await passwordFormRef.value?.validate()
    }
    
    currentStep.value++
    console.log('📝 进入下一步', {
      step: currentStep.value,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('❌ 表单验证失败', error)
    message.error('请检查表单信息')
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
    console.log('📝 返回上一步', {
      step: currentStep.value,
      timestamp: new Date().toISOString()
    })
  }
}

async function handleRegister() {
  try {
    isLoading.value = true
    
    console.log('🚀 开始注册流程', {
      username: registerForm.value.username,
      email: registerForm.value.email,
      timestamp: new Date().toISOString()
    })

    // 调用注册API
    const response = await register({
      username: registerForm.value.username,
      nickname: registerForm.value.nickname,
      email: registerForm.value.email,
      password: registerForm.value.password,
      avatar: '/static/avatars/default.jpg', // 默认头像
      permission: 1 // 默认权限
    })
    
    if (response.code === 200) {
      console.log('✅ 注册成功', {
        user: response.data,
        timestamp: new Date().toISOString()
      })

      message.success(`注册成功！欢迎 ${response.data.nickname}`)
      stepStatus.value = 'finish'
      
      // 注册成功后跳转到登录页
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      throw new Error(response.message || '注册失败')
    }
    
  } catch (error: any) {
    console.error('❌ 注册失败', {
      error: error.message || error,
      username: registerForm.value.username,
      timestamp: new Date().toISOString()
    })
    
    message.error(error.message || '注册失败，请稍后重试')
    stepStatus.value = 'error'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
<template>
  <div class="not-found-container d-flex align-items-center justify-content-center min-vh-100">
    <n-card embedded class="text-center col-12 col-md-6 col-lg-4">
      <div class="error-content">
        <div class="error-code mb-4">
          <i class="fas fa-exclamation-triangle text-warning" style="font-size: 4rem;"></i>
          <h1 class="display-1 fw-bold text-primary mt-3">404</h1>
        </div>
        
        <h2 class="h4 mb-3">页面未找到</h2>
        <p class="text-muted mb-4">
          抱歉，您访问的页面不存在或已被移动。
        </p>
        
        <n-space justify="center" class="mb-3">
          <n-button type="primary" @click="goHome">
            <i class="fas fa-home me-2"></i>
            返回首页
          </n-button>
          <n-button @click="goBack">
            <i class="fas fa-arrow-left me-2"></i>
            返回上页
          </n-button>
        </n-space>
        
        <p class="small text-muted">
          如果您认为这是一个错误，请
          <router-link to="/contact" class="text-decoration-none">联系我们</router-link>
        </p>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { NCard, NButton, NSpace } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  console.log('🏠 返回首页', {
    timestamp: new Date().toISOString()
  })
  router.push('/')
}

function goBack() {
  console.log('⬅️ 返回上页', {
    timestamp: new Date().toISOString()
  })
  router.back()
}
</script>

<style scoped>
.not-found-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.error-content {
  padding: 2rem 1rem;
}

.error-code {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>
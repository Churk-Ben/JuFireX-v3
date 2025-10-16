<template>
  <Transition name="loading-fade" appear>
    <div v-if="isLoading" class="loading-screen">
      <div class="loading-content">
        <div class="logo-container">
          <img src="/logo.svg" alt="JuFireX" class="logo" />
        </div>
        <div class="loading-spinner">
          <n-spin size="large" />
        </div>
        <div class="loading-text">
          <h3>JuFireX</h3>
          <p>正在加载中...</p>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { NSpin } from 'naive-ui'

interface Props {
  isLoading: boolean
}

defineProps<Props>()
</script>

<style scoped>
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #202020 0%, #2a2a2a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(10px);
}

.loading-content {
  text-align: center;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  width: 80px;
  height: 80px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  animation: float 3s ease-in-out infinite;
}

.loading-spinner {
  margin: 2rem 0;
}

.loading-text h3 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #0d6efd, #42a5f5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.loading-text p {
  font-size: 1rem;
  opacity: 0.8;
  margin: 0;
}

/* 过渡动画 */
.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.loading-fade-enter-from {
  opacity: 0;
}

.loading-fade-leave-to {
  opacity: 0;
}

/* 浮动动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logo {
    width: 60px;
    height: 60px;
  }
  
  .loading-text h3 {
    font-size: 1.5rem;
  }
  
  .loading-text p {
    font-size: 0.9rem;
  }
}
</style>
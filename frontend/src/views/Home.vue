<template>
  <!-- 海报栏 -->
  <section class="hero-section">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-6">
          <h1 class="display-4 fw-bold mb-4">
            <span v-if="userStore.isLoggedIn">
              欢迎回来，{{ userStore.nickname }}！
            </span>
            <span v-else>
              爝火工作室
            </span>
          </h1>
          <p class="lead mb-4" v-if="userStore.isLoggedIn">
            很高兴再次见到您！探索我们的最新项目和功能。
          </p>
          <p class="lead mb-4" v-else>
            我们是一个专注于前端开发的团队，致力于为客户提供高质量的服务。
          </p>

          <div class="d-flex gap-3">
            <router-link 
              v-if="userStore.isLoggedIn" 
              to="/project" 
              class="btn btn-primary btn-lg"
            >
              <i class="fas fa-folder-open me-2"></i>
              我的项目
            </router-link>
            <a v-else href="#projects" class="btn btn-primary btn-lg">
              <i class="fas fa-eye me-2"></i>
              查看项目
            </a>
            
            <router-link 
              v-if="userStore.isLoggedIn" 
              to="/profile" 
              class="btn btn-outline-secondary btn-lg"
            >
              <i class="fas fa-user me-2"></i>
              个人资料
            </router-link>
            <a v-else href="#contact" class="btn btn-outline-secondary btn-lg">
              <i class="fas fa-envelope me-2"></i>
              联系我们
            </a>
          </div>
        </div>
        <div class="col-lg-6 text-center">
          <div class="p-5">
            <div v-if="userStore.isLoggedIn" class="user-welcome">
              <div class="avatar-container mb-3 d-flex justify-content-center">
                <img 
                  v-if="userStore.avatar" 
                  :src="userStore.avatar" 
                  :alt="userStore.nickname"
                  class="rounded-circle"
                  style="width: 120px; height: 120px; object-fit: cover;"
                />
                <div 
                  v-else 
                  class="avatar-placeholder rounded-circle d-flex align-items-center justify-content-center"
                  style="width: 120px; height: 120px; background: linear-gradient(45deg, #0d6efd, #42a5f5);"
                >
                  <i class="fas fa-user text-white" style="font-size: 3rem;"></i>
                </div>
              </div>
              <h3 class="h4 mb-2">{{ userStore.nickname }}</h3>
              <p class="text-muted">
                <i class="fas fa-shield-alt me-1"></i>
                权限等级: {{ getPermissionText(userStore.permission) }}
              </p>
            </div>
            <div v-else>
              <i class="fas fa-fire" style="font-size: 8rem; color: var(--bs-primary)"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 项目展示 -->
  <section id="projects" class="project-section py-5">
    <div class="container">
      <div class="row mb-5">
        <div class="col-12 text-center">
          <h2 class="h1 mb-3">精选项目</h2>
          <p class="lead text-muted">展示我们最新和最受欢迎的项目</p>
        </div>
      </div>

      <div class="row">
        <div class="col-12 text-center">
          <div class="py-5">
            <i class="fas fa-folder-open" style="font-size: 4rem; color: #6c757d"></i>
            <h3 class="mt-3 text-muted">暂无项目</h3>
            <p class="text-muted">工作室项目正在筹备中, 敬请期待！</p>
            <router-link 
              v-if="userStore.isLoggedIn && userStore.permission >= 2" 
              to="/admin/project" 
              class="btn btn-outline-primary mt-3"
            >
              <i class="fas fa-plus me-2"></i>
              添加项目
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 统计信息 -->
  <section class="py-5 bg-light">
    <div class="container">
      <div class="row text-center">
        <div class="col-md-3 col-6 mb-4">
          <div class="p-3">
            <i class="fas fa-code" style="font-size: 2.5rem; color: #0d6efd"></i>
            <h3 class="mt-2 mb-0">0</h3>
            <p class="text-muted mb-0">项目数量</p>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-4">
          <div class="p-3">
            <i class="fas fa-users" style="font-size: 2.5rem; color: #198754"></i>
            <h3 class="mt-2 mb-0">5+</h3>
            <p class="text-muted mb-0">团队成员</p>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-4">
          <div class="p-3">
            <i class="fas fa-star" style="font-size: 2.5rem; color: #ffd700"></i>
            <h3 class="mt-2 mb-0">100+</h3>
            <p class="text-muted mb-0">GitHub 星标</p>
          </div>
        </div>
        <div class="col-md-3 col-6 mb-4">
          <div class="p-3">
            <i class="fas fa-download" style="font-size: 2.5rem; color: #dc3545"></i>
            <h3 class="mt-2 mb-0">1000+</h3>
            <p class="text-muted mb-0">下载次数</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 联系信息 -->
  <section id="contact" class="py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 text-center">
          <h2 class="mb-4">联系我们</h2>
          <p class="lead mb-4">有任何问题或合作意向, 欢迎随时联系我们</p>

          <div class="row g-4">
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-body">
                  <i class="fas fa-envelope" style="font-size: 2rem; color: #0d6efd"></i>
                  <h5 class="mt-3">邮箱联系</h5>
                  <p class="text-muted">
                    contact@jufire.studio
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100">
                <div class="card-body">
                  <i class="fab fa-github" style="font-size: 2rem; color: #0d6efd"></i>
                  <h5 class="mt-3">GitHub</h5>
                  <p class="text-muted">
                    github.com/jufirex
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/user'
import { onMounted } from 'vue'

const userStore = useUserStore()

// 权限等级文本映射
function getPermissionText(level: number): string {
  const permissionMap: Record<number, string> = {
    0: '游客',
    1: '普通用户',
    2: '管理员',
    3: '超级管理员'
  }
  return permissionMap[level] || '未知'
}

onMounted(() => {
  console.log('🏠 首页加载完成', {
    isLoggedIn: userStore.isLoggedIn,
    user: userStore.userInfo,
    timestamp: new Date().toISOString()
  })
})
</script>

<style scoped>
.hero-section {
  display: flex;
  align-items: center;
  min-height: 60vh;
  background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
  color: white;
}

.project-section {
  min-height: 50vh;
}

.user-welcome {
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.avatar-container {
  position: relative;
}

.avatar-placeholder {
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}
</style>
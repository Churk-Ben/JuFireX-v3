<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      <RouterLink class="navbar-brand" to="/">
        <i class="fas fa-fire me-1"></i>JuFire Studio
      </RouterLink>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" style="margin: 0 5px">
            <RouterLink class="nav-link" to="/">首页</RouterLink>
          </li>
          <!-- 可根据需要添加更多路由链接 -->
        </ul>

        <!-- 未接入认证系统前，展示登录/注册占位 -->
        <ul class="navbar-nav">
          <li class="nav-item" style="margin: 0 5px">
            <a class="nav-link" href="#">登录</a>
          </li>
          <li class="nav-item" style="margin: 0 5px">
            <a class="nav-link" href="#">注册</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<style scoped>
/* 导航栏 */
.navbar {
  background-color: var(--github-secondary) !important;
  border-bottom: 1px solid var(--github-border);
}

.navbar-brand,
.nav-link {
  color: var(--github-text) !important;
}

.nav-link:hover {
  color: var(--github-accent) !important;
}

.dropdown-menu {
  background-color: var(--github-secondary);
  border: 1px solid var(--github-border);
  padding: 0.25rem 0;
}

.dropdown-menu.show {
  padding: 0.25rem 0;
}

.dropdown-item {
  color: var(--github-text);
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  width: calc(100% - 0.5rem);
  box-sizing: border-box;
  display: block;
  transition: background-color 0.2s, color 0.2s;
}

.dropdown-item:hover {
  background-color: rgba(88, 166, 255, 0.2) !important;
  color: var(--github-accent) !important;
  border-radius: 3px;
  box-shadow: none !important;
  outline: none !important;
  margin: 0 0.25rem;
  width: calc(100% - 0.5rem);
}

.dropdown-divider {
  border-top: 1px solid var(--github-border);
  margin: 0.25rem 0;
}
</style>
<template>
  <n-config-provider :theme-overrides="themeOverrides" :theme="darkTheme">
    <n-global-style />
    <n-message-provider>
      <!-- 加载屏幕 -->
      <LoadingScreen :is-loading="isLoading" />
      
      <!-- 主应用内容 -->
      <Transition name="app-fade" appear>
        <div v-if="!isLoading" class="layout">
          <NavBar />
          <section class="content">
            <RouterView />
          </section>
          <AppFooter />
        </div>
      </Transition>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { RouterView } from "vue-router";
import {
  useOsTheme,
  lightTheme,
  darkTheme,
  NConfigProvider,
  NGlobalStyle,
  NMessageProvider,
  GlobalThemeOverrides,
} from 'naive-ui'

import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import LoadingScreen from "@/components/LoadingScreen.vue";

// 加载状态管理
const isLoading = ref(true);

// 模拟应用初始化过程
onMounted(async () => {
  try {
    // 等待DOM完全渲染
    await nextTick();
    
    // 模拟资源加载时间（可以根据实际需要调整）
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 确保所有异步操作完成后再隐藏加载屏幕
    isLoading.value = false;
    
    // 恢复body滚动
    document.body.classList.add('app-loaded');
  } catch (error) {
    console.error('应用初始化失败:', error);
    // 即使出错也要隐藏加载屏幕
    isLoading.value = false;
    document.body.classList.add('app-loaded');
  }
});

const themeOverrides: GlobalThemeOverrides = {
  common: {
    borderRadius: '6px',
    borderRadiusSmall: '4px',
    primaryColor: '#0d6efd',
    primaryColorHover: '#0a58ca',
    primaryColorPressed: '#084298',
    primaryColorSuppl: 'rgb(42, 148, 125)',
  },
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1 0 auto;
  padding: 20px;
}

/* 主应用过渡动画 */
.app-fade-enter-active,
.app-fade-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.app-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.app-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>

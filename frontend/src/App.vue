<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-global-style />
    <div class="layout">
      <NavBar />
      <section class="content">
        <RouterView />
      </section>
      <AppFooter />
    </div>
  </n-config-provider>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import {
  useOsTheme,
  lightTheme,
  darkTheme,
  NConfigProvider,
  NGlobalStyle,
  GlobalThemeOverrides,
} from 'naive-ui'

import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";

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
</style>

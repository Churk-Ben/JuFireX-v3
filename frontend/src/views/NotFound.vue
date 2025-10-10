<template>
  <main class="container">
    <h1>页面走丢了</h1>
    <RouterLink to="/">返回首页</RouterLink>
  </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.container { max-width: 720px; margin: 24px auto; padding: 0 12px; }
</style>
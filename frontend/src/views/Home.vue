<template>
  <main class="container">
    <h1>首页</h1>
    <nav class="nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/login">Login</RouterLink>
    </nav>

    <section>
      <h2>Posts</h2>
      <BaseButton @click="load">加载帖子</BaseButton>
      <ul>
        <li v-for="p in posts" :key="p.id">{{ p.title || '占位' }}</li>
      </ul>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { listPosts } from '@/api/post'
import BaseButton from '@/components/BaseButton.vue'

const posts = ref<any[]>([])
const load = async () => {
  const res = await listPosts()
  posts.value = res.data?.items || []
}
</script>

<style scoped>
.container { max-width: 720px; margin: 24px auto; padding: 0 12px; }
.nav { display:flex; gap:12px; margin-bottom: 18px; }
</style>
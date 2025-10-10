<template>
  <main class="container">
    <h1>登录</h1>
    <form @submit.prevent="onSubmit" class="form">
      <label>
        Email
        <input v-model="email" type="email" required />
      </label>
      <label>
        Password
        <input v-model="password" type="password" required />
      </label>
      <BaseButton type="submit">登录</BaseButton>
    </form>
    <p v-if="token">登录成功，token: {{ token }}</p>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { login } from '@/api/user'
import BaseButton from '@/components/BaseButton.vue'

const email = ref('test@example.com')
const password = ref('password')
const token = ref('')

async function onSubmit() {
  try {
    const res = await login(email.value, password.value)
    token.value = res.data?.token || ''
  } catch (e: any) {
    alert(e?.message || '登录失败')
  }
}
</script>

<style scoped>
.container { max-width: 480px; margin: 24px auto; padding: 0 12px; }
.form { display: grid; gap: 12px; }
.form input { padding: 8px; border:1px solid #ddd; border-radius: 6px; }
</style>
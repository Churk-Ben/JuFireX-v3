<template>
  <button class="base-button" :type="type" @click="$emit('click')">
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{ type?: 'button' | 'submit' | 'reset' }>()
</script>

<style scoped>
.base-button {
  padding: 8px 14px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}
.base-button:hover { background: #f7f7f7; }
</style>
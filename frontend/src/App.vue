<template>
  <div class="layout">
    <NavBar />
    <section class="content">
      <RouterView />
    </section>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1 0 auto;
  padding: 2em 5em;
}
</style>

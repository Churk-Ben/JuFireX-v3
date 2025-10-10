<template>
  <footer class="footer py-4">
    <div class="container">
      <div class="row">
        <div class="col-md-6 copyright">
          <p class="mb-0">&copy; 2025 JuFire Studio. All rights reserved.</p>
        </div>
        <div class="col-md-6 text-end">
          <a href="#" class="text-decoration-none me-3"><i class="fab fa-github me-2"></i>GitHub</a>
          <a href="#" class="text-decoration-none me-3"><i class="fas fa-envelope me-2"></i>Contact</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Static footer; replace links when backend profile data is available.
</script>

<style scoped>
/* 页脚 */
.footer {
  background-color: var(--github-secondary);
  border-top: 1px solid var(--github-border);
}

.copyright {
  color: #8b949e;
}
</style>
<template>
  <div v-if="open" class="modal-backdrop" @click="onBackdrop">
    <div class="modal" @click.stop>
      <header class="modal-header">
        <slot name="title">标题</slot>
        <button class="close" @click="emit('close')">×</button>
      </header>
      <section class="modal-body">
        <slot />
      </section>
      <footer class="modal-footer">
        <slot name="footer"></slot>
      </footer>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
const props = defineProps<{ open: boolean, closeOnBackdrop?: boolean }>()
const emit = defineEmits<{ (e: 'close'): void }>()
const onBackdrop = () => { if (props.closeOnBackdrop) emit('close') }
</script>

<style scoped>
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,.35);
  display: flex; align-items: center; justify-content: center;
}
.modal { width: 520px; background: #fff; border-radius: 8px; overflow: hidden; }
.modal-header { display:flex; justify-content:space-between; padding: 12px 16px; border-bottom:1px solid #eee; }
.modal-body { padding: 16px; }
.modal-footer { padding: 12px 16px; border-top:1px solid #eee; text-align: right; }
.close { border:none; background:transparent; cursor:pointer; font-size: 20px; }
</style>
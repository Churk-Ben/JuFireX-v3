<template>
  <n-space>
    <n-button>Default</n-button>
    <n-button type="tertiary">
      <i class="fas fa-info-circle me-1"></i>Tertiary
    </n-button>
    <n-button type="primary">
      Primary
    </n-button>
    <n-button type="info">
      Info
    </n-button>
    <n-button type="success">
      Success
    </n-button>
    <n-button type="warning">
      Warning
    </n-button>
    <n-button type="error">
      Error
    </n-button>
  </n-space>

  <n-space>
    <n-card title="卡片插槽示例">
      <template #header-extra>
        #header-extra
      </template>
      卡片内容
      <template #footer>
        #footer
      </template>
      <template #action>
        #action
      </template>
    </n-card>
  </n-space>

  <n-space>
    <n-avatar round size="small" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
    <n-avatar round size="medium" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
    <n-avatar round size="large" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
    <n-avatar round :size="48" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
    <n-avatar :style="{
      color: 'yellow',
      backgroundColor: 'red',
    }">
      M
    </n-avatar>
  </n-space>

</template>

<script setup lang="ts">
import { NButton, NSpace, NCard, NAvatar } from 'naive-ui'
</script>

<style scoped>
.n-space {
  margin-bottom: 20px;
}
</style>
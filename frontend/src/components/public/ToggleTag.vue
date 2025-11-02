<template>
  <n-tag 
    class="toggle" 
    ghost 
    round 
    :type="tagType"
    @click="handleClick"
    v-bind="$attrs"
  >
    <template #avatar>
      <slot name="avatar">
        <i v-if="icon" :class="icon"></i>
        <img v-else-if="avatarSrc" :src="avatarSrc" :alt="avatarAlt" />
      </slot>
    </template>
    <slot>{{ text }}</slot>
  </n-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NTag } from 'naive-ui'
import type { TagProps } from 'naive-ui'

interface Props {
  text?: string
  icon?: string
  avatarSrc?: string
  avatarAlt?: string
  permissionLevel?: 0 | 1 | 2 | 3 | 4 // 0:未登录, 1:游客, 2:成员, 3:管理员, 4:超级管理员
}

interface Emits {
  (e: 'click', event: MouseEvent): void
}

const props = withDefaults(defineProps<Props>(), {
  text: '',
  icon: '',
  avatarSrc: '',
  avatarAlt: '',
  permissionLevel: undefined
})

const emit = defineEmits<Emits>()

// 根据权限等级确定标签类型和颜色
const tagType = computed<TagProps['type']>(() => {
  if (props.permissionLevel === undefined) return 'default'
  
  switch (props.permissionLevel) {
    case 0: return 'default'     // 未登录 - 默认灰色
    case 1: return 'info'        // 游客 - 蓝色
    case 2: return 'success'     // 成员 - 绿色
    case 3: return 'warning'     // 管理员 - 橙色
    case 4: return 'error'       // 超级管理员 - 红色
    default: return 'default'
  }
})

function handleClick(event: MouseEvent) {
  emit('click', event)
}
</script>

<style scoped>
.toggle {
  display: flex;
  align-self: center;
  align-items: center;
  cursor: pointer;
}

.toggle :deep(i) {
  display: inline;
  font-size: 1.5em;
  margin: 0 -0.1em;
}

.toggle :deep(img) {
  width: 1.5em;
  border-radius: 50%;
}
</style>
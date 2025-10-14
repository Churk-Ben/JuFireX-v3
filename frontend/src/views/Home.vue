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

  <n-space>
    <n-tag>
      Anyway.FM
      <template #avatar>
        <n-avatar src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg" />
      </template>
    </n-tag>
    <n-tag round :bordered="false">
      Anyway.FM
      <template #avatar>
        <n-avatar src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg" />
      </template>
    </n-tag>
  </n-space>

  <n-space>
    <n-dropdown trigger="click" :options="options" @select="handleSelect">
      <n-button>点击！</n-button>
    </n-dropdown>
  </n-space>

</template>

<script setup lang="ts">
import { NButton, NSpace, NCard, NAvatar, NTag, NDropdown } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { ref } from 'vue'

const message = useMessage()
const showDropdown = ref(false)

const options = [
  {
    label: '首页',
    key: '/home'
  },
  {
    label: '导航',
    key: '/navigation'
  },
  {
    label: '项目',
    key: '/project'
  },
  {
    label: '设置',
    key: 'setting',
    children: [
      {
        label: '工作室',
        key: '/setting/studio'
      },
      {
        label: '个性化',
        key: '/setting/preference' // 仪表盘和主题等外观,展示设置
      },
      {
        label: '账户',
        key: '/setting/account' // 关乎账户信息,登录状态等
      },
      // divider
      {
        label: '退出登录',
        key: '/logout'
      }
    ]
  },
  {
    label: '管理',
    key: 'admin',
    children: [
      {
        label: '用户管理',
        key: '/admin/user'
      },
      {
        label: '项目管理',
        key: '/admin/project'
      },
      {
        label: '导航管理',
        key: '/admin/navigation'
      }
    ]
  }
]


function handleSelect(key: string | number) {
  message.info(String(key))
}
</script>

<style scoped>
.n-space {
  margin-bottom: 20px;
}
</style>
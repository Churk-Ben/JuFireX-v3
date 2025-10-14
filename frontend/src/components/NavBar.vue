<template>
  <n-flex>
    <n-card class="m-2">
      <div class="bar d-flex flex-row justify-content-between align-items-center">
        <div class="d-flex align-items-center">
          <router-link to="/" class="brand d-flex align-items-center mx-3">
            <img class="logo me-1" src="@/assets/logo.svg" alt="JuFireX" />
            <span class="name">JuFireX</span>
          </router-link>

          <div class="menu">
            <n-menu v-model:value="activeKey" mode="horizontal" :options="menuOptions" @update:value="handleMenuSelect"
              responsive />
          </div>
        </div>

        <div class="action">
          <n-space>
            <n-button ghost circle @click="handleThemeChange">
              <template #icon>
                <i class="fas fa-moon"></i>
              </template>
            </n-button>

            <n-tag v-if="false" ghost size="large" round>
              Aurore
              <template #avatar>
                <n-avatar src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg" />
              </template>
            </n-tag>

            <n-tag v-else ghost size="large" round>
              登录
              <template #avatar>
                <i class="fas fa-user-circle"></i>
              </template>
            </n-tag>
          </n-space>
        </div>
      </div>
    </n-card>
  </n-flex>
</template>

<script setup lang="ts">
import { NButton, NSpace, NMenu, NCard, NFlex, NTag, NAvatar } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useOsTheme, lightTheme, darkTheme } from 'naive-ui'

const message = useMessage()
const router = useRouter()
const activeKey = ref<string>('/')
const osTheme = useOsTheme()

// 主题切换
function handleThemeChange() {

}

// 主菜单选项
const menuOptions: MenuOption[] = [
  {
    label: '首页',
    key: '/'
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
      {
        type: 'divider',
        key: 'divider'
      },
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


// 处理主菜单选择
function handleMenuSelect(key: string) {
  activeKey.value = key
  if (key.startsWith('/')) {
    router.push(key)
  }
  message.info(`导航到: ${key}`)
}
</script>

<style scoped>
.bar {
  height: 20px;
}

.brand {
  min-width: fit-content;
  text-decoration: none;
  transition: all 0.3s ease;
}

.logo {
  width: 24px;
  height: 24px;
}

.name {
  font-size: 18px;
  font-weight: 600;
}

.action {
  min-width: fit-content;
}
</style>
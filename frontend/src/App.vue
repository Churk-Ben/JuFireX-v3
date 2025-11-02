<template>
	<n-config-provider :theme-overrides="themeOverrides" :theme="isDarkTheme ? darkTheme : null">
		<n-global-style />
		<n-message-provider>
			<!-- 加载屏幕 -->
			<LoadingScreen :is-loading="isLoading" />

			<!-- 主应用内容 -->
			<Transition name="app-fade" appear>
				<div v-if="!isLoading" class="layout">
					<!-- Header 内容 -->
					<n-flex>
						<n-card embedded class="m-2">
							<header class="container">
								<div class="row">
									<!-- 工作室 Logo 以及 名称 -->
									<a class="brand col-md-2" href="/">
										<img class="logo me-1" src="@/assets/studio/logo.svg" alt="JuFireX" />
										<span class="name me-1">JuFireX</span>
									</a>

									<!-- TODO: 重写NavMenu组件, 实现由登录用户权限生成动态导航菜单 -->
									<div class="menu col-md-6">
										<n-menu v-model:value="activeKey" mode="horizontal" :options="menuOptions"
											@update:value="handleMenuSelect" responsive />
									</div>


									<div class="action col-md-4 d-flex justify-content-end align-items-center gap-2">
										<!-- 开发调试用的登录状态切换开关 -->
										<n-switch v-model:value="userStore.isLoggedIn" @update:value="handleDebugLoginToggle" />

										<ToggleTag :icon="'fas fa-circle-half-stroke'"
											:text="isDarkTheme ? 'Light' : 'Dark'" @click="handleThemeChange" />

										<ToggleTag v-if="userStore.isLoggedIn" 
											:avatar-src="userStore.avatar || avatarImage" 
											:avatar-alt="userStore.nickname || 'User'"
											:text="userStore.nickname || 'User'" 
											:permission-level="userStore.permission" 
											@click="handleUserProfile" />

										<ToggleTag v-else :icon="'fas fa-user-circle'" :avatar-alt="'Login'"
											text="Login" :permission-level="0" @click="handleUserProfile" />
									</div>
								</div>
							</header>
						</n-card>
					</n-flex>


					<section class="content col-xl-8 col-md-10 col-12 mx-auto py-3">
						<RouterView />
					</section>

					<!-- Footer 内容 -->
					<n-flex>
						<n-card embedded class="m-2">
							<footer class="container">
								<div class="row">
									<div class="col-md-6">
										<span class="mb-0">&copy; 2025 JuFire Studio. All rights reserved.</span>
									</div>
									<div class="col-md-6 text-end">
										<a href="https://www.github.com/JuFireX" class="link me-3">
											<i class="fab fa-github me-2"></i>GitHub
										</a>
										<RouterLink to="/contact" class="link me-3">
											<i class="fas fa-envelope me-2"></i>Contact
										</RouterLink>
									</div>
								</div>
							</footer>
						</n-card>
					</n-flex>
				</div>
			</Transition>
		</n-message-provider>
	</n-config-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRouter, RouterView } from "vue-router";
import {
	useOsTheme,
	darkTheme,
	NConfigProvider,
	NGlobalStyle,
	NMessageProvider,
	GlobalThemeOverrides,
} from 'naive-ui'
import {
	NSwitch,
	NMenu,
	NCard,
	NFlex
} from 'naive-ui'
import type { MenuOption } from 'naive-ui'

import LoadingScreen from "@/components/LoadingScreen.vue";
import ToggleTag from "@/components/public/ToggleTag.vue";
import avatarImage from "@/assets/profile/avatar.jpg";
import { useUserStore } from "@/store";

// 加载状态管理
const router = useRouter()
const osTheme = useOsTheme()
const userStore = useUserStore()
const isLoading = ref(true);
const activeKey = ref<string>('/')
const isDarkTheme = ref(osTheme.value === 'dark')
const themeOverrides: GlobalThemeOverrides = {
	common: {
		borderRadius: '6px',
		borderRadiusSmall: '4px',
		primaryColor: '#0d6efd',
		primaryColorHover: '#0a58ca',
		primaryColorPressed: '#084298',
		primaryColorSuppl: 'rgb(42, 148, 125)',
	},
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
				// 仪表盘和主题等外观,展示设置
				label: '个性化',
				key: '/setting/preference'
			},
			{
				// 关乎账户信息,登录状态等
				label: '账户',
				key: '/setting/account'
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

// 等待应用初始化完成
onMounted(async () => {
	try {
		await nextTick();
		
		// 初始化用户状态
		await userStore.initUserState();
		
		await new Promise(resolve => setTimeout(resolve, 1500));

		// 确保所有异步操作完成后再隐藏加载屏幕
		isLoading.value = false;

		// 恢复body滚动
		document.body.classList.add('app-loaded');
	} catch (error) {
		console.error('应用初始化失败:', error);
		isLoading.value = false;
		document.body.classList.add('app-loaded');
	}
});

// 处理主菜单选择
function handleMenuSelect(key: string) {
	activeKey.value = key
	if (key.startsWith('/')) {
		router.push(key)
	}

	console.log(`导航到: ${key}`)
}

// 主题切换逻辑
function handleThemeChange() {
	isDarkTheme.value = !isDarkTheme.value
}

// 未登录时点击头像按钮跳转到登录页面, 登录后则跳转到用户个人主页
function handleUserProfile() {
	if (userStore.isLoggedIn) {
		router.push('/profile')
	} else {
		router.push('/login')
	}
}

// 开发调试用的登录状态切换处理函数
function handleDebugLoginToggle(value: boolean) {
	if (!value) {
		// 如果切换为未登录状态，清除用户信息
		userStore.clearUserState()
	} else {
		// 如果切换为登录状态，可以设置一些模拟数据用于开发调试
		// 注意：这只是为了开发调试，实际应用中应该通过API获取真实数据
		console.log('调试模式：切换到登录状态')
	}
}



</script>

<style scoped>
.layout {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

.content {
	display: flex;
	flex-direction: column;
	flex: 1 0 auto;
}

/* 主应用过渡动画 */
.app-fade-enter-active,
.app-fade-leave-active {
	transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.app-fade-enter-from {
	opacity: 0;
	transform: translateY(20px);
}

.app-fade-leave-to {
	opacity: 0;
	transform: translateY(-20px);
}

/* Header 与 Footer 样式 */
header {
	font-size: medium;
}

header .brand {
	min-width: fit-content;
	text-decoration: none;
	transition: all 0.3s ease;

	display: flex;
	align-items: center;
}

header .brand .logo {
	width: 24px;
	height: 24px;
}

header .brand .name {
	font-size: 1.4em;
	font-weight: 600;
	background: linear-gradient(45deg, #0d6efd, #42a5f5);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

header .action {
	min-width: fit-content;
}

header .menu {
	font-weight: 600;
}

footer {
	font-size: medium;
	font-weight: 300;
}

footer .link {
	color: inherit;
	text-decoration: none;
	transition: all 0.3s ease;
}

footer .link:hover {
	color: #0d6efd;
}
</style>

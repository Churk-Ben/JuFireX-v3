<template>
	<n-config-provider :theme-overrides="themeOverrides" :theme="isDarkTheme ? darkTheme : null">
		<n-global-style />
		<n-message-provider>
			<!-- 加载屏幕 -->
			<LoadingScreen :is-loading="isLoading" />

			<!-- 主应用内容 -->
			<Transition name="app-fade" appear>
				<div v-if="!isLoading" class="layout">
					<!-- NavBar -->
					<n-flex>
						<n-card embedded class="m-2">
							<div class="bar d-flex flex-row justify-content-between align-items-center">
								<div class="d-flex flex-row align-items-center">
									<a class="brand d-flex align-items-center mx-3" href="/">
										<img class="logo me-1" src="@/assets/studio/logo.svg" alt="JuFireX" />
										<span class="name me-1">JuFireX</span>
									</a>

									<!-- TODO: 封装NavMenu组件, 实现由登录用户权限生成动态导航菜单 -->
									<div class="menu">
										<n-menu v-model:value="activeKey" mode="horizontal" :options="menuOptions"
											@update:value="handleMenuSelect" responsive />
									</div>
								</div>

								<div class="action">
									<n-space>
										<!-- TODO: 美化这些按钮 -->
										<n-button ghost circle @click="handleThemeChange">
											<template #icon>
												<i class="fas fa-moon"></i>
											</template>
										</n-button>

										<!-- TODO: 封装UserBadge组件 -->
										<n-tag v-if="isUserLogin" ghost size="large" round>
											Aurore
											<template #avatar>
												<img class="avatar" src="@/assets/profile/avatar.jpg" alt="Aurore" />
											</template>
										</n-tag>

										<n-tag v-else ghost size="large" round>
											登录
											<template #avatar>
												<i class="avatar fas fa-user-circle" alt="登录"></i>
											</template>
										</n-tag>
										<!-- - -->
									</n-space>
								</div>
							</div>
						</n-card>
					</n-flex>


					<section class="content col-xl-10 col-lg-11 col-md-12 mx-auto py-3">
						<RouterView />
					</section>

					<!-- AppFooter 内容 -->
					<n-flex>
						<n-card embedded class="m-2">
							<div class="footer container">
								<div class="row">
									<div class="col-md-6">
										<span class="mb-0">&copy; 2025 JuFire Studio. All rights reserved.</span>
									</div>
									<div class="col-md-6 text-end">
										<a href="https://www.github.com/JuFireX" class="footer-link me-3">
											<i class="fab fa-github me-2"></i>GitHub
										</a>
										<RouterLink to="/contact" class="footer-link me-3">
											<i class="fas fa-envelope me-2"></i>Contact
										</RouterLink>
									</div>
								</div>
							</div>
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
	NButton,
	NSpace,
	NMenu,
	NCard,
	NFlex,
	NTag
} from 'naive-ui'
import type { MenuOption } from 'naive-ui'

import LoadingScreen from "@/components/LoadingScreen.vue";

// 加载状态管理
const router = useRouter()
const osTheme = useOsTheme()
const isLoading = ref(true);
const isUserLogin = ref(true);
const activeKey = ref<string>('/')
const isDarkTheme = ref(osTheme.value === 'dark')


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

// 等待应用初始化完成
onMounted(async () => {
	try {
		await nextTick();
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

/* NavBar 样式 */
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
	font-size: 1.5em;
	font-weight: 600;
	background: linear-gradient(45deg, #0d6efd, #42a5f5);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

/* 待封装组件 */

.action {
	min-width: fit-content;
}


.avatar {
	display: flex;
	align-self: center;
	height: 2em;
	border-radius: 50%;
}

/* AppFooter 样式 */
.footer {
	font-size: medium;
	font-weight: 300;
}

.footer-link {
	color: inherit;
	text-decoration: none;
	transition: all 0.3s ease;
}

.footer-link:hover {
	color: #0d6efd;
}
</style>

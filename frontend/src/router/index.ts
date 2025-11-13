import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { useUserStore } from "@/store/user";

const routes: RouteRecordRaw[] = [
  { 
    path: "/", 
    name: "home", 
    component: () => import("@/views/Home.vue"),
    meta: { title: "首页" }
  },
  { 
    path: "/contact", 
    name: "contact", 
    component: () => import("@/views/Contact.vue"),
    meta: { title: "联系我们" }
  },
  { 
    path: "/hello", 
    name: "hello", 
    component: () => import("@/views/Hello.vue"),
    meta: { title: "Hello" }
  },
  { 
    path: "/login", 
    name: "login", 
    component: () => import("@/views/Login.vue"),
    meta: { title: "登录", requiresGuest: true }
  },
  { 
    path: "/navigation", 
    name: "navigation", 
    component: () => import("@/views/Navigation.vue"),
    meta: { title: "导航" }
  },
  { 
    path: "/register", 
    name: "register", 
    component: () => import("@/views/Register.vue"),
    meta: { title: "注册", requiresGuest: true }
  },
  {
    path: "/logout",
    name: "logout",
    beforeEnter: () => {
      const userStore = useUserStore()
      userStore.userLogout()
      return { path: "/login" }
    },
    meta: { title: "退出登录" }
  },
  { 
    path: "/profile", 
    name: "profile", 
    component: () => import("@/views/Profile.vue"),
    meta: { title: "个人资料", requiresAuth: true }
  },
  { 
    path: "/project", 
    name: "project", 
    component: () => import("@/views/Project.vue"),
    meta: { title: "项目" }
  },
  // 设置相关路由
  {
    path: "/setting",
    name: "setting",
    redirect: "/setting/account",
    meta: { title: "设置", requiresAuth: true },
    children: [
      {
        path: "account",
        name: "setting-account",
        component: () => import("@/views/setting/Account.vue"),
        meta: { title: "账户设置", requiresAuth: true }
      },
      {
        path: "preference",
        name: "setting-preference",
        component: () => import("@/views/setting/Preference.vue"),
        meta: { title: "个性化设置", requiresAuth: true }
      },
      {
        path: "studio",
        name: "setting-studio",
        component: () => import("@/views/setting/Studio.vue"),
        meta: { title: "工作室设置", requiresAuth: true }
      }
    ]
  },
  // 管理员路由
  {
    path: "/admin",
    name: "admin",
    redirect: "/admin/user",
    meta: { title: "管理", requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: "user",
        name: "admin-user",
        component: () => import("@/views/admin/User.vue"),
        meta: { title: "用户管理", requiresAuth: true, requiresAdmin: true }
      },
      {
        path: "project",
        name: "admin-project",
        component: () => import("@/views/admin/Project.vue"),
        meta: { title: "项目管理", requiresAuth: true, requiresAdmin: true }
      },
      {
        path: "navigation",
        name: "admin-navigation",
        component: () => import("@/views/admin/Navigation.vue"),
        meta: { title: "导航管理", requiresAuth: true, requiresAdmin: true }
      }
    ]
  },
  // 404 页面
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/NotFound.vue"),
    meta: { title: "页面未找到" }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  
  console.log('🧭 路由导航', {
    from: from.path,
    to: to.path,
    meta: to.meta,
    isLoggedIn: userStore.isLoggedIn,
    timestamp: new Date().toISOString()
  });

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - JuFireX`;
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      console.log('🔒 需要登录，重定向到登录页', {
        targetPath: to.path,
        timestamp: new Date().toISOString()
      });
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
      return;
    }

    // 检查管理员权限
    if (to.meta.requiresAdmin && userStore.permission < 2) {
      console.log('🚫 权限不足，拒绝访问', {
        targetPath: to.path,
        userPermission: userStore.permission,
        timestamp: new Date().toISOString()
      });
      next('/');
      return;
    }
  }

  // 检查是否需要游客状态（未登录）
  if (to.meta.requiresGuest && userStore.isLoggedIn) {
    console.log('👤 已登录用户访问游客页面，重定向到首页', {
      targetPath: to.path,
      timestamp: new Date().toISOString()
    });
    next('/');
    return;
  }

  next();
});

// 路由后置守卫
router.afterEach((to, from) => {
  console.log('✅ 路由导航完成', {
    from: from.path,
    to: to.path,
    timestamp: new Date().toISOString()
  });
});

export default router;

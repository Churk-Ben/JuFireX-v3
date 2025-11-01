import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
	{ path: "/", name: "home", component: () => import("@/views/Home.vue") },
	{ path: "/contact", name: "contact", component: () => import("@/views/Contact.vue") },
	{ path: "/hello", name: "hello", component: () => import("@/views/Hello.vue") },
	{ path: "/login", name: "login", component: () => import("@/views/Login.vue") },
	{ path: "/navigation", name: "navigation", component: () => import("@/views/Navigation.vue") },
	{ path: "/register", name: "register", component: () => import("@/views/Register.vue") },
	{ path: "/profile", name: "profile", component: () => import("@/views/Profile.vue") },
	{ path: "/project", name: "project", component: () => import("@/views/Project.vue") },
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;

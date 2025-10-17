import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
	{ path: "/", name: "home", component: () => import("@/views/Home.vue") },
	{ path: "/contact", name: "contact", component: () => import("@/views/Contact.vue") },
	{ path: "/hello", name: "hello", component: () => import("@/views/Hello.vue") },

];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;

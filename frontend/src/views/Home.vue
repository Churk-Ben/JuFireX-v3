<template>
	<main>
		<h1>最小联通示例</h1>
		<p>后端连接状态：{{ status }}</p>
	</main>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import http from "@/utils/request";

const status = ref("检测中...");

onMounted(async () => {
	try {
		const res = await http.get("/health");
		status.value = String(res?.status || "ok");
	} catch (e) {
		status.value = "连接失败";
	}
});
</script>

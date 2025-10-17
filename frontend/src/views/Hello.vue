<template>
    <main>
        <h1>最小联通示例</h1>
        <p>后端连接状态：{{ status }}</p>
    </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getHelloStatus } from "@/api/hello";

const status = ref("检测中...");

onMounted(async () => {
    try {
        const res = await getHelloStatus();
        status.value = "连接成功" + res.message;
    } catch (e) {
        status.value = "连接失败";
    }
});
</script>
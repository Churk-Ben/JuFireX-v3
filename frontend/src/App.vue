<template>
	<div class="layout">
		<header class="header">
			<nav class="nav">
				<RouterLink to="/">Home</RouterLink>
			</nav>
		</header>
		<section class="content">
			<RouterView />
		</section>
	</div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped>
.layout {
	max-width: 960px;
	margin: 0 auto;
	padding: 0 16px;
}
.header {
	padding: 12px 0;
	border-bottom: 1px solid #eee;
}
.nav {
	display: flex;
	gap: 12px;
}
.content {
	padding: 16px 0;
}
</style>

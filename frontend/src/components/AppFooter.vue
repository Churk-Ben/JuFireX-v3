<template>
	<n-card :bordered="false">
		<div class="container">
			<div class="row">
				<div class="col-md-6">
					<span class="mb-0">&copy; 2025 JuFire Studio. All rights reserved.</span>
				</div>
				<div class="col-md-6 text-end">
					<n-button text tag="a" href="https://github.com" class="me-3" target="_blank">
						<i class="fab fa-github me-2"></i>GitHub
					</n-button>
					<n-button text tag="a" href="/contact" class="me-3">
						<i class="fas fa-envelope me-2"></i>Contact
					</n-button>
				</div>
			</div>
		</div>
	</n-card>
</template>

<script setup lang="ts">
import { NCard, NButton } from 'naive-ui';
</script>

<style scoped>
.n-card {
	font-size: medium;
	font-weight: 300;
}
</style>
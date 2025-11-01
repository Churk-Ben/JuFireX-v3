<template>
	<!-- 海报栏 -->
	<section class="hero-section">
		<div class="container">
			<div class="row align-items-center">
				<div class="col-lg-6">
					<h1 class="display-4 fw-bold mb-4">爝火工作室</h1>
					<p class="lead mb-4">我们是一个专注于前端开发的团队，致力于为客户提供高质量的服务。</p>

					<div class="d-flex gap-3">
						<a href="#projects" class="btn btn-primary btn-lg">查看项目</a>
						<a href="#contact" class="btn btn-outline-secondary btn-lg">联系我们</a>
					</div>
				</div>
				<div class="col-lg-6 text-center">
					<div class="p-5">
						<i class="fas fa-fire" style="font-size: 8rem; color: var(--github-accent)"></i>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- 项目展示 -->
	<section class="project-section py-5">
		<div class="container">
			<div class="row mb-5">
				<div class="col-12 text-center">
					<h2 class="h1 mb-3">精选项目</h2>
					<p class="lead text-muted">展示我们最新和最受欢迎的项目</p>
				</div>
			</div>

			<div class="row">
				<div class="col-12 text-center">
					<div class="py-5">
						<i class="fas fa-folder-open" style="font-size: 4rem; color: var(--github-text-secondary)"></i>
						<h3 class="mt-3 text-muted">暂无项目</h3>
						<p class="text-muted">工作室项目正在筹备中, 敬请期待！</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- 统计信息 -->
	<section class="py-5" style="background-color: var(--github-secondary)">
		<div class="container">
			<div class="row text-center">
				<div class="col-md-3 col-6 mb-4">
					<div class="p-3">
						<i class="fas fa-code" style="font-size: 2.5rem; color: var(--github-accent)"></i>
						<h3 class="mt-2 mb-0">0</h3>
						<p class="text-muted mb-0">项目数量</p>
					</div>
				</div>
				<div class="col-md-3 col-6 mb-4">
					<div class="p-3">
						<i class="fas fa-users" style="font-size: 2.5rem; color: var(--github-success)"></i>
						<h3 class="mt-2 mb-0">5+</h3>
						<p class="text-muted mb-0">团队成员</p>
					</div>
				</div>
				<div class="col-md-3 col-6 mb-4">
					<div class="p-3">
						<i class="fas fa-star" style="font-size: 2.5rem; color: #ffd700"></i>
						<h3 class="mt-2 mb-0">100+</h3>
						<p class="text-muted mb-0">GitHub 星标</p>
					</div>
				</div>
				<div class="col-md-3 col-6 mb-4">
					<div class="p-3">
						<i class="fas fa-download" style="font-size: 2.5rem; color: var(--github-danger)"></i>
						<h3 class="mt-2 mb-0">1000+</h3>
						<p class="text-muted mb-0">下载次数</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- 联系信息 -->
	<section class="py-5">
		<div class="container">
			<div class="row justify-content-center">
				<div class="col-lg-8 text-center">
					<h2 class="mb-4">联系我们</h2>
					<p class="lead mb-4">有任何问题或合作意向, 欢迎随时联系我们</p>

					<div class="row g-4">
						<div class="col-md-6">
							<div class="card">
								<div class="card-body">
									<i class="fas fa-envelope" style="font-size: 2rem; color: var(--github-accent)"></i>
									<h5 class="mt-3">邮箱联系</h5>
									<p class="text-muted">
										contact@jufire.studio
									</p>
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="card">
								<div class="card-body">
									<i class="fab fa-github" style="font-size: 2rem; color: var(--github-accent)"></i>
									<h5 class="mt-3">GitHub</h5>
									<p class="text-muted">
										github.com/jufirex
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">

</script>


<style>
.hero-section {
	display: flex;
	align-items: center;
	height: 50vh;
	background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
	background-size: cover;
}

.project-section {
	min-height: 100vh;
}
</style>
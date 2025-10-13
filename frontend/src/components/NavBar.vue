<template>
  <nav>
    <div class="container">
      <a class="navbar-brand" href="#">
        <i class="fas fa-fire me-1"></i>JuFire Studio
      </a>

      <div class="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" style="margin: 0 5px">
            <a class="nav-link" href="#">首页</a>
          </li>

          <li class="nav-item" style="margin: 0 5px">
            <a class="nav-link" href="#">导航</a>
          </li>

          <li class="nav-item" style="margin: 0 5px">
            <a class="nav-link" href="#">项目</a>
          </li>

          <li class="nav-item dropdown" style="margin: 0 5px">
            <a class="nav-link dropdown-toggle">设置</a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li>
                <a class="dropdown-item" href="#">工作室</a>
              </li>
              <li>
                <a class="dropdown-item" href="#">仪表盘</a>
              </li>
              <li>
                <a class="dropdown-item" href="#">所有设置</a>
              </li>
              <li>
                <hr class="dropdown-divider" />
              </li>
              <li>
                <a class="dropdown-item text-danger" href="#">退出登录</a>
              </li>
            </ul>
          </li>

          <li class="nav-item dropdown" style="margin: 0 5px">
            <a class="nav-link dropdown-toggle">管理</a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li>
                <a class="dropdown-item" href="#">项目管理</a>
              </li>
              <li>
                <a class="dropdown-item" href="#">导航管理</a>
              </li>
              <li>
                <a class="dropdown-item" href="#">用户管理</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

</template>

<script setup lang="ts">
import { } from 'naive-ui'
</script>
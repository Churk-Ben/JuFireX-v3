<template>
    <n-card embedded title="登录" class="col-3 mx-auto my-auto">
        <!-- 登录表单 -->
        <n-form ref="formRef" :model="modelRef" :rules="rules">
            <n-form-item path="username" label="用户名">
                <n-input v-model:value="modelRef.username" placeholder="请输入用户名" @keydown.enter.prevent />
            </n-form-item>
            <n-form-item path="password" label="密码">
                <n-input v-model:value="modelRef.password" type="password" placeholder="请输入密码" @keydown.enter.prevent />
            </n-form-item>
        </n-form>

        <!-- 底部链接 -->
        <template #footer>
            <p class="mb-0">
                还没有账号？
                <router-link to="/register" class="text-decoration-none">立即注册</router-link>
            </p>
        </template>

        <template #action>
            <n-button type="primary" block size="large" @click="handleLogin">
                <i class="fas fa-sign-in-alt me-2"></i>
                登录
            </n-button>
        </template>

    </n-card>
</template>

<script setup lang="ts">
import type { FormInst, FormItemInst, FormItemRule, FormRules } from 'naive-ui'
import { NButton, NCard, NForm, NFormItem, NInput } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { ref } from 'vue'

interface ModelType {
    username: string | null
    password: string | null
}

const formRef = ref<FormInst | null>(null)
const message = useMessage()

const modelRef = ref<ModelType>({
    username: null,
    password: null
})

const rules: FormRules = {
    username: [
        {
            required: true,
            message: '至少输个用户名啊喂!'
        }
    ],
    password: [
        {
            required: true,
            message: '还需要密码'
        }
    ]
}

function handleLogin() {
    // 验证密码格式
    handleValidateButtonClick(new MouseEvent('click'))
    // 处理登录逻辑
    console.log("登录按钮被点击" + JSON.stringify(modelRef.value, null, 2));
}

function handleValidateButtonClick(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate((errors) => {
        if (!errors) {
            message.success('验证成功')
        }
        else {
            console.log(errors)
            message.error('验证失败')
        }
    })
}
</script>
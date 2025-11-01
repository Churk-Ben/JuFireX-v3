<template>
    <n-card embedded title="登录" class="col-4 mx-auto my-auto">
        <!-- 登录表单 -->
        <n-form ref="formRef" :model="modelRef" :rules="rules">
            <n-form-item path="username" label="用户名">
                <n-input v-model:value="modelRef.username" @keydown.enter.prevent />
            </n-form-item>
            <n-form-item path="password" label="密码">
                <n-input v-model:value="modelRef.password" type="password" @input="handlePasswordInput"
                    @keydown.enter.prevent />
            </n-form-item>

            <n-row :gutter="[0, 24]">
                <n-col :span="24">
                    <div style="display: flex; justify-content: flex-end">
                        <n-button :disabled="modelRef.username === null" round type="primary"
                            @click="handleValidateButtonClick">
                            验证
                        </n-button>
                    </div>
                </n-col>
            </n-row>
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
                登录
            </n-button>
        </template>

    </n-card>


    <pre>{{ JSON.stringify(modelRef, null, 2) }}</pre>
</template>

<script setup lang="ts">
import { NButton, NSpace, NCard, NAvatar, NTag, NDropdown, NFlex } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { ref } from 'vue'

function handleLogin() {
    // 处理登录逻辑
    console.log("登录按钮被点击");
}

import { NForm, NFormItem, NInput, NRow, NCol } from 'naive-ui'
import type { FormInst, FormItemInst, FormItemRule, FormRules } from 'naive-ui'


interface ModelType {
    username: string | null
    password: string | null
}

const formRef = ref<FormInst | null>(null)
const rPasswordFormItemRef = ref<FormItemInst | null>(null)
const message = useMessage()
const modelRef = ref<ModelType>({
    username: null,
    password: null
})

function validatePasswordStartWith(rule: FormItemRule, value: string): boolean {
    return (
        !!modelRef.value.password
        && modelRef.value.password.startsWith(value)
        && modelRef.value.password.length >= value.length
    )
}

function validatePasswordSame(rule: FormItemRule, value: string): boolean {
    return value === modelRef.value.password
}

const rules: FormRules = {
    age: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error('需要年龄')
                }
                else if (!/^\d*$/.test(value)) {
                    return new Error('年龄应该为整数')
                }
                else if (Number(value) < 18) {
                    return new Error('年龄应该超过十八岁')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    password: [
        {
            required: true,
            message: '请输入密码'
        }
    ],
    reenteredPassword: [
        {
            required: true,
            message: '请再次输入密码',
            trigger: ['input', 'blur']
        },
        {
            validator: validatePasswordStartWith,
            message: '两次密码输入不一致',
            trigger: 'input'
        },
        {
            validator: validatePasswordSame,
            message: '两次密码输入不一致',
            trigger: ['blur', 'password-input']
        }
    ]
}

function handlePasswordInput() {
    rPasswordFormItemRef.value?.validate('password-input')
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
<template>
    <n-space vertical>
        <n-steps :current="current || undefined" :status="currentStatus">
            <n-step title="邮箱" description="在创建你的帐号前, 我们需要收集你的邮箱作为账号的唯一标识." />
            <n-step title="用户名和密码" description="取一个好听的名字, 并设置一个安全好记的密码. 放心, 我们会加密存储你的密码." />
            <n-step title="头像" description="需要上传图片作为你的头像吗? 我们也有一些预设. 你也可以稍后在个人设置中修改." />
            <n-step title="完成" description="注册成功! 点击按钮前往登录页面. 再登录一次是为了确保你记住了密码~" />
        </n-steps>
    </n-space>

    <n-space class="mx-auto my-auto">
        <p>当前步骤: {{ current !== null ? current + 1 : '无' }}</p>
        <p>当前状态: {{ currentStatus }}</p>
        <n-button-group>
            <n-button @click="prev">
                <template #icon>
                    <i class="fas fa-angle-left"></i>
                </template>
            </n-button>
            <n-button @click="next">
                <template #icon>
                    <i class="fas fa-angle-right"></i>
                </template>
            </n-button>
        </n-button-group>
        <n-radio-group v-model:value="currentStatus" size="medium" name="basic">
            <n-radio-button value="error">
                Error
            </n-radio-button>
            <n-radio-button value="process">
                Process
            </n-radio-button>
            <n-radio-button value="wait">
                Wait
            </n-radio-button>
            <n-radio-button value="finish">
                Finish
            </n-radio-button>
        </n-radio-group>
    </n-space>
</template>

<script setup lang="ts">
import { NSteps, NStep, NSpace, NButtonGroup, NButton, NRadioButton, NRadioGroup } from 'naive-ui'
import type { StepsProps } from 'naive-ui'
import { ref } from 'vue'

const currentRef = ref<number | null>(1)
const currentStatus = ref<StepsProps['status']>('process')
const current = currentRef

function next() {
    if (currentRef.value === null)
        currentRef.value = 1
    else if (currentRef.value >= 4)
        currentRef.value = null
    else currentRef.value++
}

function prev() {
    if (currentRef.value === 0)
        currentRef.value = null
    else if (currentRef.value === null)
        currentRef.value = 4
    else currentRef.value--
}
</script>
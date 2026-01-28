<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div class="w-full max-w-md">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
        <div class="text-center mb-6">
          <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">创建新账户</p>
        </div>

        <!-- 错误提示 -->
        <div v-if="authStore.error" class="mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
          {{ authStore.error }}
        </div>

        <!-- 自定义错误提示 -->
        <div v-if="passwordMismatch" class="mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
          两次输入的密码不一致
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="form-group">
            <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">用户名</label>
            <input
              type="text"
              id="name"
              v-model="form.username"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="请输入用户名"
              required
            >
          </div>

          <div class="form-group">
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">邮箱</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="请输入邮箱地址"
              required
            >
          </div>

          <div class="form-group">
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">密码</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="请输入密码"
              required
              minlength="6"
            >
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="form.confirmPassword"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="请再次输入密码"
              required
              minlength="6"
            >
          </div>

          <div class="flex items-center">
            <input
              type="checkbox"
              id="terms"
              v-model="form.terms"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded dark:bg-gray-700 dark:border-gray-600"
              required
            >
            <label for="terms" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
              我同意 <a href="#" class="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300">服务条款</a> 和 <a href="#" class="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300">隐私政策</a>
            </label>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ authStore.loading ? '注册中...' : '注册' }}
            </button>
          </div>

          <div class="text-center mt-4">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              已有账户? <router-link to="/auth/login" class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300">登录</router-link>
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth.store';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: false
});

const passwordMismatch = computed(() => {
  return form.value.password && form.value.confirmPassword && form.value.password !== form.value.confirmPassword;
});

const handleRegister = async () => {
  // 重置错误
  authStore.clearError();

  // 验证密码是否匹配
  if (passwordMismatch.value) {
    return;
  }

  try {
    await authStore.register(form.value.username, form.value.email, form.value.password);
    // 注册成功后重定向到仪表盘
    router.push('/');
  } catch (error) {
    // 错误已经在 store 中处理
    console.error('注册失败:', error);
  }
};
</script>

<style scoped>
/* 组件特定样式 */
</style>

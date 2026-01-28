<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div class="w-full max-w-md">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
        <div class="text-center mb-6">
          <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">登录到 TrendMatrix</p>
        </div>

        <!-- 错误提示 -->
        <div v-if="authStore.error" class="mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
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
            >
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                type="checkbox"
                id="remember"
                v-model="form.remember"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded dark:bg-gray-700 dark:border-gray-600"
              >
              <label for="remember" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">记住我</label>
            </div>
            <div class="text-sm">
              <a href="#" class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300">忘记密码?</a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ authStore.loading ? '登录中...' : '登录' }}
            </button>
          </div>

          <div class="text-center mt-4">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              还没有账户? <router-link to="/auth/register" class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300">注册</router-link>
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth.store';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  email: '',
  password: '',
  remember: false
});

const handleLogin = async () => {
  try {
    await authStore.login(form.value.email, form.value.password);
    // 登录成功后重定向到仪表盘
    router.push('/');
  } catch (error) {
    // 错误已经在 store 中处理
    console.error('登录失败:', error);
  }
};
</script>

<style scoped>
/* 组件特定样式 */
</style>

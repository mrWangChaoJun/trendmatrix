<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">管理您的订阅和使用情况</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
      {{ error }}
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 无订阅状态 -->
    <div v-else-if="!activeSubscription" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 text-center">
      <div class="mb-6">
        <svg class="h-16 w-16 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">您还没有订阅</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">选择一个订阅计划来开始使用我们的服务</p>
      <router-link
        to="/subscription/plans"
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        浏览订阅计划
      </router-link>
    </div>

    <!-- 订阅详情 -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <!-- 订阅头部 -->
      <div class="bg-blue-50 dark:bg-blue-900/30 p-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ activeSubscription?.plan.name }}</h2>
            <p class="mt-1 text-gray-600 dark:text-gray-400">{{ activeSubscription?.plan.description }}</p>
          </div>
          <div class="mt-4 md:mt-0 flex items-center">
            <span class="px-3 py-1 text-sm font-medium rounded-full" :class="statusClass">
              {{ activeSubscription?.status === 'active' ? '活跃' : '已取消' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 订阅详情内容 -->
      <div class="p-6">
        <!-- 订阅信息 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">订阅信息</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">订阅开始日期</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(activeSubscription?.start_date) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">订阅结束日期</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(activeSubscription?.end_date) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">计费周期</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ activeSubscription?.plan.billing_cycle }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">自动续费</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ activeSubscription?.auto_renew ? '开启' : '关闭' }}</span>
              </div>
            </div>
          </div>

          <!-- 价格信息 -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">价格信息</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">计划价格</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ activeSubscription?.plan.price }} {{ activeSubscription?.plan.currency }}/{{ activeSubscription?.plan.billing_cycle }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">支付状态</span>
                <span class="font-medium text-green-600 dark:text-green-400">已支付</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 使用情况 -->
        <div class="mb-8">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">使用情况</h3>
          <div class="space-y-6">
            <!-- API 调用限制 -->
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600 dark:text-gray-400">API 调用</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ currentUsage.api_calls }} / {{ activeSubscription?.plan.api_rate_limit }} 次/分钟
                </span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div
                  class="bg-blue-600 h-2.5 rounded-full"
                  :style="{ width: `${Math.min((currentUsage.api_calls / (activeSubscription?.plan.api_rate_limit || 1)) * 100, 100)}%` }"
                ></div>
              </div>
            </div>

            <!-- 信号生成限制 -->
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600 dark:text-gray-400">信号生成</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ currentUsage.signals_generated }} / {{ activeSubscription?.plan.signal_limit }} 个/月
                </span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div
                  class="bg-green-600 h-2.5 rounded-full"
                  :style="{ width: `${Math.min((currentUsage.signals_generated / (activeSubscription?.plan.signal_limit || 1)) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex flex-wrap gap-4">
          <button
            @click="toggleAutoRenew"
            :disabled="isLoading"
            class="px-6 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ activeSubscription?.auto_renew ? '关闭自动续费' : '开启自动续费' }}
          </button>
          <router-link
            to="/subscription/plans"
            :disabled="isLoading"
            class="px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            升级计划
          </router-link>
          <button
            @click="confirmCancel"
            :disabled="isLoading || activeSubscription?.status !== 'active'"
            class="px-6 py-2 border border-red-300 dark:border-red-600 rounded-md shadow-sm text-sm font-medium text-red-700 dark:text-red-300 bg-white dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            取消订阅
          </button>
        </div>
      </div>
    </div>

    <!-- 取消订阅确认弹窗 -->
    <div v-if="showCancelConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
        <div class="text-center mb-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">确认取消订阅</h3>
          <p class="mt-2 text-gray-600 dark:text-gray-400">
            您确定要取消 {{ activeSubscription?.plan.name }} 计划的订阅吗？
          </p>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            取消后，您的订阅将在当前计费周期结束后失效。
          </p>
        </div>

        <div class="flex space-x-4">
          <button
            @click="showCancelConfirm = false"
            class="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button
            @click="cancelSubscription"
            :disabled="isLoading"
            class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ isLoading ? '处理中...' : '确认取消' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import localDbService from '../../services/db/local-db.service';

// 状态数据
const isLoading = ref(false);
const error = ref('');
const activeSubscription = ref<any>(null);
const showCancelConfirm = ref(false);
const currentUsage = ref({
  api_calls: 0,
  signals_generated: 0
});

// 状态样式
const statusClass = computed(() => {
  if (activeSubscription.value?.status === 'active') {
    return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
  } else {
    return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
});

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};

// 加载订阅数据
async function loadSubscriptionData() {
  isLoading.value = true;
  error.value = '';

  try {
    // 从本地数据库获取订阅数据
    const subscriptions = await localDbService.getUserSubscriptions();

    if (subscriptions.length > 0) {
      activeSubscription.value = subscriptions[0];

      // 模拟使用数据
      currentUsage.value = activeSubscription.value.current_usage || {
        api_calls: Math.floor(Math.random() * (activeSubscription.value.plan.api_rate_limit || 100)),
        signals_generated: Math.floor(Math.random() * (activeSubscription.value.plan.signal_limit || 50))
      };
    }
  } catch (err) {
    error.value = '获取订阅数据失败';
    console.error('Error loading subscription data:', err);
  } finally {
    isLoading.value = false;
  }
}

// 切换自动续费
const toggleAutoRenew = async () => {
  if (!activeSubscription.value) return;

  try {
    // 模拟更新自动续费设置
    activeSubscription.value.auto_renew = !activeSubscription.value.auto_renew;
  } catch (error) {
    console.error('更新自动续费设置失败:', error);
  }
};

// 确认取消订阅
const confirmCancel = () => {
  showCancelConfirm.value = true;
};

// 取消订阅
const cancelSubscription = async () => {
  if (!activeSubscription.value) return;

  try {
    // 模拟取消订阅
    activeSubscription.value.status = 'canceled';
    showCancelConfirm.value = false;
  } catch (error) {
    console.error('取消订阅失败:', error);
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadSubscriptionData();
});
</script>

<style scoped>
/* 组件特定样式 */
</style>

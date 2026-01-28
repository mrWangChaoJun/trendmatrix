<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">查看您的支付记录</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
      {{ error }}
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 筛选器 -->
    <div class="mb-6 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">开始日期</label>
          <input
            type="date"
            v-model="filter.start_date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">结束日期</label>
          <input
            type="date"
            v-model="filter.end_date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">支付状态</label>
          <select
            v-model="filter.status"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          >
            <option value="">全部状态</option>
            <option value="completed">已完成</option>
            <option value="pending">处理中</option>
            <option value="failed">失败</option>
            <option value="refunded">已退款</option>
          </select>
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button
          @click="applyFilter"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          应用筛选
        </button>
        <button
          @click="resetFilter"
          class="ml-3 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          重置
        </button>
      </div>
    </div>

    <!-- 支付历史列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                支付 ID
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                日期
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                金额
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                状态
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                支付方式
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                描述
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="payment in paymentHistory" :key="payment.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ payment.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                {{ formatDate(payment.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ payment.amount }} {{ payment.currency }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(payment.status)"
                >
                  {{ getStatusText(payment.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                {{ payment.payment_method.type === 'credit_card' ? `${payment.payment_method.brand} 卡` :
                   payment.payment_method.type === 'paypal' ? 'PayPal' :
                   payment.payment_method.type === 'crypto' ? '加密货币' : '银行转账' }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-600 dark:text-gray-400">
                {{ payment.subscription_id ? '订阅支付' : '其他支付' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click="viewPaymentDetails(payment.id)"
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 focus:outline-none"
                >
                  查看详情
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 空状态 -->
      <div v-if="paymentHistory.length === 0" class="px-6 py-12 text-center">
        <svg class="h-16 w-16 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path>
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-white">暂无支付记录</h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400">您还没有任何支付记录</p>
      </div>

      <!-- 分页 -->
      <div v-if="paymentHistory.length > 0" class="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <a href="#" class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            上一页
          </a>
          <a href="#" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            下一页
          </a>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              显示第 <span class="font-medium">1</span> 到 <span class="font-medium">{{ paymentHistory.length }}</span> 条，共 <span class="font-medium">{{ paymentHistory.length }}</span> 条记录
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600">
                <span class="sr-only">上一页</span>
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
              </a>
              <a href="#" aria-current="page" class="z-10 bg-blue-50 dark:bg-blue-900/30 border-blue-500 text-blue-600 dark:text-blue-400 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                1
              </a>
              <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600">
                <span class="sr-only">下一页</span>
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
              </a>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 支付详情弹窗 -->
    <div v-if="showPaymentDetails" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">支付详情</h3>
          <button
            @click="showPaymentDetails = false"
            class="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div v-if="selectedPayment" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">支付信息</h4>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">支付 ID</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">交易 ID</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.transaction_id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">金额</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.amount }} {{ selectedPayment.currency }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">状态</span>
                  <span
                    class="text-sm font-medium px-2 py-1 rounded-full"
                    :class="getStatusClass(selectedPayment.status)"
                  >
                    {{ getStatusText(selectedPayment.status) }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">创建时间</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ formatDateTime(selectedPayment.created_at) }}</span>
                </div>
                <div v-if="selectedPayment.updated_at" class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">更新时间</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ formatDateTime(selectedPayment.updated_at) }}</span>
                </div>
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">支付方式</h4>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">类型</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ selectedPayment.payment_method.type === 'credit_card' ? '信用卡/借记卡' :
                       selectedPayment.payment_method.type === 'paypal' ? 'PayPal' :
                       selectedPayment.payment_method.type === 'crypto' ? '加密货币' : '银行转账' }}
                  </span>
                </div>
                <div v-if="selectedPayment.payment_method.type === 'credit_card'" class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">品牌</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.payment_method.brand }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">账号</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ selectedPayment.payment_method.type === 'credit_card' ? `**** ${selectedPayment.payment_method.last_four}` :
                       selectedPayment.payment_method.last_four }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">其他信息</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">描述</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.subscription_id ? '订阅支付' : '其他支付' }}</span>
              </div>
              <div v-if="selectedPayment.subscription_id" class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">订阅 ID</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedPayment.subscription_id }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 flex justify-end">
          <button
            @click="showPaymentDetails = false"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import localDbService from '../../services/db/local-db.service';

// 状态数据
const isLoading = ref(false);
const error = ref('');
const paymentHistory = ref<any[]>([]);
const showPaymentDetails = ref(false);
const selectedPayment = ref<any>(null);

const filter = ref({
  start_date: '',
  end_date: '',
  status: '',
  limit: 20,
  offset: 0
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

// 格式化日期时间
const formatDateTime = (dateString?: string) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

// 获取状态样式
const getStatusClass = (status?: string) => {
  switch (status) {
    case 'completed':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
    case 'failed':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
    case 'refunded':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
};

// 获取状态文本
const getStatusText = (status?: string) => {
  switch (status) {
    case 'completed':
      return '已完成';
    case 'pending':
      return '处理中';
    case 'failed':
      return '失败';
    case 'refunded':
      return '已退款';
    default:
      return '未知';
  }
};

// 生成测试支付数据
function generateTestPaymentData() {
  const statuses = ['completed', 'pending', 'failed', 'refunded'];
  const paymentMethods = [
    {
      type: 'credit_card',
      brand: 'Visa',
      last_four: '4242'
    },
    {
      type: 'credit_card',
      brand: 'Mastercard',
      last_four: '5555'
    },
    {
      type: 'paypal',
      last_four: 'paypal123'
    },
    {
      type: 'crypto',
      last_four: 'BTC1234'
    },
    {
      type: 'bank_transfer',
      last_four: 'BANK5678'
    }
  ];

  const payments = [];
  const today = new Date();

  for (let i = 1; i <= 15; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i * 2);

    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const paymentMethod = paymentMethods[Math.floor(Math.random() * paymentMethods.length)];
    const isSubscription = Math.random() > 0.3;

    payments.push({
      id: `payment_${i}`,
      transaction_id: `tx_${i}_${Math.floor(Math.random() * 1000000)}`,
      amount: (Math.random() * 1000 + 10).toFixed(2),
      currency: 'USD',
      status: status,
      payment_method: paymentMethod,
      subscription_id: isSubscription ? `sub_${Math.floor(Math.random() * 1000)}` : null,
      created_at: date.toISOString(),
      updated_at: status !== 'completed' ? new Date(date.getTime() + 3600000).toISOString() : date.toISOString()
    });
  }

  return payments;
}

// 加载支付历史
async function loadPaymentHistory(filters?: any) {
  isLoading.value = true;
  error.value = '';

  try {
    // 生成测试支付数据
    let payments = generateTestPaymentData();

    // 应用筛选
    if (filters) {
      if (filters.status) {
        payments = payments.filter(payment => payment.status === filters.status);
      }

      if (filters.start_date) {
        const startDate = new Date(filters.start_date);
        payments = payments.filter(payment => new Date(payment.created_at) >= startDate);
      }

      if (filters.end_date) {
        const endDate = new Date(filters.end_date);
        endDate.setHours(23, 59, 59, 999);
        payments = payments.filter(payment => new Date(payment.created_at) <= endDate);
      }

      if (filters.limit) {
        payments = payments.slice(filters.offset, filters.offset + filters.limit);
      }
    }

    paymentHistory.value = payments;
  } catch (err) {
    error.value = '获取支付历史失败';
    console.error('Error loading payment history:', err);
  } finally {
    isLoading.value = false;
  }
}

// 加载支付详情
async function loadPaymentDetails(paymentId: string) {
  try {
    // 查找支付记录
    const payment = paymentHistory.value.find(p => p.id === paymentId);
    if (payment) {
      selectedPayment.value = payment;
      showPaymentDetails.value = true;
    }
  } catch (err) {
    console.error('获取支付详情失败:', err);
  }
}

// 应用筛选
const applyFilter = async () => {
  await loadPaymentHistory(filter.value);
};

// 重置筛选
const resetFilter = async () => {
  filter.value = {
    start_date: '',
    end_date: '',
    status: '',
    limit: 20,
    offset: 0
  };
  await loadPaymentHistory();
};

// 查看支付详情
const viewPaymentDetails = async (paymentId: string) => {
  await loadPaymentDetails(paymentId);
};

// 组件挂载时加载数据
onMounted(() => {
  loadPaymentHistory();
});
</script>

<style scoped>
/* 组件特定样式 */
</style>

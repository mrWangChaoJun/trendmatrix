<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">管理您的支付方式</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="paymentStore.error" class="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
      {{ paymentStore.error }}
    </div>

    <!-- 成功提示 -->
    <div v-if="successMessage" class="mb-6 p-4 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-md">
      {{ successMessage }}
    </div>

    <!-- 加载状态 -->
    <div v-if="paymentStore.loading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 支付方式列表 -->
    <div v-else class="mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white">已添加的支付方式</h2>
        <button 
          @click="showAddForm = true"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          添加支付方式
        </button>
      </div>

      <!-- 无支付方式 -->
      <div v-if="!paymentStore.hasPaymentMethods" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 text-center">
        <div class="mb-6">
          <svg class="h-16 w-16 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"></path>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">您还没有添加支付方式</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">添加支付方式以便于订阅和支付</p>
        <button 
          @click="showAddForm = true"
          class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          添加支付方式
        </button>
      </div>

      <!-- 支付方式卡片 -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="method in paymentStore.userPaymentMethods" 
          :key="method.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden border border-gray-200 dark:border-gray-700"
        >
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <div class="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mr-4">
                  <svg v-if="method.type === 'credit_card'" class="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                  </svg>
                  <svg v-else-if="method.type === 'paypal'" class="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                  </svg>
                  <svg v-else-if="method.type === 'crypto'" class="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <svg v-else class="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-medium text-gray-900 dark:text-white">
                    {{ method.type === 'credit_card' ? `${method.brand} 卡` : 
                       method.type === 'paypal' ? 'PayPal' : 
                       method.type === 'crypto' ? '加密货币' : '银行转账' }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ method.type === 'credit_card' ? `**** ${method.last_four}` : 
                       method.type === 'paypal' ? method.last_four : 
                       method.type === 'crypto' ? method.last_four : '银行账户' }}
                  </p>
                </div>
              </div>
              <div v-if="method.is_default" class="px-3 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                默认
              </div>
            </div>

            <div class="mt-4 space-y-2">
              <div v-if="method.type === 'credit_card' && method.expiry_date" class="text-sm text-gray-600 dark:text-gray-400">
                到期日期: {{ method.expiry_date }}
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">
                添加时间: {{ formatDate(method.created_at) }}
              </div>
              <div class="text-sm" :class="method.status === 'active' ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'">
                状态: {{ method.status === 'active' ? '活跃' : '已禁用' }}
              </div>
            </div>

            <div class="mt-6 flex space-x-3">
              <button 
                v-if="!method.is_default"
                @click="setDefaultMethod(method.id)"
                :disabled="paymentStore.loading"
                class="flex-1 py-1.5 px-3 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-xs font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                设置为默认
              </button>
              <button 
                @click="confirmDelete(method.id)"
                :disabled="paymentStore.loading"
                class="py-1.5 px-3 border border-red-300 dark:border-red-600 rounded-md shadow-sm text-xs font-medium text-red-700 dark:text-red-300 bg-white dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 添加支付方式弹窗 -->
  <div v-if="showAddForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">添加支付方式</h3>
        <button 
          @click="showAddForm = false"
          class="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <form @submit.prevent="addPaymentMethod">
        <!-- 支付方式类型 -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">支付方式类型</label>
          <select 
            v-model="newPaymentMethod.type"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            required
          >
            <option value="">选择类型</option>
            <option value="credit_card">信用卡/借记卡</option>
            <option value="paypal">PayPal</option>
            <option value="crypto">加密货币</option>
            <option value="bank_transfer">银行转账</option>
          </select>
        </div>

        <!-- 信用卡信息 -->
        <div v-if="newPaymentMethod.type === 'credit_card'" class="space-y-4">
          <div>
            <label for="card-number" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">卡号</label>
            <input 
              type="text"
              id="card-number"
              v-model="newPaymentMethod.details.number"
              placeholder="请输入卡号"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
          </div>
          <div>
            <label for="card-expiry" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">到期日期</label>
            <div class="grid grid-cols-2 gap-4">
              <input 
                type="number"
                id="expiry-month"
                v-model="newPaymentMethod.details.expiry_month"
                placeholder="月"
                min="1"
                max="12"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                required
              >
              <input 
                type="number"
                id="expiry-year"
                v-model="newPaymentMethod.details.expiry_year"
                placeholder="年"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                required
              >
            </div>
          </div>
          <div>
            <label for="card-cvc" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">CVC</label>
            <input 
              type="text"
              id="card-cvc"
              v-model="newPaymentMethod.details.cvc"
              placeholder="请输入CVC"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
          </div>
        </div>

        <!-- PayPal 信息 -->
        <div v-else-if="newPaymentMethod.type === 'paypal'" class="mb-4">
          <label for="paypal-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">PayPal 邮箱</label>
          <input 
            type="email"
            id="paypal-email"
            v-model="newPaymentMethod.details.email"
            placeholder="请输入PayPal邮箱"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            required
          >
        </div>

        <!-- 加密货币信息 -->
        <div v-else-if="newPaymentMethod.type === 'crypto'" class="mb-4">
          <label for="crypto-address" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">钱包地址</label>
          <input 
            type="text"
            id="crypto-address"
            v-model="newPaymentMethod.details.wallet_address"
            placeholder="请输入钱包地址"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            required
          >
        </div>

        <!-- 银行转账信息 -->
        <div v-else-if="newPaymentMethod.type === 'bank_transfer'" class="space-y-4">
          <div>
            <label for="account-holder" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">账户持有人姓名</label>
            <input 
              type="text"
              id="account-holder"
              v-model="newPaymentMethod.details.bank_account.account_holder_name"
              placeholder="请输入账户持有人姓名"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
          </div>
          <div>
            <label for="account-number" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">账号</label>
            <input 
              type="text"
              id="account-number"
              v-model="newPaymentMethod.details.bank_account.account_number"
              placeholder="请输入账号"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
          </div>
          <div>
            <label for="routing-number" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"> routing number</label>
            <input 
              type="text"
              id="routing-number"
              v-model="newPaymentMethod.details.bank_account.routing_number"
              placeholder="请输入routing number"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
          </div>
        </div>

        <!-- 设置为默认 -->
        <div class="flex items-center mb-6">
          <input 
            type="checkbox" 
            id="set-as-default"
            v-model="newPaymentMethod.set_as_default"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          >
          <label for="set-as-default" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
            设置为默认支付方式
          </label>
        </div>

        <div class="flex space-x-4">
          <button 
            type="button"
            @click="showAddForm = false"
            class="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button 
            type="submit"
            :disabled="paymentStore.loading || !newPaymentMethod.type"
            class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="paymentStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ paymentStore.loading ? '添加中...' : '添加支付方式' }}
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- 删除确认弹窗 -->
  <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
      <div class="text-center mb-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">确认删除</h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400">您确定要删除这个支付方式吗？</p>
      </div>

      <div class="flex space-x-4">
        <button 
          @click="showDeleteConfirm = false"
          class="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          取消
        </button>
        <button 
          @click="deletePaymentMethod"
          :disabled="paymentStore.loading"
          class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="paymentStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          {{ paymentStore.loading ? '删除中...' : '删除' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePaymentStore } from '../../stores/payment.store';

const paymentStore = usePaymentStore();
const showAddForm = ref(false);
const showDeleteConfirm = ref(false);
const successMessage = ref<string | null>(null);
const methodToDelete = ref<string>('');

const newPaymentMethod = ref({
  type: '',
  provider: '',
  details: {
    number: '',
    expiry_month: undefined,
    expiry_year: undefined,
    cvc: '',
    email: '',
    wallet_address: '',
    bank_account: {
      account_number: '',
      routing_number: '',
      account_holder_name: ''
    }
  },
  set_as_default: false
});

// 加载支付方式
onMounted(async () => {
  await paymentStore.fetchPaymentMethods();
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

// 添加支付方式
const addPaymentMethod = async () => {
  if (!newPaymentMethod.value.type) return;

  try {
    // 设置 provider
    newPaymentMethod.value.provider = 
      newPaymentMethod.value.type === 'credit_card' ? 'stripe' :
      newPaymentMethod.value.type === 'paypal' ? 'paypal' :
      newPaymentMethod.value.type === 'crypto' ? 'crypto' : 'bank';

    await paymentStore.addPaymentMethod(newPaymentMethod.value);
    
    // 重置表单
    resetForm();
    showAddForm.value = false;
    successMessage.value = '支付方式添加成功';
    
    // 3秒后清除成功信息
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (error) {
    console.error('添加支付方式失败:', error);
  }
};

// 重置表单
const resetForm = () => {
  newPaymentMethod.value = {
    type: '',
    provider: '',
    details: {
      number: '',
      expiry_month: undefined,
      expiry_year: undefined,
      cvc: '',
      email: '',
      wallet_address: '',
      bank_account: {
        account_number: '',
        routing_number: '',
        account_holder_name: ''
      }
    },
    set_as_default: false
  };
};

// 设置默认支付方式
const setDefaultMethod = async (methodId: string) => {
  try {
    await paymentStore.setDefaultPaymentMethod(methodId);
    successMessage.value = '默认支付方式设置成功';
    
    // 3秒后清除成功信息
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (error) {
    console.error('设置默认支付方式失败:', error);
  }
};

// 确认删除
const confirmDelete = (methodId: string) => {
  methodToDelete.value = methodId;
  showDeleteConfirm.value = true;
};

// 删除支付方式
const deletePaymentMethod = async () => {
  if (!methodToDelete.value) return;

  try {
    await paymentStore.deletePaymentMethod(methodToDelete.value);
    showDeleteConfirm.value = false;
    successMessage.value = '支付方式删除成功';
    
    // 3秒后清除成功信息
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  } catch (error) {
    console.error('删除支付方式失败:', error);
  }
};
</script>

<style scoped>
/* 组件特定样式 */
</style>
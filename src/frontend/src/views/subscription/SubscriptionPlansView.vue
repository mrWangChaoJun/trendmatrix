<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">选择适合您需求的订阅计划</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="subscriptionStore.error" class="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md">
      {{ subscriptionStore.error }}
    </div>

    <!-- 加载状态 -->
    <div v-if="subscriptionStore.loading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 订阅计划卡片 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div 
        v-for="plan in subscriptionStore.subscriptionPlans" 
        :key="plan.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="text-center mb-6">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ plan.name }}</h3>
            <p class="mt-2 text-gray-600 dark:text-gray-400">{{ plan.description }}</p>
            <div class="mt-4">
              <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ plan.price }}</span>
              <span class="text-gray-600 dark:text-gray-400">{{ plan.currency }}/{{ plan.billing_cycle }}</span>
            </div>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">包含功能</h4>
            <ul class="space-y-2">
              <li v-for="(feature, index) in plan.features" :key="index" class="flex items-start">
                <svg class="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-gray-600 dark:text-gray-400">{{ feature }}</span>
              </li>
            </ul>
          </div>

          <div class="mb-6">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">使用限制</h4>
            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-400">API 调用限制</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ plan.api_rate_limit }} 次/分钟</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600 dark:text-gray-400">信号生成限制</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ plan.signal_limit }} 个/月</span>
              </div>
            </div>
          </div>

          <button 
            @click="selectPlan(plan)"
            :disabled="subscriptionStore.loading"
            class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            选择计划
          </button>
        </div>
      </div>
    </div>

    <!-- 选择计划弹窗 -->
    <div v-if="selectedPlan" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
        <div class="text-center mb-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">确认订阅</h3>
          <p class="mt-2 text-gray-600 dark:text-gray-400">您选择了 {{ selectedPlan.name }} 计划</p>
          <div class="mt-4">
            <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ selectedPlan.price }}</span>
            <span class="text-gray-600 dark:text-gray-400">{{ selectedPlan.currency }}/{{ selectedPlan.billing_cycle }}</span>
          </div>
        </div>

        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">支付方式</h4>
          <div v-if="paymentStore.userPaymentMethods.length > 0">
            <div 
              v-for="method in paymentStore.userPaymentMethods" 
              :key="method.id"
              class="flex items-center p-3 border border-gray-200 dark:border-gray-700 rounded-md mb-2 cursor-pointer"
              :class="{ 'border-blue-500 bg-blue-50 dark:bg-blue-900/30': selectedPaymentMethodId === method.id }"
              @click="selectedPaymentMethodId = method.id"
            >
              <div class="flex items-center">
                <input 
                  type="radio" 
                  :id="`payment-${method.id}`"
                  :name="'payment-method'"
                  :checked="selectedPaymentMethodId === method.id"
                  @change="selectedPaymentMethodId = method.id"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                >
                <label 
                  :for="`payment-${method.id}`"
                  class="ml-2 block text-sm text-gray-900 dark:text-gray-300"
                >
                  {{ method.type === 'credit_card' ? `${method.brand} ****${method.last_four}` : method.type }}
                </label>
              </div>
              <div v-if="method.is_default" class="ml-auto">
                <span class="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/50 px-2 py-0.5 rounded">默认</span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4">
            <p class="text-gray-600 dark:text-gray-400 mb-4">您还没有添加支付方式</p>
            <router-link 
              to="/payment/methods"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              添加支付方式
            </router-link>
          </div>
        </div>

        <div class="flex items-center mb-6">
          <input 
            type="checkbox" 
            id="auto-renew"
            v-model="autoRenew"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          >
          <label for="auto-renew" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
            自动续费
          </label>
        </div>

        <div class="flex space-x-4">
          <button 
            @click="selectedPlan = null"
            class="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button 
            @click="confirmSubscription"
            :disabled="subscriptionStore.loading || !selectedPaymentMethodId"
            class="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="subscriptionStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ subscriptionStore.loading ? '处理中...' : '确认订阅' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSubscriptionStore } from '../../stores/subscription.store';
import { usePaymentStore } from '../../stores/payment.store';
import { SubscriptionPlan } from '../../services/api/subscription.service';

const router = useRouter();
const subscriptionStore = useSubscriptionStore();
const paymentStore = usePaymentStore();

const selectedPlan = ref<SubscriptionPlan | null>(null);
const selectedPaymentMethodId = ref<string>('');
const autoRenew = ref(true);

// 加载订阅计划和支付方式
onMounted(async () => {
  await subscriptionStore.fetchSubscriptionPlans();
  await paymentStore.fetchPaymentMethods();
  
  // 设置默认支付方式
  if (paymentStore.defaultPaymentMethod) {
    selectedPaymentMethodId.value = paymentStore.defaultPaymentMethod.id;
  }
});

// 选择计划
const selectPlan = (plan: SubscriptionPlan) => {
  selectedPlan.value = plan;
};

// 确认订阅
const confirmSubscription = async () => {
  if (!selectedPlan.value || !selectedPaymentMethodId.value) {
    return;
  }

  try {
    await subscriptionStore.createSubscription({
      plan_id: selectedPlan.value.id,
      payment_method_id: selectedPaymentMethodId.value,
      auto_renew: autoRenew.value
    });
    
    // 订阅成功后跳转到我的订阅页面
    router.push('/subscription/my');
  } catch (error) {
    console.error('订阅失败:', error);
  }
};
</script>

<style scoped>
/* 组件特定样式 */
</style>
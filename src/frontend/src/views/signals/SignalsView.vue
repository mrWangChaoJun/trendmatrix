<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">实时信号和市场趋势</p>

    <!-- 筛选和搜索 -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mt-6 gap-4">
      <div class="relative">
        <input
          type="text"
          v-model="searchTerm"
          placeholder="搜索资产..."
          class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        >
        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
      <div class="relative">
        <select
          v-model="selectedSignalType"
          class="pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        >
          <option value="">所有类型</option>
          <option value="trend">趋势</option>
          <option value="momentum">动量</option>
          <option value="reversal">反转</option>
          <option value="volume">交易量</option>
        </select>
        <svg class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>
    </div>

    <!-- 信号列表 -->
    <div class="mt-6 overflow-x-auto">
      <table class="min-w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
        <thead class="bg-gray-100 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">资产</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">类型</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">强度</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">时间</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="signal in filteredSignals" :key="signal.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900 dark:text-white">{{ signal.asset }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', getSignalTypeClass(signal.type)]">
                {{ signal.type }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div :class="['h-2 rounded-full', getSignalStrengthClass(signal.strength)]" :style="{ width: signal.strength + '%' }"></div>
                </div>
                <span class="ml-2 text-xs text-gray-600 dark:text-gray-400">{{ signal.strength }}%</span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
              {{ formatTime(signal.timestamp) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { localDbService } from '@/services/db/local-db.service';

// 响应式数据
const searchTerm = ref('');
const selectedSignalType = ref('');
const signals = ref<any[]>([]);
const isLoading = ref(false);

// 计算属性
const filteredSignals = computed(() => {
  return signals.value.filter(signal => {
    const matchesSearch = signal.asset.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesType = !selectedSignalType.value || signal.type === selectedSignalType.value;
    return matchesSearch && matchesType;
  });
});

// 加载数据
const loadData = async () => {
  isLoading.value = true;
  try {
    // 获取信号数据
    const signalData = await localDbService.getRecentSignals(20); // 获取更多信号
    signals.value = signalData;
  } catch (error) {
    console.error('Error loading signals:', error);
  } finally {
    isLoading.value = false;
  }
};

// 获取信号类型的样式类
const getSignalTypeClass = (type: string) => {
  const typeClasses: Record<string, string> = {
    trend: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    momentum: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    reversal: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    volume: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
  };
  return typeClasses[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200';
};

// 获取信号强度的样式类
const getSignalStrengthClass = (strength: number) => {
  if (strength >= 80) return 'bg-green-500';
  if (strength >= 60) return 'bg-yellow-500';
  if (strength >= 40) return 'bg-orange-500';
  return 'bg-red-500';
};

// 格式化时间
const formatTime = (timestamp: string) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(timestamp));
};

// 生命周期钩子
onMounted(() => {
  // 初始化时直接加载数据
  loadData();
});
</script>

<style scoped>
/* 组件特定样式 */
</style>

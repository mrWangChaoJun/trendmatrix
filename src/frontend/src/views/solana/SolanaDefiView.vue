<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">Solana DeFi 协议分析</p>

    <!-- 市场概览指标 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">总协议数</h3>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ protocols.length }}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">总锁仓价值 (TVL)</h3>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ totalTvl.toLocaleString() }}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">24h 总交易量</h3>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ totalVolume.toLocaleString() }}</p>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mt-6 gap-4">
      <div class="relative">
        <input
          type="text"
          v-model="searchTerm"
          placeholder="搜索协议..."
          class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        >
        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
      <div class="flex items-center gap-2">
        <label class="text-sm font-medium text-gray-700 dark:text-gray-300">分类:</label>
        <select v-model="selectedCategory" class="border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white">
          <option value="">全部</option>
          <option value="AMM">AMM</option>
          <option value="DEX">DEX</option>
          <option value="Staking">Staking</option>
          <option value="Aggregator">Aggregator</option>
          <option value="DNS">DNS</option>
        </select>
      </div>
    </div>

    <!-- DeFi 协议表格 -->
    <div class="mt-6 overflow-x-auto">
      <table class="min-w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
        <thead class="bg-gray-100 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">协议名称</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">分类</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">TVL</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">24h 交易量</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">24h 变化</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户数</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">链接</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="protocol in filteredProtocols" :key="protocol.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900 dark:text-white">{{ protocol.name }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">{{ protocol.category }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">${{ protocol.tvl.toLocaleString() }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">${{ protocol.volume_24h.toLocaleString() }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="protocol.change_24h >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                {{ protocol.change_24h >= 0 ? '+' : '' }}{{ protocol.change_24h }}%
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">{{ protocol.users.toLocaleString() }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex space-x-2">
                <a :href="protocol.url" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.39-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 14.97 6.118 13.546 6.03 12H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd"></path>
                  </svg>
                </a>
                <a :href="protocol.twitter" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-blue-500">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
                  </svg>
                </a>
                <a v-if="protocol.github" :href="protocol.github" target="_blank" rel="noopener noreferrer" class="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
                  </svg>
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { localDbService, DefiProtocol } from '@/services/db/local-db.service';

const protocols = ref<DefiProtocol[]>([]);
const searchTerm = ref('');
const selectedCategory = ref('');

// 计算属性
const filteredProtocols = computed(() => {
  return protocols.value.filter(protocol => {
    const matchesSearch = protocol.name.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesCategory = !selectedCategory.value || protocol.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

const totalTvl = computed(() => {
  return protocols.value.reduce((sum, protocol) => sum + protocol.tvl, 0);
});

const totalVolume = computed(() => {
  return protocols.value.reduce((sum, protocol) => sum + protocol.volume_24h, 0);
});

// 生命周期钩子
onMounted(async () => {
  try {
    protocols.value = await localDbService.getDefiProtocols();
  } catch (error) {
    console.error('Error fetching DeFi protocols:', error);
  }
});
</script>

<style scoped>
/* 组件特定样式 */
</style>

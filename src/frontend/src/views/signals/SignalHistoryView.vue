<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">历史信号记录</p>

    <!-- 过滤和搜索 -->
    <div class="mt-4 flex flex-col md:flex-row gap-4">
      <div class="flex-1">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索信号..."
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        />
      </div>
      <div class="flex gap-2">
        <select
          v-model="filterType"
          class="px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        >
          <option value="all">所有类型</option>
          <option value="trend">趋势</option>
          <option value="momentum">动量</option>
          <option value="reversal">反转</option>
        </select>
        <button
          @click="loadSignals"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          刷新
        </button>
      </div>
    </div>

    <!-- 信号列表 -->
    <div class="mt-6">
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h3 class="font-medium text-gray-900 dark:text-white">历史信号</h3>
          <span class="text-sm text-gray-600 dark:text-gray-400">{{ filteredSignals.length }} 个信号</span>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">资产</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">类型</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">强度</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">时间</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="signal in paginatedSignals" :key="signal.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td class="px-4 py-3 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ signal.asset }}</div>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', getSignalTypeClass(signal.type)]">
                    {{ signal.type }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div :class="['h-2 rounded-full', getSignalStrengthClass(signal.strength)]" :style="{ width: signal.strength + '%' }"></div>
                    </div>
                    <span class="ml-2 text-xs text-gray-600 dark:text-gray-400">{{ signal.strength }}%</span>
                  </div>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                  {{ formatTime(signal.timestamp) }}
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
                  <router-link :to="`/signals/${signal.id}`" class="text-blue-600 dark:text-blue-400 hover:underline">查看详情</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- 分页 -->
        <div class="card-footer flex items-center justify-between px-4 py-3">
          <div class="text-sm text-gray-600 dark:text-gray-400">
            显示 {{ (currentPage - 1) * pageSize + 1 }} 到 {{ Math.min(currentPage * pageSize, filteredSignals.length) }} 共 {{ filteredSignals.length }} 个信号
          </div>
          <div class="flex space-x-2">
            <button
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 dark:border-gray-700 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <button
              @click="currentPage = Math.min(Math.ceil(filteredSignals.length / pageSize), currentPage + 1)"
              :disabled="currentPage === Math.ceil(filteredSignals.length / pageSize)"
              class="px-3 py-1 border border-gray-300 dark:border-gray-700 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import localDbService from '../../services/db/local-db.service'

// 状态数据
const isLoading = ref(false)
const error = ref('')
const signals = ref<any[]>([])
const searchQuery = ref('')
const filterType = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)



// 计算属性
const filteredSignals = computed(() => {
  let result = [...signals.value]

  // 按搜索词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(signal =>
      signal.asset.toLowerCase().includes(query)
    )
  }

  // 按类型过滤
  if (filterType.value !== 'all') {
    result = result.filter(signal => signal.type === filterType.value)
  }

  // 按时间排序
  result.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())

  return result
})

const paginatedSignals = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredSignals.value.slice(start, end)
})

// 工具函数
function getSignalTypeClass(type: string): string {
  const classes = {
    trend: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    momentum: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    reversal: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return classes[type as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
}

function getSignalStrengthClass(strength: number): string {
  if (strength >= 80) return 'bg-green-500'
  if (strength >= 60) return 'bg-yellow-500'
  if (strength >= 40) return 'bg-orange-500'
  return 'bg-red-500'
}

function formatTime(timestamp: string): string {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(timestamp))
}

// 加载信号数据
async function loadSignals() {
  isLoading.value = true
  error.value = ''
  try {
    // 从本地数据库获取信号数据
    const recentSignals = await localDbService.getRecentSignals(50) // 获取更多信号用于历史记录
    signals.value = recentSignals
    currentPage.value = 1 // 重置到第一页
  } catch (err) {
    error.value = '获取信号数据失败'
    console.error('Error loading signals:', err)
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadSignals()
})
</script>

<style scoped>
/* 组件特定样式 */
</style>

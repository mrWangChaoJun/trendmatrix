<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">信号详细信息与分析</p>

    <!-- 返回按钮 -->
    <div class="mt-4">
      <router-link to="/signals/history" class="inline-flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        返回信号历史
      </router-link>
    </div>

    <!-- 信号详情 -->
    <div class="mt-6">
      <div class="card">
        <div class="card-header">
          <h3 class="font-medium text-gray-900 dark:text-white">信号信息</h3>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="flex justify-center items-center py-10">
            <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
          </div>
          <div v-else-if="error" class="text-red-600 dark:text-red-400 py-4">
            {{ error }}
          </div>
          <div v-else-if="signal" class="space-y-6">
            <!-- 基本信息 -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">资产</p>
                <h4 class="text-xl font-bold text-gray-900 dark:text-white mt-1">{{ signal.asset }}</h4>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">信号类型</p>
                <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-1', getSignalTypeClass(signal.type)]">
                  {{ signal.type }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">信号强度</p>
                <div class="mt-1 flex items-center">
                  <div class="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div :class="['h-2 rounded-full', getSignalStrengthClass(signal.strength)]" :style="{ width: signal.strength + '%' }"></div>
                  </div>
                  <span class="ml-2 text-sm font-medium text-gray-900 dark:text-white">{{ signal.strength }}%</span>
                </div>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">生成时间</p>
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mt-1">{{ formatTime(signal.timestamp) }}</h4>
              </div>
            </div>

            <!-- 技术指标分析 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">技术指标分析</h4>
              <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div v-for="indicator in technicalIndicators" :key="indicator.name" class="bg-white dark:bg-gray-700 p-3 rounded-md">
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ indicator.name }}</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ indicator.value }}</p>
                    <span :class="['text-xs mt-1 inline-block', indicator.trend >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                      {{ indicator.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(indicator.trend) }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 信号分析 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">信号分析</h4>
              <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
                <p class="text-gray-600 dark:text-gray-400 mb-4">
                  {{ getSignalAnalysis(signal) }}
                </p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div class="bg-white dark:bg-gray-700 p-3 rounded-md">
                    <p class="text-sm text-gray-600 dark:text-gray-400">预测方向</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ getPredictionDirection(signal) }}</p>
                  </div>
                  <div class="bg-white dark:bg-gray-700 p-3 rounded-md">
                    <p class="text-sm text-gray-600 dark:text-gray-400">置信度</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ signal.strength }}%</p>
                  </div>
                  <div class="bg-white dark:bg-gray-700 p-3 rounded-md">
                    <p class="text-sm text-gray-600 dark:text-gray-400">建议操作</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ getRecommendedAction(signal) }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 市场情绪分析 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">市场情绪分析</h4>
              <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div class="flex justify-between mb-2">
                      <p class="text-sm text-gray-600 dark:text-gray-400">市场情绪</p>
                      <span :class="['text-sm font-medium', marketSentiment.score >= 50 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                        {{ marketSentiment.label }}
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div class="bg-blue-500 h-2 rounded-full" :style="{ width: marketSentiment.score + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between mb-2">
                      <p class="text-sm text-gray-600 dark:text-gray-400">交易量变化</p>
                      <span :class="['text-sm font-medium', marketSentiment.volumeChange >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                        {{ marketSentiment.volumeChange >= 0 ? '+' : '' }}{{ marketSentiment.volumeChange }}%
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" :style="{ width: (50 + marketSentiment.volumeChange) + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 相关资产 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">相关资产</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <div v-for="asset in relatedAssets" :key="asset.symbol" class="bg-white dark:bg-gray-700 p-3 rounded-md border border-gray-200 dark:border-gray-600 hover:shadow-md transition-shadow">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="font-medium text-gray-900 dark:text-white">{{ asset.symbol }}</p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ asset.name }}</p>
                    </div>
                    <span :class="['text-sm font-medium', asset.change >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                      {{ asset.change >= 0 ? '+' : '' }}{{ asset.change }}%
                    </span>
                  </div>
                  <div class="mt-2">
                    <p class="text-xs text-gray-600 dark:text-gray-400">市值</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ asset.marketCap }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 历史信号 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">历史信号</h4>
              <div class="bg-white dark:bg-gray-700 rounded-md border border-gray-200 dark:border-gray-600 overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        日期
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        类型
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        强度
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        结果
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="(historyItem, index) in historicalSignals" :key="index">
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ historyItem.date }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', getSignalTypeClass(historyItem.type)]">
                          {{ historyItem.type }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ historyItem.strength }}%
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="['text-sm font-medium', historyItem.result >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                          {{ historyItem.result >= 0 ? '+' : '' }}{{ historyItem.result }}%
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-600 dark:text-gray-400 py-4">
            信号不存在或已被删除
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import localDbService from '../../services/db/local-db.service'

// 状态数据
const isLoading = ref(false)
const error = ref('')
const signal = ref<any>(null)
const relatedAssets = ref<any[]>([])
const technicalIndicators = ref<any[]>([])
const marketSentiment = ref<any>(null)
const historicalSignals = ref<any[]>([])

// 路由
const route = useRoute()
const router = useRouter()

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
    minute: '2-digit',
    second: '2-digit'
  }).format(new Date(timestamp))
}

function getSignalAnalysis(signal: any): string {
  const analyses = {
    trend: `基于${signal.asset}的长期价格走势分析，我们检测到明显的${signal.strength > 70 ? '强' : '中'}趋势信号。价格在过去${Math.floor(Math.random() * 30) + 7}天内${Math.random() > 0.5 ? '持续上涨' : '持续下跌'}，成交量${Math.random() > 0.5 ? '明显增加' : '保持稳定'}，表明市场对该资产的${Math.random() > 0.5 ? '买入' : '卖出'}兴趣${signal.strength > 70 ? '强烈' : '适中'}。`,
    momentum: `动量分析显示${signal.asset}当前处于${signal.strength > 70 ? '强劲' : '中等'}动量状态。过去${Math.floor(Math.random() * 14) + 3}天的价格变化率${Math.random() > 0.5 ? '显著' : '逐步'}${Math.random() > 0.5 ? '上升' : '下降'}，相对强弱指标(RSI)位于${Math.floor(Math.random() * 30) + 50}水平，表明${Math.random() > 0.5 ? '超买' : '超卖'}状态可能${Math.random() > 0.5 ? '即将出现' : '已经形成'}。`,
    reversal: `反转信号分析显示${signal.asset}可能即将出现${signal.strength > 70 ? '强烈' : '中等'}反转。价格在${Math.floor(Math.random() * 60) + 30}天内形成了${Math.random() > 0.5 ? '双底' : '双顶'}形态，同时MACD指标${Math.random() > 0.5 ? '金叉' : '死叉'}，成交量${Math.random() > 0.5 ? '明显放大' : '开始萎缩'}，这些都是${Math.random() > 0.5 ? '看涨' : '看跌'}反转的重要信号。`
  }
  return analyses[signal.type as keyof typeof analyses] || '信号分析数据不可用'
}

function getPredictionDirection(signal: any): string {
  if (signal.type === 'trend') {
    return Math.random() > 0.5 ? '上涨' : '下跌'
  } else if (signal.type === 'momentum') {
    return Math.random() > 0.5 ? '继续上涨' : '继续下跌'
  } else if (signal.type === 'reversal') {
    return Math.random() > 0.5 ? '反转上涨' : '反转下跌'
  }
  return '未知'
}

function getRecommendedAction(signal: any): string {
  if (signal.strength >= 80) {
    return signal.type === 'reversal' ? '强烈建议关注' : '强烈建议操作'
  } else if (signal.strength >= 60) {
    return '建议谨慎操作'
  } else {
    return '建议观望'
  }
}

// 生成技术指标数据
function generateTechnicalIndicators(): any[] {
  return [
    {
      name: 'RSI (14)',
      value: (Math.random() * 40 + 30).toFixed(1),
      trend: (Math.random() * 10 - 5).toFixed(1)
    },
    {
      name: 'MACD',
      value: (Math.random() * 2 - 1).toFixed(3),
      trend: (Math.random() * 15 - 7.5).toFixed(1)
    },
    {
      name: '布林带',
      value: (Math.random() * 0.1 + 0.05).toFixed(3),
      trend: (Math.random() * 20 - 10).toFixed(1)
    },
    {
      name: 'MA (50)',
      value: (Math.random() * 10000 + 1000).toFixed(2),
      trend: (Math.random() * 8 - 4).toFixed(1)
    }
  ].map(indicator => ({
    ...indicator,
    trend: parseFloat(indicator.trend)
  }))
}

// 生成市场情绪数据
function generateMarketSentiment(): any {
  const score = Math.floor(Math.random() * 50) + 30
  let label = '中性'

  if (score >= 70) {
    label = '极度看涨'
  } else if (score >= 55) {
    label = '看涨'
  } else if (score >= 45) {
    label = '中性'
  } else if (score >= 30) {
    label = '看跌'
  } else {
    label = '极度看跌'
  }

  return {
    score,
    label,
    volumeChange: (Math.random() * 30 - 10).toFixed(1)
  }
}

// 生成相关资产数据
function generateRelatedAssets(baseAsset: string): any[] {
  const assets = [
    { symbol: 'BTC', name: 'Bitcoin', change: (Math.random() * 10 - 3).toFixed(2), marketCap: '1.2T' },
    { symbol: 'ETH', name: 'Ethereum', change: (Math.random() * 15 - 5).toFixed(2), marketCap: '450B' },
    { symbol: 'SOL', name: 'Solana', change: (Math.random() * 20 - 8).toFixed(2), marketCap: '80B' },
    { symbol: 'ADA', name: 'Cardano', change: (Math.random() * 12 - 4).toFixed(2), marketCap: '40B' },
    { symbol: 'DOT', name: 'Polkadot', change: (Math.random() * 18 - 6).toFixed(2), marketCap: '30B' },
    { symbol: 'DOGE', name: 'Dogecoin', change: (Math.random() * 25 - 10).toFixed(2), marketCap: '25B' }
  ]

  // 过滤掉基础资产，然后随机选择4个
  return assets
    .filter(asset => asset.symbol !== baseAsset)
    .sort(() => Math.random() - 0.5)
    .slice(0, 4)
    .map(asset => ({
      ...asset,
      change: parseFloat(asset.change)
    }))
}

// 生成历史信号数据
function generateHistoricalSignals(asset: string): any[] {
  const types = ['trend', 'momentum', 'reversal']
  const history = []
  const today = new Date()

  for (let i = 1; i <= 7; i++) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)

    history.push({
      date: date.toLocaleDateString('zh-CN'),
      type: types[Math.floor(Math.random() * types.length)],
      strength: Math.floor(Math.random() * 40) + 40,
      result: (Math.random() * 15 - 5).toFixed(1)
    })
  }

  return history.map(item => ({
    ...item,
    result: parseFloat(item.result)
  }))
}

// 加载信号数据
async function loadSignalDetail() {
  const signalId = route.params.id as string
  isLoading.value = true
  error.value = ''

  try {
    // 从本地数据库获取信号数据
    const signals = await localDbService.getRecentSignals(50)
    const foundSignal = signals.find((s: any) => s.id === signalId)

    if (foundSignal) {
      signal.value = foundSignal

      // 生成相关数据
      relatedAssets.value = generateRelatedAssets(foundSignal.asset)
      technicalIndicators.value = generateTechnicalIndicators()
      marketSentiment.value = generateMarketSentiment()
      historicalSignals.value = generateHistoricalSignals(foundSignal.asset)
    } else {
      // 如果找不到对应ID的信号，使用第一个信号作为示例
      if (signals.length > 0) {
        signal.value = signals[0]
        relatedAssets.value = generateRelatedAssets(signals[0].asset)
        technicalIndicators.value = generateTechnicalIndicators()
        marketSentiment.value = generateMarketSentiment()
        historicalSignals.value = generateHistoricalSignals(signals[0].asset)
      }
    }
  } catch (err) {
    error.value = '获取信号详情失败'
    console.error('Error loading signal detail:', err)
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadSignalDetail()
})
</script>

<style scoped>
/* 组件特定样式 */
</style>

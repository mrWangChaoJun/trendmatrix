<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">Solana 项目详细分析</p>

    <!-- 返回按钮 -->
    <div class="mt-4">
      <router-link to="/solana" class="inline-flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        返回Solana生态
      </router-link>
    </div>

    <!-- 项目详情 -->
    <div class="mt-6">
      <div class="card">
        <div class="card-body">
          <div v-if="isLoading" class="flex justify-center items-center py-10">
            <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
          </div>
          <div v-else-if="error" class="text-red-600 dark:text-red-400 py-4">
            {{ error }}
          </div>
          <div v-else-if="project" class="space-y-6">
            <!-- 项目基本信息 -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ project.name }}</h3>
                <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2', getCategoryClass(project.category)]">
                  {{ project.category }}
                </span>
                <p class="text-gray-600 dark:text-gray-400 mt-4">
                  {{ project.description }}
                </p>
                <div class="mt-4 flex space-x-4">
                  <a v-if="project.website" :href="project.website" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    官网
                  </a>
                  <a v-if="project.twitter" :href="project.twitter" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
                    </svg>
                    Twitter
                  </a>
                  <a v-if="project.github" :href="project.github" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
                    </svg>
                    GitHub
                  </a>
                </div>
              </div>
              <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-md">
                <div class="space-y-4">
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">项目得分</p>
                    <div class="flex items-center mt-1">
                      <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ project.score }}</span>
                      <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">/100</span>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">市场表现</p>
                    <div class="flex items-center mt-1">
                      <span :class="['text-lg font-medium', project.change >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                        {{ project.change >= 0 ? '+' : '' }}{{ project.change }}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">上市时间</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white mt-1">{{ project.launchDate }}</p>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">代币</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white mt-1">{{ project.token }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 市场数据 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">市场数据</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">当前价格</p>
                  <p class="text-xl font-bold text-gray-900 dark:text-white mt-1">${{ project.marketData.price.toFixed(2) }}</p>
                </div>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">24h 高/低</p>
                  <p class="text-xl font-bold text-gray-900 dark:text-white mt-1">${{ project.marketData.high24h.toFixed(2) }} / ${{ project.marketData.low24h.toFixed(2) }}</p>
                </div>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">7d 变化</p>
                  <p :class="['text-xl font-bold mt-1', project.marketData.change7d >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                    {{ project.marketData.change7d >= 0 ? '+' : '' }}{{ project.marketData.change7d.toFixed(2) }}%
                  </p>
                </div>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">市值</p>
                  <p class="text-xl font-bold text-gray-900 dark:text-white mt-1">${{ formatMarketCap(project.marketData.marketCap) }}</p>
                </div>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">24h交易量</p>
                  <p class="text-xl font-bold text-gray-900 dark:text-white mt-1">${{ formatMarketCap(project.marketData.volume24h) }}</p>
                </div>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                  <p class="text-sm text-gray-600 dark:text-gray-400">流通供应量</p>
                  <p class="text-xl font-bold text-gray-900 dark:text-white mt-1">{{ formatSupply(project.marketData.circulatingSupply) }}</p>
                </div>
              </div>
            </div>

            <!-- 项目趋势图表 -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-lg font-medium text-gray-900 dark:text-white">价格趋势</h4>
                <div class="flex space-x-2">
                  <button @click="timeRange = '7d'" :class="['px-3 py-1 text-sm rounded-md', timeRange === '7d' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200']">7天</button>
                  <button @click="timeRange = '30d'" :class="['px-3 py-1 text-sm rounded-md', timeRange === '30d' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200']">30天</button>
                  <button @click="timeRange = '90d'" :class="['px-3 py-1 text-sm rounded-md', timeRange === '90d' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200']">90天</button>
                </div>
              </div>
              <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                <div ref="priceChart" class="h-64"></div>
              </div>
            </div>

            <!-- 交易量图表 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">交易量趋势</h4>
              <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                <div ref="volumeChart" class="h-64"></div>
              </div>
            </div>

            <!-- 开发与社区分析 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- 开发活动 -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">开发活动</h4>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600 space-y-4">
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">代码提交</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.development.activity }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-blue-500 h-2 rounded-full" :style="{ width: project.development.activity + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">开发者数量</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.development.developers }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" :style="{ width: project.development.developers + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">代码质量</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.development.codeQuality }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-purple-500 h-2 rounded-full" :style="{ width: project.development.codeQuality + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">文档完整性</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.development.documentation }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: project.development.documentation + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 社区活跃度 -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">社区活跃度</h4>
                <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600 space-y-4">
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">社交媒体关注</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.community.socialMedia }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: project.community.socialMedia + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">社区参与</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.community.engagement }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-red-500 h-2 rounded-full" :style="{ width: project.community.engagement + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">用户增长</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.community.growth }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-indigo-500 h-2 rounded-full" :style="{ width: project.community.growth + '%' }"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-sm text-gray-600 dark:text-gray-400">社区支持</p>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.community.support }}</p>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" :style="{ width: project.community.support + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 项目风险评估 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">风险评估</h4>
              <div class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">市场风险</p>
                    <div class="mt-1 flex items-center">
                      <div class="flex">
                        <span v-for="i in 5" :key="i" :class="['w-4 h-4 rounded-full mx-0.5', i <= project.risk.market ? 'bg-red-500' : 'bg-gray-200 dark:bg-gray-600']"></span>
                      </div>
                      <span class="ml-2 text-sm font-medium text-gray-900 dark:text-white">{{ project.risk.market }}/5</span>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">技术风险</p>
                    <div class="mt-1 flex items-center">
                      <div class="flex">
                        <span v-for="i in 5" :key="i" :class="['w-4 h-4 rounded-full mx-0.5', i <= project.risk.technical ? 'bg-red-500' : 'bg-gray-200 dark:bg-gray-600']"></span>
                      </div>
                      <span class="ml-2 text-sm font-medium text-gray-900 dark:text-white">{{ project.risk.technical }}/5</span>
                    </div>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">监管风险</p>
                    <div class="mt-1 flex items-center">
                      <div class="flex">
                        <span v-for="i in 5" :key="i" :class="['w-4 h-4 rounded-full mx-0.5', i <= project.risk.regulatory ? 'bg-red-500' : 'bg-gray-200 dark:bg-gray-600']"></span>
                      </div>
                      <span class="ml-2 text-sm font-medium text-gray-900 dark:text-white">{{ project.risk.regulatory }}/5</span>
                    </div>
                  </div>
                </div>
                <div class="mt-4">
                  <p class="text-sm text-gray-600 dark:text-gray-400">风险评估总结</p>
                  <p class="text-sm text-gray-900 dark:text-white mt-1">{{ project.risk.summary }}</p>
                </div>
              </div>
            </div>

            <!-- 相关项目 -->
            <div>
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">相关项目</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div v-for="relatedProject in relatedProjects" :key="relatedProject.id" class="bg-white dark:bg-gray-700 p-4 rounded-md border border-gray-200 dark:border-gray-600 hover:shadow-md transition-shadow">
                  <h5 class="font-medium text-gray-900 dark:text-white">{{ relatedProject.name }}</h5>
                  <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium mt-1', getCategoryClass(relatedProject.category)]">
                    {{ relatedProject.category }}
                  </span>
                  <div class="flex items-center justify-between mt-4">
                    <span class="text-sm font-medium text-gray-900 dark:text-white">{{ relatedProject.score }}/100</span>
                    <span :class="['text-sm font-medium', relatedProject.change >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                      {{ relatedProject.change >= 0 ? '+' : '' }}{{ relatedProject.change }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-600 dark:text-gray-400 py-4">
            项目不存在或已被删除
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as d3 from 'd3'
import localDbService from '../../services/db/local-db.service'

// 状态数据
const isLoading = ref(false)
const error = ref('')
const project = ref<any>(null)
const relatedProjects = ref<any[]>([])
const priceChart = ref<HTMLElement | null>(null)
const volumeChart = ref<HTMLElement | null>(null)
const timeRange = ref('30d')

// 路由
const route = useRoute()
const router = useRouter()

// 监听时间范围变化，重新生成图表
watch(timeRange, () => {
  if (project.value) {
    nextTick(() => {
      generatePriceChart()
      generateVolumeChart()
    })
  }
})

// 工具函数
function getCategoryClass(category: string): string {
  const classes = {
    'Layer 1': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    'DEX': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    'AMM': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    'Staking': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    'GameFi': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return classes[category as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
}

function formatMarketCap(value: number): string {
  if (value >= 1000000000) {
    return (value / 1000000000).toFixed(2) + 'B'
  } else if (value >= 1000000) {
    return (value / 1000000).toFixed(2) + 'M'
  } else if (value >= 1000) {
    return (value / 1000).toFixed(2) + 'K'
  }
  return value.toString()
}

function formatSupply(value: number): string {
  if (value >= 1000000000) {
    return (value / 1000000000).toFixed(2) + 'B'
  } else if (value >= 1000000) {
    return (value / 1000000).toFixed(2) + 'M'
  } else if (value >= 1000) {
    return (value / 1000).toFixed(2) + 'K'
  }
  return value.toString()
}

// 生成价格趋势图表
function generatePriceChart() {
  if (!priceChart.value || !project.value) return

  // 清除现有内容
  d3.select(priceChart.value).selectAll('*').remove()

  // 根据时间范围确定数据点数量
  let days = 30
  if (timeRange.value === '7d') {
    days = 7
  } else if (timeRange.value === '90d') {
    days = 90
  }

  // 生成模拟价格数据
  const data = []
  const today = new Date()
  let price = project.value.marketData.price

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)

    // 随机价格波动
    price += (Math.random() * 2 - 0.8) * price * 0.01

    data.push({
      date: date,
      price: price
    })
  }

  // 设置尺寸
  const width = priceChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(priceChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleTime()
    .domain(d3.extent(data, d => d.date) as [Date, Date])
    .range([0, innerWidth])

  const y = d3.scaleLinear()
    .domain([d3.min(data, d => d.price) as number * 0.95, d3.max(data, d => d.price) as number * 1.05])
    .range([innerHeight, 0])

  // 创建轴
  svg.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x))

  svg.append('g')
    .call(d3.axisLeft(y))

  // 创建折线图
  const line = d3.line<typeof data[0]>()
    .x(d => x(d.date) || 0)
    .y(d => y(d.price))
    .curve(d3.curveMonotoneX)

  svg.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', '#3b82f6')
    .attr('stroke-width', 2)
    .attr('d', line)

  // 添加数据点
  svg.selectAll('.dot')
    .data(data)
    .enter()
    .append('circle')
    .attr('class', 'dot')
    .attr('cx', d => x(d.date) || 0)
    .attr('cy', d => y(d.price))
    .attr('r', 3)
    .attr('fill', '#3b82f6')
}

// 生成交易量图表
function generateVolumeChart() {
  if (!volumeChart.value || !project.value) return

  // 清除现有内容
  d3.select(volumeChart.value).selectAll('*').remove()

  // 根据时间范围确定数据点数量
  let days = 30
  if (timeRange.value === '7d') {
    days = 7
  } else if (timeRange.value === '90d') {
    days = 90
  }

  // 生成模拟交易量数据
  const data = []
  const today = new Date()
  let baseVolume = project.value.marketData.volume24h

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)

    // 随机交易量波动
    const volume = baseVolume * (0.5 + Math.random())

    data.push({
      date: date,
      volume: volume
    })
  }

  // 设置尺寸
  const width = volumeChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(volumeChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleTime()
    .domain(d3.extent(data, d => d.date) as [Date, Date])
    .range([0, innerWidth])

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.volume) as number * 1.1])
    .range([innerHeight, 0])

  // 创建轴
  svg.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x))

  svg.append('g')
    .call(d3.axisLeft(y))

  // 创建柱状图
  svg.selectAll('.bar')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.date) || 0)
    .attr('y', d => y(d.volume))
    .attr('width', innerWidth / days - 2)
    .attr('height', d => innerHeight - y(d.volume))
    .attr('fill', '#10b981')
}

// 加载项目数据
async function loadProjectDetail() {
  const projectId = route.params.id as string
  isLoading.value = true
  error.value = ''

  try {
    // 从本地数据库获取热门项目数据
    const projects = await localDbService.getHotProjects(10)
    const foundProject = projects.find((p: any) => p.id === projectId)

    if (foundProject) {
      // 增强项目数据，添加更多详细信息
      project.value = enhanceProjectData(foundProject)
    } else {
      // 如果找不到对应ID的项目，使用第一个项目作为示例
      if (projects.length > 0) {
        project.value = enhanceProjectData(projects[0])
      } else {
        // 如果没有项目数据，生成一个默认项目
        project.value = generateDefaultProject()
      }
    }

    // 生成相关项目
    relatedProjects.value = generateRelatedProjects(project.value)

    // 等待DOM更新后生成图表
  await nextTick()
  generatePriceChart()
  generateVolumeChart()
} catch (err) {
  error.value = '获取项目详情失败'
  console.error('Error loading project detail:', err)
} finally {
  isLoading.value = false
}
}

// 增强项目数据
function enhanceProjectData(baseProject: any) {
  // 项目描述
  const descriptions = {
    'Solana': 'Solana是一个高性能的区块链平台，专为去中心化应用和加密货币而设计。它使用 Proof of History 和 Proof of Stake 共识机制，提供高吞吐量和低交易费用。',
    'Serum': 'Serum是建立在Solana上的去中心化交易所(DEX)，提供高速度、低成本的交易体验。它使用中央限价订单簿模型，支持复杂的交易策略。',
    'Raydium': 'Raydium是Solana上的自动做市商(AMM)和流动性提供者，与Serum DEX集成，为用户提供无缝的交易和流动性挖矿体验。',
    'Marinade Finance': 'Marinade Finance是Solana上的去中心化质押协议，允许用户质押SOL并获得mSOL代币，同时保持流动性。',
    'Star Atlas': 'Star Atlas是建立在Solana上的区块链太空模拟游戏，结合了DeFi、NFT和游戏元素，创建了一个虚拟宇宙经济系统。'
  }

  // 项目类别
  const categories = {
    'Solana': 'Layer 1',
    'Serum': 'DEX',
    'Raydium': 'AMM',
    'Marinade Finance': 'Staking',
    'Star Atlas': 'GameFi'
  }

  // 项目代币
  const tokens = {
    'Solana': 'SOL',
    'Serum': 'SRM',
    'Raydium': 'RAY',
    'Marinade Finance': 'MNDE',
    'Star Atlas': 'ATLAS'
  }

  // 项目链接
  const links = {
    'Solana': {
      website: 'https://solana.com',
      twitter: 'https://twitter.com/solana',
      github: 'https://github.com/solana-labs'
    },
    'Serum': {
      website: 'https://projectserum.com',
      twitter: 'https://twitter.com/projectserum',
      github: 'https://github.com/project-serum'
    },
    'Raydium': {
      website: 'https://raydium.io',
      twitter: 'https://twitter.com/raydiumprotocol',
      github: 'https://github.com/raydium-io'
    },
    'Marinade Finance': {
      website: 'https://marinade.finance',
      twitter: 'https://twitter.com/marinadefinance',
      github: 'https://github.com/marinade-finance'
    },
    'Star Atlas': {
      website: 'https://staratlas.com',
      twitter: 'https://twitter.com/staratlasgame',
      github: 'https://github.com/star-atlas'
    }
  }

  // 生成上市日期
  const launchDate = new Date()
  launchDate.setMonth(launchDate.getMonth() - Math.floor(Math.random() * 24) - 6) // 6-30个月前

  // 生成市场数据
  const price = Math.random() * 1000 + 1
  const marketCap = Math.random() * 10000000000 + 100000000
  const volume24h = Math.random() * 1000000000 + 10000000
  const circulatingSupply = Math.random() * 10000000000 + 100000000
  const high24h = price * (1 + Math.random() * 0.1)
  const low24h = price * (1 - Math.random() * 0.1)
  const change7d = (Math.random() * 30 - 10).toFixed(2)

  return {
    ...baseProject,
    description: descriptions[baseProject.name] || '这是一个Solana生态系统中的项目，提供创新的区块链解决方案。',
    category: categories[baseProject.name] || 'Other',
    token: tokens[baseProject.name] || 'TOKEN',
    launchDate: launchDate.toISOString().split('T')[0],
    website: links[baseProject.name]?.website || '',
    twitter: links[baseProject.name]?.twitter || '',
    github: links[baseProject.name]?.github || '',
    marketData: {
      price: price,
      marketCap: marketCap,
      volume24h: volume24h,
      circulatingSupply: circulatingSupply,
      high24h: high24h,
      low24h: low24h,
      change7d: parseFloat(change7d)
    },
    development: {
      activity: Math.floor(Math.random() * 50) + 30,
      developers: Math.floor(Math.random() * 40) + 20,
      codeQuality: Math.floor(Math.random() * 60) + 40,
      documentation: Math.floor(Math.random() * 70) + 20
    },
    community: {
      socialMedia: Math.floor(Math.random() * 60) + 20,
      engagement: Math.floor(Math.random() * 50) + 30,
      growth: Math.floor(Math.random() * 70) + 10,
      support: Math.floor(Math.random() * 60) + 30
    },
    risk: {
      market: Math.floor(Math.random() * 3) + 1,
      technical: Math.floor(Math.random() * 2) + 1,
      regulatory: Math.floor(Math.random() * 3) + 1,
      summary: '该项目风险较低，具有稳定的技术基础和良好的市场前景。建议投资者根据自身风险承受能力进行投资决策。'
    }
  }
}

// 生成默认项目
function generateDefaultProject() {
  const launchDate = new Date()
  launchDate.setMonth(launchDate.getMonth() - 12)

  return {
    id: 'default',
    name: 'Solana Project',
    category: 'Layer 1',
    token: 'SOL',
    score: 85,
    change: 5.2,
    description: '这是一个Solana生态系统中的项目，提供创新的区块链解决方案。该项目专注于提高区块链的可扩展性和安全性，为去中心化应用提供更好的基础设施。',
    launchDate: launchDate.toISOString().split('T')[0],
    website: 'https://example.com',
    twitter: 'https://twitter.com/example',
    github: 'https://github.com/example',
    marketData: {
      price: 100.50,
      marketCap: 40000000000,
      volume24h: 2000000000,
      circulatingSupply: 400000000,
      high24h: 105.25,
      low24h: 98.75,
      change7d: 8.5
    },
    development: {
      activity: 75,
      developers: 60,
      codeQuality: 80,
      documentation: 70
    },
    community: {
      socialMedia: 85,
      engagement: 70,
      growth: 65,
      support: 75
    },
    risk: {
      market: 2,
      technical: 1,
      regulatory: 2,
      summary: '该项目风险较低，具有稳定的技术基础和良好的市场前景。建议投资者根据自身风险承受能力进行投资决策。'
    }
  }
}

// 生成相关项目
function generateRelatedProjects(baseProject: any) {
  const projects = [
    { id: '1', name: 'Solana', category: 'Layer 1', score: 92, change: 8.5 },
    { id: '2', name: 'Serum', category: 'DEX', score: 88, change: 5.2 },
    { id: '3', name: 'Raydium', category: 'AMM', score: 85, change: 3.7 },
    { id: '4', name: 'Marinade Finance', category: 'Staking', score: 82, change: 2.1 },
    { id: '5', name: 'Star Atlas', category: 'GameFi', score: 79, change: 10.3 }
  ]

  // 过滤掉基础项目，然后随机选择4个
  return projects
    .filter(p => p.id !== baseProject.id && p.name !== baseProject.name)
    .sort(() => Math.random() - 0.5)
    .slice(0, 4)
}

// 组件挂载时加载数据
onMounted(() => {
  loadProjectDetail()
})
</script>

<style scoped>
/* 组件特定样式 */
</style>

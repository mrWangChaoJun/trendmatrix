<template>
  <div class="container mx-auto px-4 py-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-1">数据概览和趋势分析</p>
    </div>



    <!-- 关键指标卡片 -->
    <div v-if="isDataLoaded" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <!-- 总信号数 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总信号数</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ metrics.total_signals.toLocaleString() }}</h3>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                </svg>
                12.5% 较上周
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-secondary/20 dark:bg-secondary/30 flex items-center justify-center">
              <svg class="w-5 h-5 text-secondary dark:text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 活跃项目数 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">活跃项目数</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ metrics.active_projects }}</h3>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                </svg>
                8.2% 较上周
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-accent/20 dark:bg-accent/30 flex items-center justify-center">
              <svg class="w-5 h-5 text-accent dark:text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 市场情绪 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">市场情绪</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ metrics.market_sentiment }}</h3>
              <p class="text-xs text-yellow-600 dark:text-yellow-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-.77-1.964-.77-2.732 0L3.34 16c-.77.77-.77 1.964 0 2.732z"></path>
                </svg>
                {{ metrics.sentiment_score }}/100
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-primary/20 dark:bg-primary/30 flex items-center justify-center">
              <svg class="w-5 h-5 text-primary dark:text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Solana 生态活跃度 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Solana 生态活跃度</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ metrics.solana_activity }}%</h3>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                </svg>
                5.3% 较上周
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-neutral/20 dark:bg-neutral/30 flex items-center justify-center">
              <svg class="w-5 h-5 text-neutral dark:text-neutral" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div v-if="isDataLoaded" class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 信号趋势图表 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-primary dark:text-white">信号趋势</h3>
        </div>
        <div ref="signalTrendChart" class="h-64"></div>
      </div>

      <!-- 项目活跃度图表 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-secondary dark:text-white">项目活跃度</h3>
        </div>
        <div ref="projectActivityChart" class="h-64"></div>
      </div>

      <!-- 价格趋势图表 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-accent dark:text-white">价格趋势</h3>
        </div>
        <div ref="priceTrendChart" class="h-64"></div>
      </div>

      <!-- 交易量趋势图表 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-neutral dark:text-white">交易量趋势</h3>
        </div>
        <div ref="volumeTrendChart" class="h-64"></div>
      </div>
    </div>

    <!-- 最近信号和热门项目 -->
    <div v-if="isDataLoaded" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 最近信号 -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h3 class="font-medium text-primary dark:text-white">最近信号</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">资产</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">类型</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">强度</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">时间</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              <tr v-for="signal in recentSignals" :key="signal.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
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
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 热门项目 -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <div class="flex items-center gap-2">
              <h3 class="font-medium text-secondary dark:text-white">热门项目</h3>
              <select
                v-model="selectedProjectCategory"
                class="border border-gray-300 dark:border-gray-700 rounded-md px-2 py-1 text-sm dark:bg-gray-800 dark:text-white"
              >
                <option value="">全部类别</option>
                <option value="Layer 1">Layer 1</option>
                <option value="DEX">DEX</option>
                <option value="AMM">AMM</option>
                <option value="Staking">Staking</option>
                <option value="GameFi">GameFi</option>
              </select>
            </div>
        </div>
        <div class="p-4">
          <div v-for="project in filteredHotProjects" :key="project.id" class="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-0">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3">
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ project.name.charAt(0) }}</span>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ project.name }}</h4>
                <p class="text-xs text-gray-600 dark:text-gray-400">{{ project.category }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ project.score }}/100</p>
              <p :class="['text-xs', project.change >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400']">
                {{ project.change >= 0 ? '+' : '' }}{{ project.change }}%
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 初始化提示 -->
    <div v-else class="flex flex-col items-center justify-center py-16">
      <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">点击上方按钮加载数据</h3>
      <p class="text-gray-600 dark:text-gray-400 text-center max-w-md">
        为了优化性能，数据将在您点击后加载。这将显示最新的市场数据、信号趋势和项目活跃度。
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import * as d3 from 'd3'
import { localDbService } from '@/services/db/local-db.service'

// 图表引用
const signalTrendChart = ref<HTMLElement | null>(null)
const projectActivityChart = ref<HTMLElement | null>(null)
const priceTrendChart = ref<HTMLElement | null>(null)
const volumeTrendChart = ref<HTMLElement | null>(null)

// 状态数据
const isLoading = reactive({
  all: false
})

const error = reactive({
  data: ''
})



// 项目类别选择
const selectedProjectCategory = ref('')

// 数据加载状态
const isDataLoaded = ref(false)

// 数据模型
interface Signal {
  id: string;
  asset: string;
  type: string;
  strength: number;
  timestamp: string;
}

interface Project {
  id: string;
  name: string;
  category: string;
  score: number;
  change: number;
}

interface DashboardMetrics {
  total_signals: number;
  active_projects: number;
  market_sentiment: string;
  sentiment_score: number;
  solana_activity: number;
}

interface ChartData {
  date: string;
  signals: number;
  activity: number;
  price: number;
  volume: number;
}

// 数据状态
const recentSignals = ref<Signal[]>([])
const hotProjects = ref<Project[]>([])
const metrics = ref<DashboardMetrics>({
  total_signals: 0,
  active_projects: 0,
  market_sentiment: '中性',
  sentiment_score: 50,
  solana_activity: 0
})
const signalTrendData = ref<ChartData[]>([])
const projectActivityData = ref<ChartData[]>([])
const priceTrendData = ref<ChartData[]>([])
const volumeTrendData = ref<ChartData[]>([])

// 计算属性
const filteredHotProjects = computed(() => {
  if (!selectedProjectCategory.value) {
    return hotProjects.value
  }
  return hotProjects.value.filter(project => project.category === selectedProjectCategory.value)
})

// 工具函数
function getSignalTypeClass(type: string): string {
  const classes = {
    trend: 'bg-secondary/20 text-secondary dark:bg-secondary/30 dark:text-secondary',
    momentum: 'bg-accent/20 text-accent dark:bg-accent/30 dark:text-accent',
    reversal: 'bg-primary/20 text-primary dark:bg-primary/30 dark:text-primary'
  }
  return classes[type as keyof typeof classes] || 'bg-neutral/20 text-neutral dark:bg-neutral/30 dark:text-neutral'
}

function getSignalStrengthClass(strength: number): string {
  if (strength >= 80) return 'bg-secondary'
  if (strength >= 60) return 'bg-neutral'
  if (strength >= 40) return 'bg-accent'
  return 'bg-primary'
}

function formatTime(timestamp: string): string {
  return new Intl.DateTimeFormat('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(timestamp))
}

// 生成测试图表数据
function generateChartData(days: number, type: 'signals' | 'activity' | 'price' | 'volume'): ChartData[] {
  const data: ChartData[] = []
  const today = new Date()

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)

    const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`

    const baseValue = type === 'price' ? 100 : type === 'volume' ? 1000000 : 50
    const variation = type === 'price' ? 5 : type === 'volume' ? 500000 : 20

    data.push({
      date: dateStr,
      signals: type === 'signals' ? Math.floor(baseValue + Math.random() * variation - variation / 2) : 0,
      activity: type === 'activity' ? Math.floor(50 + Math.random() * 50) : 0,
      price: type === 'price' ? parseFloat((baseValue + Math.random() * variation - variation / 2).toFixed(2)) : 0,
      volume: type === 'volume' ? Math.floor(baseValue + Math.random() * variation - variation / 2) : 0
    })
  }

  return data
}

// 数据加载函数
async function loadData() {
  isLoading.all = true
  error.data = ''

  try {
    // 并行获取所有数据
    const [metricsData, signalsData, projectsData] = await Promise.all([
      localDbService.getDashboardMetrics(),
      localDbService.getRecentSignals(5),
      localDbService.getHotProjects(10)
    ])

    // 更新数据状态
    metrics.value = metricsData
    recentSignals.value = signalsData
    hotProjects.value = projectsData

    // 初始化图表数据
    signalTrendData.value = generateChartData(7, 'signals')
    projectActivityData.value = generateChartData(7, 'activity')
    priceTrendData.value = generateChartData(7, 'price')
    volumeTrendData.value = generateChartData(7, 'volume')

    // 标记数据已加载
    isDataLoaded.value = true

    // 延迟初始化图表，确保DOM元素已经渲染完成
    setTimeout(() => {
      initSignalTrendChart()
      initProjectActivityChart()
      initPriceTrendChart()
      initVolumeTrendChart()
    }, 100)
  } catch (err) {
    error.data = '获取数据失败'
    console.error('Error loading data:', err)
  } finally {
    isLoading.all = false
  }
}



// 初始化信号趋势图表
function initSignalTrendChart() {
  if (!signalTrendChart.value) return

  // 清除现有内容
  d3.select(signalTrendChart.value).selectAll('*').remove()

  // 使用数据
  const data = signalTrendData.value

  // 设置尺寸
  const width = signalTrendChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(signalTrendChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, innerWidth])
    .padding(0.1)

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.signals) || 100])
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
    .attr('y', d => y(d.signals))
    .attr('width', x.bandwidth())
    .attr('height', d => innerHeight - y(d.signals))
    .attr('fill', '#93beb4')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('每日信号数')
}

// 初始化项目活跃度图表
function initProjectActivityChart() {
  if (!projectActivityChart.value) return

  // 清除现有内容
  d3.select(projectActivityChart.value).selectAll('*').remove()

  // 使用数据
  const data = projectActivityData.value

  // 设置尺寸
  const width = projectActivityChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(projectActivityChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, innerWidth])
    .padding(0.1)

  const y = d3.scaleLinear()
    .domain([0, 100])
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
    .y(d => y(d.activity))
    .curve(d3.curveMonotoneX)

  svg.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', '#453b31')
    .attr('stroke-width', 2)
    .attr('d', line)

  // 添加数据点
  svg.selectAll('.dot')
    .data(data)
    .enter()
    .append('circle')
    .attr('class', 'dot')
    .attr('cx', d => x(d.date) || 0)
    .attr('cy', d => y(d.activity))
    .attr('r', 4)
    .attr('fill', '#453b31')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('项目活跃度')
}

// 初始化价格趋势图表
function initPriceTrendChart() {
  if (!priceTrendChart.value) return

  // 清除现有内容
  d3.select(priceTrendChart.value).selectAll('*').remove()

  // 使用数据
  const data = priceTrendData.value

  // 设置尺寸
  const width = priceTrendChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(priceTrendChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, innerWidth])
    .padding(0.1)

  const y = d3.scaleLinear()
    .domain([
      d3.min(data, d => d.price) || 0,
      d3.max(data, d => d.price) || 100
    ])
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
    .attr('stroke', '#f83a22')
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
    .attr('r', 4)
    .attr('fill', '#f83a22')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('价格趋势')
}

// 初始化交易量趋势图表
function initVolumeTrendChart() {
  if (!volumeTrendChart.value) return

  // 清除现有内容
  d3.select(volumeTrendChart.value).selectAll('*').remove()

  // 使用数据
  const data = volumeTrendData.value

  // 设置尺寸
  const width = volumeTrendChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(volumeTrendChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, innerWidth])
    .padding(0.1)

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.volume) || 1000000])
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
    .attr('width', x.bandwidth())
    .attr('height', d => innerHeight - y(d.volume))
    .attr('fill', '#b2937f')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('交易量趋势')
}

// 挂载时的处理
onMounted(() => {
  // 初始化时直接加载数据
  loadData()

  // 窗口大小变化时重新初始化图表
  window.addEventListener('resize', () => {
    if (isDataLoaded.value) {
      initSignalTrendChart()
      initProjectActivityChart()
      initPriceTrendChart()
      initVolumeTrendChart()
    }
  })
})
</script>

<style scoped>
/* 组件特定样式 */
</style>

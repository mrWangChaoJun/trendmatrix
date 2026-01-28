<template>
  <div class="container mx-auto px-4 py-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-1">项目活跃度、NFT 市场和 DeFi 协议分析</p>
    </div>

    <!-- Solana 生态概览 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <!-- 总项目数 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总项目数</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">1,847</h3>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                </svg>
                15.3% 较上月
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- NFT 交易量 -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">NFT 交易量</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">$124.5M</h3>
              <p class="text-xs text-red-600 dark:text-red-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
                8.2% 较上周
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- DeFi TVL -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">DeFi TVL</p>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">$4.2B</h3>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                </svg>
                12.8% 较上月
              </p>
            </div>
            <div class="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 生态分类分布 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 项目分类分布 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">项目分类分布</h3>
        </div>
        <div ref="categoryDistributionChart" class="h-64"></div>
      </div>

      <!-- 活跃度趋势 -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">生态活跃度趋势</h3>
        </div>
        <div ref="activityTrendChart" class="h-64"></div>
      </div>
    </div>

    <!-- 热门项目列表 -->
    <div class="card mb-6">
      <div class="card-header flex items-center justify-between">
        <h3 class="font-medium text-gray-900 dark:text-white">热门项目</h3>
        <div class="flex items-center space-x-2">
          <select class="text-sm border border-gray-300 dark:border-gray-600 rounded px-2 py-1 dark:bg-gray-800 dark:text-white">
            <option>活跃度</option>
            <option>交易量</option>
            <option>TVL</option>
            <option>增长率</option>
          </select>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-800">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">项目</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">分类</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">活跃度</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">交易量</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">TVL</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
            <tr v-for="project in topProjects" :key="project.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3">
                    <span class="text-xs font-medium text-gray-900 dark:text-white">{{ project.name.charAt(0) }}</span>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ project.name }}</div>
                    <div class="text-xs text-gray-500 dark:text-gray-400">{{ project.symbol }}</div>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200">
                  {{ project.category }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div class="h-2 rounded-full bg-blue-500" :style="{ width: project.activity + '%' }"></div>
                  </div>
                  <span class="ml-2 text-xs text-gray-600 dark:text-gray-400">{{ project.activity }}%</span>
                </div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                ${{ project.volume.toLocaleString() }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                ${{ project.tvl.toLocaleString() }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
                <router-link :to="`/solana/project/${project.id}`" class="text-blue-600 dark:text-blue-400 hover:underline">详情</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- NFT 和 DeFi 概览 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- NFT 市场概览 -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h3 class="font-medium text-gray-900 dark:text-white">NFT 市场概览</h3>
        </div>
        <div class="p-4">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总交易量</p>
              <h4 class="text-xl font-bold text-gray-900 dark:text-white mt-1">$124.5M</h4>
              <p class="text-xs text-red-600 dark:text-red-400 mt-1">-8.2% 较上周</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">活跃收藏</p>
              <h4 class="text-xl font-bold text-gray-900 dark:text-white mt-1">2,456</h4>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1">+3.5% 较上周</p>
            </div>
          </div>
          <div class="space-y-3">
            <div v-for="collection in topNftCollections" :key="collection.id" class="flex items-center justify-between py-2 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3">
                  <span class="text-xs font-medium text-gray-900 dark:text-white">{{ collection.name.charAt(0) }}</span>
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-900 dark:text-white">{{ collection.name }}</h5>
                  <p class="text-xs text-gray-600 dark:text-gray-400">{{ collection.items }} 项</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900 dark:text-white">${{ collection.floorPrice.toFixed(2) }}</p>
                <p class="text-xs text-green-600 dark:text-green-400">{{ collection.change }}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- DeFi 协议概览 -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h3 class="font-medium text-gray-900 dark:text-white">DeFi 协议概览</h3>
        </div>
        <div class="p-4">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总 TVL</p>
              <h4 class="text-xl font-bold text-gray-900 dark:text-white mt-1">$4.2B</h4>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1">+12.8% 较上月</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">活跃协议</p>
              <h4 class="text-xl font-bold text-gray-900 dark:text-white mt-1">156</h4>
              <p class="text-xs text-green-600 dark:text-green-400 mt-1">+5.4% 较上月</p>
            </div>
          </div>
          <div class="space-y-3">
            <div v-for="protocol in topDefiProtocols" :key="protocol.id" class="flex items-center justify-between py-2 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3">
                  <span class="text-xs font-medium text-gray-900 dark:text-white">{{ protocol.name.charAt(0) }}</span>
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-900 dark:text-white">{{ protocol.name }}</h5>
                  <p class="text-xs text-gray-600 dark:text-gray-400">{{ protocol.category }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900 dark:text-white">${{ (protocol.tvl / 1000000).toFixed(1) }}M</p>
                <p class="text-xs text-green-600 dark:text-green-400">{{ protocol.apr }}% APY</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as d3 from 'd3'

// 图表引用
const categoryDistributionChart = ref<HTMLElement | null>(null)
const activityTrendChart = ref<HTMLElement | null>(null)

// 模拟数据
const topProjects = [
  { id: 1, name: 'Solana', symbol: 'SOL', category: 'Layer 1', activity: 95, volume: 1250000000, tvl: 4200000000 },
  { id: 2, name: 'Serum', symbol: 'SRM', category: 'DeFi', activity: 88, volume: 450000000, tvl: 850000000 },
  { id: 3, name: 'Metaplex', symbol: 'MPLX', category: 'NFT', activity: 82, volume: 280000000, tvl: 420000000 },
  { id: 4, name: 'Raydium', symbol: 'RAY', category: 'DeFi', activity: 79, volume: 320000000, tvl: 680000000 },
  { id: 5, name: 'Star Atlas', symbol: 'ATLAS', category: 'GameFi', activity: 75, volume: 180000000, tvl: 250000000 },
  { id: 6, name: 'Marinade Finance', symbol: 'MNDE', category: 'DeFi', activity: 72, volume: 150000000, tvl: 520000000 },
  { id: 7, name: 'Solanart', symbol: 'SART', category: 'NFT', activity: 68, volume: 120000000, tvl: 180000000 },
  { id: 8, name: 'STEPN', symbol: 'GMT', category: 'GameFi', activity: 65, volume: 95000000, tvl: 150000000 }
]

const topNftCollections = [
  { id: 1, name: 'Solana Monkey Business', items: 5000, floorPrice: 45.5, change: +2.5 },
  { id: 2, name: 'Degenerate Ape Academy', items: 10000, floorPrice: 28.7, change: -1.2 },
  { id: 3, name: 'Star Atlas NFTs', items: 25000, floorPrice: 12.3, change: +4.8 },
  { id: 4, name: 'Okay Bears', items: 10000, floorPrice: 32.1, change: +1.7 },
  { id: 5, name: 'Galactic Geckos', items: 7500, floorPrice: 8.9, change: -0.5 }
]

const topDefiProtocols = [
  { id: 1, name: 'Raydium', category: 'AMM', tvl: 680000000, apr: 8.5 },
  { id: 2, name: 'Marinade Finance', category: 'Staking', tvl: 520000000, apr: 6.2 },
  { id: 3, name: 'Serum', category: 'DEX', tvl: 450000000, apr: 4.8 },
  { id: 4, name: 'Orca', category: 'AMM', tvl: 320000000, apr: 7.3 },
  { id: 5, name: 'Kamino Finance', category: 'Lending', tvl: 280000000, apr: 9.1 }
]

// 初始化项目分类分布图表
function initCategoryDistributionChart() {
  if (!categoryDistributionChart.value) return

  // 模拟数据
  const data = [
    { category: 'DeFi', count: 587 },
    { category: 'NFT', count: 423 },
    { category: 'GameFi', count: 312 },
    { category: 'Social', count: 215 },
    { category: 'Infrastructure', count: 189 },
    { category: 'Other', count: 121 }
  ]

  // 清除现有内容
  d3.select(categoryDistributionChart.value).selectAll('*').remove()

  // 设置尺寸
  const width = categoryDistributionChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(categoryDistributionChart.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // 创建比例尺
  const x = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1)

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count) || 600])
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
    .attr('x', d => x(d.category) || 0)
    .attr('y', d => y(d.count))
    .attr('width', x.bandwidth())
    .attr('height', d => innerHeight - y(d.count))
    .attr('fill', '#6366f1')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('项目分类分布')
}

// 初始化活跃度趋势图表
function initActivityTrendChart() {
  if (!activityTrendChart.value) return

  // 模拟数据
  const data = [
    { date: '1月', activity: 65 },
    { date: '2月', activity: 68 },
    { date: '3月', activity: 72 },
    { date: '4月', activity: 78 },
    { date: '5月', activity: 82 },
    { date: '6月', activity: 79 },
    { date: '7月', activity: 85 },
    { date: '8月', activity: 88 },
    { date: '9月', activity: 92 },
    { date: '10月', activity: 89 },
    { date: '11月', activity: 94 },
    { date: '12月', activity: 95 }
  ]

  // 清除现有内容
  d3.select(activityTrendChart.value).selectAll('*').remove()

  // 设置尺寸
  const width = activityTrendChart.value.clientWidth
  const height = 250
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  // 创建SVG
  const svg = d3.select(activityTrendChart.value)
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
    .domain([60, 100])
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
    .attr('cy', d => y(d.activity))
    .attr('r', 4)
    .attr('fill', '#3b82f6')

  // 添加标题
  svg.append('text')
    .attr('x', innerWidth / 2)
    .attr('y', -5)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .text('生态活跃度趋势')
}

// 挂载时初始化图表
onMounted(() => {
  initCategoryDistributionChart()
  initActivityTrendChart()

  // 窗口大小变化时重新初始化图表
  window.addEventListener('resize', () => {
    initCategoryDistributionChart()
    initActivityTrendChart()
  })
})
</script>

<style scoped>
/* 组件特定样式 */
</style>

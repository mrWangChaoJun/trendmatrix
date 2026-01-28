<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-primary dark:text-white">TrendMatrix</h1>
    <p class="text-gray-600 dark:text-gray-400 mt-1">Solana NFT 市场趋势分析</p>

    <!-- 数据内容 -->
    <div>
      <!-- 市场概览指标 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">总集合数</h3>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ marketMetrics.total_collections }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">24h 总交易量</h3>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ marketMetrics.total_volume_24h.toLocaleString() }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">平均地板价</h3>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ marketMetrics.average_floor_price }} SOL</p>
        </div>
      </div>



      <!-- 图表区域 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        <!-- 交易量趋势 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">交易量趋势</h3>
          <div class="h-64 mt-4" ref="volumeChartRef"></div>
        </div>

        <!-- 地板价趋势 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">地板价趋势</h3>
          <div class="h-64 mt-4" ref="floorPriceChartRef"></div>
        </div>
      </div>

      <!-- 筛选和搜索 -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mt-6 gap-4">
        <div class="relative">
          <input
            type="text"
            v-model="searchTerm"
            placeholder="搜索集合..."
            class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          >
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
        <div class="relative">
          <select
            v-model="selectedCategory"
            class="pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          >
            <option value="">所有类别</option>
            <option value="Avatar">头像</option>
            <option value="GameFi">GameFi</option>
            <option value="Art">艺术</option>
            <option value="Metaverse">元宇宙</option>
          </select>
          <svg class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
      </div>

      <!-- NFT 集合表格 -->
      <div class="mt-6 overflow-x-auto">
        <table class="min-w-full bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
          <thead class="bg-gray-100 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">集合名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">类别</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">地板价</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">24h 交易量</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">7d 交易量</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">24h 变化</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">持有者数</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">链接</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="collection in filteredCollections" :key="collection.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ collection.name }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 rounded-full">{{ collection.category }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ collection.floor_price }} SOL</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">${{ collection.volume_24h.toLocaleString() }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">${{ collection.volume_7d.toLocaleString() }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="collection.change_24h >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                  {{ collection.change_24h >= 0 ? '+' : '' }}{{ collection.change_24h }}%
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ collection.holders.toLocaleString() }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex space-x-2">
                  <a :href="collection.url" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.39-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 14.97 6.118 13.546 6.03 12H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd"></path>
                    </svg>
                  </a>
                  <a :href="collection.twitter" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-blue-500">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
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
import { ref, computed, onMounted, watch } from 'vue';
import * as d3 from 'd3';
import { localDbService, NftMarketMetrics, NftTrendData } from '@/services/db/local-db.service';

// 响应式数据
const marketMetrics = ref<NftMarketMetrics>({
  total_collections: 0,
  total_volume_24h: 0,
  average_floor_price: 0,
  top_collections: []
});
const searchTerm = ref('');
const selectedCategory = ref('');
const isLoading = ref(false);
const trendData = ref<NftTrendData[]>([]);

// 图表引用
const volumeChartRef = ref<HTMLElement | null>(null);
const floorPriceChartRef = ref<HTMLElement | null>(null);

// 计算属性
const filteredCollections = computed(() => {
  return marketMetrics.value.top_collections.filter(collection => {
    const matchesSearch = collection.name.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesCategory = !selectedCategory.value || collection.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

// 加载数据方法
const loadData = async () => {
  isLoading.value = true;
  try {
    // 加载市场指标
    marketMetrics.value = await localDbService.getNftMarketMetrics();
    // 加载趋势数据
    await loadTrendData();
  } catch (error) {
    console.error('Error loading NFT data:', error);
  } finally {
    isLoading.value = false;
  }
};

// 加载趋势数据
const loadTrendData = async () => {
  try {
    console.log('Loading trend data for 7 days');
    trendData.value = await localDbService.getNftTrendData(7);
    console.log('Loaded trend data:', trendData.value.length, 'days');
  } catch (error) {
    console.error('Error loading NFT trend data:', error);
  }
};

// 初始化交易量图表
const initVolumeChart = () => {
  if (!volumeChartRef.value || trendData.value.length === 0) return;

  const container = volumeChartRef.value;
  d3.select(container).selectAll('*').remove();

  const width = container.clientWidth;
  const height = 250;
  const margin = { top: 20, right: 20, bottom: 40, left: 40 };

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const x = d3.scaleBand()
    .domain(trendData.value.map(d => d.date))
    .range([margin.left, width - margin.right])
    .padding(0.2);

  const y = d3.scaleLinear()
    .domain([0, d3.max(trendData.value, d => d.volume) || 1])
    .range([height - margin.bottom, margin.top]);

  // X轴
  svg.append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'rotate(-45)')
    .attr('text-anchor', 'end')
    .attr('font-size', trendData.value.length > 14 ? '8px' : '10px');

  // 调整X轴刻度显示密度
  if (trendData.value.length > 30) {
    d3.select(container).selectAll('g.tick').each(function(_, i) {
      if (i % 3 !== 0) d3.select(this).remove();
    });
  } else if (trendData.value.length > 14) {
    d3.select(container).selectAll('g.tick').each(function(_, i) {
      if (i % 2 !== 0) d3.select(this).remove();
    });
  }

  // Y轴
  svg.append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickFormat(d => `$${((d as number) / 1000000).toFixed(0)}M`));

  // 柱状图
  svg.selectAll('.bar')
    .data(trendData.value)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.date) || 0)
    .attr('y', d => y(d.volume))
    .attr('width', x.bandwidth())
    .attr('height', d => height - margin.bottom - y(d.volume))
    .attr('fill', '#3b82f6');
};

// 初始化地板价图表
const initFloorPriceChart = () => {
  if (!floorPriceChartRef.value || trendData.value.length === 0) return;

  const container = floorPriceChartRef.value;
  d3.select(container).selectAll('*').remove();

  const width = container.clientWidth;
  const height = 250;
  const margin = { top: 20, right: 20, bottom: 40, left: 40 };

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const x = d3.scaleBand()
    .domain(trendData.value.map(d => d.date))
    .range([margin.left, width - margin.right])
    .padding(0.2);

  const y = d3.scaleLinear()
    .domain([0, d3.max(trendData.value, d => d.floor_price) || 1])
    .range([height - margin.bottom, margin.top]);

  // X轴
  svg.append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'rotate(-45)')
    .attr('text-anchor', 'end')
    .attr('font-size', trendData.value.length > 14 ? '8px' : '10px');

  // 调整X轴刻度显示密度
  if (trendData.value.length > 30) {
    d3.select(container).selectAll('g.tick').each(function(_, i) {
      if (i % 3 !== 0) d3.select(this).remove();
    });
  } else if (trendData.value.length > 14) {
    d3.select(container).selectAll('g.tick').each(function(_, i) {
      if (i % 2 !== 0) d3.select(this).remove();
    });
  }

  // Y轴
  svg.append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickFormat(d => `${((d as number)).toFixed(2)} SOL`));

  // 折线图
  const line = d3.line<NftTrendData>()
    .x(d => x(d.date) || 0)
    .y(d => y(d.floor_price));

  svg.append('path')
    .datum(trendData.value)
    .attr('fill', 'none')
    .attr('stroke', '#10b981')
    .attr('stroke-width', 2)
    .attr('d', line);

  // 数据点
  svg.selectAll('.dot')
    .data(trendData.value)
    .enter()
    .append('circle')
    .attr('class', 'dot')
    .attr('cx', d => x(d.date) || 0)
    .attr('cy', d => y(d.floor_price))
    .attr('r', 4)
    .attr('fill', '#10b981');
};

// 监听趋势数据变化，更新图表
watch(trendData, () => {
  setTimeout(() => {
    initVolumeChart();
    initFloorPriceChart();
  }, 100);
}, { deep: true });

// 监听窗口大小变化，重绘图表
const handleResize = () => {
  initVolumeChart();
  initFloorPriceChart();
};

// 生命周期钩子
onMounted(() => {
  // 初始化时直接加载数据
  loadData();
  window.addEventListener('resize', handleResize);
});
</script>

<style scoped>
/* 组件特定样式 */
</style>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <i class="fas fa-cloud-sun text-2xl text-blue-500"></i>
            <h1 class="text-xl font-semibold text-gray-800">银川特色作物气象灾害预警系统</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">2023年11月15日 星期三</span>
            <button class="!rounded-button whitespace-nowrap bg-blue-500 px-4 py-2 text-sm text-white">
              <i class="fas fa-bell mr-2"></i>预警通知
            </button>
          </div>
        </div>
      </div>
    </header>
    <!-- 气象数据展示区 -->
    <section class="container mx-auto px-6 py-8">
      <div class="rounded-xl bg-white p-6 shadow-md">
        <h2 class="mb-6 text-xl font-semibold text-gray-800">实时气象数据</h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <!-- 实时数据 -->
          <div class="rounded-lg border border-gray-200 p-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-medium text-gray-700">当前气象状况</h3>
                <p class="text-sm text-gray-500">银川市兴庆区 - 更新于10分钟前</p>
              </div>
              <i class="fas fa-sync-alt cursor-pointer text-blue-500"></i>
            </div>
            <div class="mt-6 grid grid-cols-2 gap-4">
              <div class="text-center">
                <div class="text-5xl font-bold text-blue-600">12°C</div>
                <p class="text-sm text-gray-500">当前温度</p>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-blue-600">65%</div>
                <p class="text-sm text-gray-500">湿度</p>
              </div>
              <div class="text-center">
                <div class="flex items-center justify-center">
                  <i class="fas fa-wind mr-2 text-blue-600"></i>
                  <span class="text-xl font-bold">3级</span>
                </div>
                <p class="text-sm text-gray-500">西北风</p>
              </div>
              <div class="text-center">
                <div class="text-xl font-bold text-blue-600">1012 hPa</div>
                <p class="text-sm text-gray-500">气压</p>
              </div>
            </div>
          </div>
          <!-- 宁夏作物分布地图 -->
          <div class="rounded-lg border border-gray-200 p-6">
            <h3 class="mb-4 text-lg font-medium text-gray-700">宁夏作物分布与风险地图</h3>
            <div class="h-48">
              <div ref="ningxiaMap" class="h-full w-full"></div>
            </div>
          </div>
        </div>
        <!-- 详细气象预测 -->
        <div class="mt-8">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-700">详细气象预测</h3>
            <select
                v-model="selectedForecastDay"
                class="!rounded-button whitespace-nowrap border border-gray-300 bg-white px-3 py-2 text-sm"
            >
              <option v-for="(day, index) in weatherForecast" :key="index" :value="index">
                {{ day.date }} {{ day.weather }}
              </option>
            </select>
          </div>
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <!-- 预测数据详情 -->
            <div class="rounded-lg border border-gray-200 p-6">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-medium text-gray-700">{{ weatherForecast[selectedForecastDay].date }}
                    气象预测</h3>
                  <p class="text-sm text-gray-500">更新时间: {{ currentTime }}</p>
                </div>
              </div>
              <div class="mt-6 grid grid-cols-2 gap-4">
                <div class="text-center">
                  <div class="text-5xl font-bold text-blue-600">{{
                      weatherForecast[selectedForecastDay].avgTemp
                    }}°C
                  </div>
                  <p class="text-sm text-gray-500">平均温度</p>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-blue-600">{{
                      weatherForecast[selectedForecastDay].humidity
                    }}%
                  </div>
                  <p class="text-sm text-gray-500">湿度</p>
                </div>
                <div class="text-center">
                  <div class="flex items-center justify-center">
                    <i class="fas fa-wind mr-2 text-blue-600"></i>
                    <span class="text-xl font-bold">{{ weatherForecast[selectedForecastDay].windLevel }}级</span>
                  </div>
                  <p class="text-sm text-gray-500">{{ weatherForecast[selectedForecastDay].windDirection }}风</p>
                </div>
                <div class="text-center">
                  <div class="text-xl font-bold text-blue-600">{{ weatherForecast[selectedForecastDay].pressure }} hPa
                  </div>
                  <p class="text-sm text-gray-500">气压</p>
                </div>
              </div>
            </div>
            <!-- 预测地图 -->
            <div class="rounded-lg border border-gray-200 p-6">
              <h3 class="mb-4 text-lg font-medium text-gray-700">宁夏气象风险预测</h3>
              <div class="h-48">
                <div ref="forecastMap" class="h-full w-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- 风险分析区 -->
    <section class="container mx-auto px-6 py-8">
      <div class="rounded-xl bg-white p-6 shadow-md">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-xl font-semibold text-gray-800">气象灾害风险分析</h2>
          <div class="flex rounded-md bg-gray-100 p-1">
            <button
                v-for="tab in riskTabs"
                :key="tab.id"
                @click="activeRiskTab = tab.id"
                :class="`!rounded-button whitespace-nowrap px-4 py-2 text-sm ${activeRiskTab === tab.id ? 'bg-blue-500 text-white' : 'text-gray-700'}`"
            >
              {{ tab.label }}
            </button>
          </div>
        </div>
        <!-- 作物风险卡片 -->
        <div class="space-y-4">
          <div
              v-for="crop in sortedCrops"
              :key="crop.id"
              class="rounded-lg border border-gray-200 p-6"
              :class="{
'border-red-300 bg-red-50': crop.riskLevel === 'high',
'border-yellow-300 bg-yellow-50': crop.riskLevel === 'medium',
'border-green-300 bg-green-50': crop.riskLevel === 'low'
}"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-center">
                <div class="mr-4 flex h-12 w-12 items-center justify-center rounded-full bg-white shadow-sm">
                  <i :class="`fas ${crop.icon} text-xl ${crop.riskLevel === 'high' ? 'text-red-500' : crop.riskLevel === 'medium' ? 'text-yellow-500' : 'text-green-500'}`"></i>
                </div>
                <div>
                  <h3 class="text-lg font-medium">{{ crop.name }}</h3>
                  <div class="flex items-center">
<span
    class="mr-2 rounded-full px-2 py-1 text-xs font-medium text-white"
    :class="{
'bg-red-500': crop.riskLevel === 'high',
'bg-yellow-500': crop.riskLevel === 'medium',
'bg-green-500': crop.riskLevel === 'low'
}"
>
{{ crop.riskLevel === 'high' ? '高风险' : crop.riskLevel === 'medium' ? '中风险' : '低风险' }}
</span>
                    <span class="text-sm text-gray-500">{{
                        activeRiskTab === 'current' ? '当前风险' : '预测风险'
                      }}</span>
                  </div>
                </div>
              </div>
              <button
                  @click="toggleCropDetail(crop.id)"
                  class="!rounded-button whitespace-nowrap bg-white px-3 py-1 text-sm shadow-sm"
              >
                <i :class="`fas ${showCropDetails[crop.id] ? 'fa-chevron-up' : 'fa-chevron-down'} mr-1`"></i>
                {{ showCropDetails[crop.id] ? '收起' : '详情' }}
              </button>
            </div>
            <!-- 详细分析 -->
            <div v-if="showCropDetails[crop.id]" class="mt-4">
              <div class="mb-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                <div class="rounded-lg bg-white p-4 shadow-sm">
                  <h4 class="mb-2 text-sm font-medium text-gray-700">主要威胁因素</h4>
                  <ul class="space-y-1 text-sm text-gray-600">
                    <li v-for="(factor, index) in crop.threats" :key="index" class="flex items-start">
                      <i class="fas fa-exclamation-circle mr-2 mt-0.5 text-red-400"></i>
                      <span>{{ factor }}</span>
                    </li>
                  </ul>
                </div>
                <div class="rounded-lg bg-white p-4 shadow-sm">
                  <h4 class="mb-2 text-sm font-medium text-gray-700">影响程度</h4>
                  <div class="h-32">
                    <div :ref="`impactChart-${crop.id}`" class="h-full w-full"></div>
                  </div>
                </div>
                <div class="rounded-lg bg-white p-4 shadow-sm">
                  <h4 class="mb-2 text-sm font-medium text-gray-700">风险分析</h4>
                  <p class="text-sm text-gray-600">{{ crop.analysis }}</p>
                </div>
              </div>
              <!-- 风险地图 -->
              <div class="mb-4 rounded-lg bg-white p-4 shadow-sm">
                <h4 class="mb-4 text-sm font-medium text-gray-700">区域风险分布</h4>
                <div class="h-64">
                  <div :ref="`riskMap-${crop.id}`" class="h-full w-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- 防护措施区 -->
    <section class="container mx-auto px-6 py-8">
      <div class="rounded-xl bg-white p-6 shadow-md">
        <h2 class="mb-6 text-xl font-semibold text-gray-800">防护措施建议</h2>
        <div class="space-y-4">
          <div
              v-for="crop in crops"
              :key="`measure-${crop.id}`"
              class="rounded-lg border border-gray-200 p-6"
          >
            <div class="flex items-center">
              <i :class="`fas ${crop.icon} mr-4 text-2xl ${crop.riskLevel === 'high' ? 'text-red-500' : crop.riskLevel === 'medium' ? 'text-yellow-500' : 'text-green-500'}`"></i>
              <h3 class="text-lg font-medium">{{ crop.name }}防护措施</h3>
            </div>
            <div class="mt-4">
              <div
                  v-for="(measure, index) in crop.measures"
                  :key="index"
                  class="mb-3 flex items-start rounded-lg bg-gray-50 p-4"
                  :class="{
'border-l-4 border-red-500': measure.level === 'urgent',
'border-l-4 border-yellow-500': measure.level === 'important',
'border-l-4 border-green-500': measure.level === 'normal'
}"
              >
                <i
                    :class="`fas ${measure.icon} mr-3 mt-1 ${measure.level === 'urgent' ? 'text-red-500' : measure.level === 'important' ? 'text-yellow-500' : 'text-green-500'}`"
                ></i>
                <div>
                  <h4 class="font-medium text-gray-800">{{ measure.title }}</h4>
                  <p class="mt-1 text-sm text-gray-600">{{ measure.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- 底部 -->
    <footer class="bg-gray-800 py-8 text-white">
      <div class="container mx-auto px-6">
        <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div>
            <h3 class="mb-4 text-lg font-semibold">银川特色作物气象灾害预警系统</h3>
            <p class="text-sm text-gray-300">为银川地区特色作物提供精准的气象灾害预警和防护建议，助力农业安全生产。</p>
          </div>
          <div>
            <h3 class="mb-4 text-lg font-semibold">联系方式</h3>
            <ul class="space-y-2 text-sm text-gray-300">
              <li class="flex items-center">
                <i class="fas fa-phone-alt mr-2"></i>
                <span>0951-1234567</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-envelope mr-2"></i>
                <span>service@ycmaws.com</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-map-marker-alt mr-2"></i>
                <span>宁夏银川市金凤区气象局</span>
              </li>
            </ul>
          </div>
          <div>
            <h3 class="mb-4 text-lg font-semibold">相关链接</h3>
            <ul class="space-y-2 text-sm text-gray-300">
              <li><a href="#" class="hover:text-white">宁夏气象局</a></li>
              <li><a href="#" class="hover:text-white">银川农业农村局</a></li>
              <li><a href="#" class="hover:text-white">中国气象数据网</a></li>
            </ul>
          </div>
        </div>
        <div class="mt-8 border-t border-gray-700 pt-6 text-center text-sm text-gray-400">
          <p>© 2023 银川特色作物气象灾害预警系统 版权所有</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import ningxia from '@/assets/map/js/province/ningxia';

export default {
  data() {
    return {
      weatherForecast: [
        {
          date: '11/16',
          icon: 'fa-sun',
          weather: '晴',
          maxTemp: 15,
          minTemp: 4,
          avgTemp: 9,
          tempDiff: 3,
          humidity: 45,
          windLevel: 3,
          windDirection: '西北',
          pressure: 1012,
          hoursTemp: [4, 3, 2, 3, 5, 7, 9, 12, 14, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 4, 4, 4]
        },
        {
          date: '11/17',
          icon: 'fa-cloud-sun',
          weather: '多云',
          maxTemp: 13,
          minTemp: 3,
          avgTemp: 8,
          tempDiff: -2,
          humidity: 55,
          windLevel: 4,
          windDirection: '北',
          pressure: 1015,
          hoursTemp: [3, 3, 3, 4, 5, 6, 7, 9, 11, 12, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 4, 3, 3, 3]
        },
        {
          date: '11/18',
          icon: 'fa-cloud-rain',
          weather: '小雨',
          maxTemp: 10,
          minTemp: 2,
          avgTemp: 6,
          tempDiff: -3,
          humidity: 75,
          windLevel: 3,
          windDirection: '东北',
          pressure: 1018,
          hoursTemp: [2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 3, 3, 2, 2, 2, 2]
        },
        {
          date: '11/19',
          icon: 'fa-cloud',
          weather: '阴',
          maxTemp: 8,
          minTemp: 1,
          avgTemp: 5,
          tempDiff: -2,
          humidity: 65,
          windLevel: 2,
          windDirection: '东',
          pressure: 1020,
          hoursTemp: [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1]
        },
        {
          date: '11/20',
          icon: 'fa-sun',
          weather: '晴',
          maxTemp: 12,
          minTemp: 0,
          avgTemp: 6,
          tempDiff: 4,
          humidity: 50,
          windLevel: 3,
          windDirection: '西北',
          pressure: 1015,
          hoursTemp: [0, -1, -1, 0, 2, 4, 6, 8, 10, 11, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0]
        },
        {
          date: '11/21',
          icon: 'fa-cloud-sun',
          weather: '多云',
          maxTemp: 11,
          minTemp: -1,
          avgTemp: 5,
          tempDiff: -1,
          humidity: 55,
          windLevel: 4,
          windDirection: '北',
          pressure: 1018,
          hoursTemp: [-1, -2, -2, -1, 1, 3, 5, 7, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -1]
        },
        {
          date: '11/22',
          icon: 'fa-snowflake',
          weather: '小雪',
          maxTemp: 5,
          minTemp: -3,
          avgTemp: 1,
          tempDiff: -6,
          humidity: 70,
          windLevel: 3,
          windDirection: '西北',
          pressure: 1022,
          hoursTemp: [-3, -3, -3, -2, -1, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, -1, -2, -2, -2, -3, -3, -3, -3]
        }
      ],
      selectedForecastDay: 0,
      currentTime: new Date().toLocaleString(),
      ningxiaMap: null,
      forecastChart: null,
      riskTabs: [
        {id: 'current', label: '实时风险'},
        {id: 'forecast', label: '预测风险'}
      ],
      activeRiskTab: 'current',
      crops: [
        {
          id: 'grape',
          name: '葡萄',
          icon: 'fa-wine-bottle',
          riskLevel: 'high',
          threats: ['霜冻风险', '低温冷害', '大风影响'],
          analysis: '当前气温骤降，预计未来24小时最低温度将降至0°C以下，对葡萄藤造成严重霜冻危害，特别是新梢和幼果部分。',
          timeRange: '24h',
          chartType: 'line',
          measures: [
            {
              level: 'urgent',
              icon: 'fa-fire',
              title: '紧急防霜措施',
              description: '立即在葡萄园内点燃防霜堆，每公顷布置30-40个，提高园内温度2-3°C。'
            },
            {
              level: 'important',
              icon: 'fa-tint-slash',
              title: '停止灌溉',
              description: '暂停所有灌溉活动，避免土壤湿度过大加剧低温危害。'
            },
            {
              level: 'important',
              icon: 'fa-umbrella',
              title: '覆盖保护',
              description: '使用防寒布或草帘覆盖葡萄藤，特别是幼嫩部分，防止直接受冻。'
            },
            {
              level: 'normal',
              icon: 'fa-clipboard-check',
              title: '灾后检查',
              description: '霜冻过后及时检查植株受损情况，剪除受冻枝条，喷施营养液促进恢复。'
            }
          ]
        },
        {
          id: 'wheat',
          name: '小麦',
          icon: 'fa-bread-slice',
          riskLevel: 'medium',
          threats: ['干旱风险', '低温影响'],
          analysis: '近期降水偏少，土壤墒情下降，加上低温影响，可能导致小麦生长缓慢，分蘖减少。',
          timeRange: '7d',
          chartType: 'bar',
          measures: [
            {
              level: 'important',
              icon: 'fa-tint',
              title: '适时灌溉',
              description: '选择晴天中午进行小水灌溉，每亩用水量控制在30-40立方米。'
            },
            {
              level: 'important',
              icon: 'fa-spray-can',
              title: '叶面施肥',
              description: '喷施0.3%磷酸二氢钾+1%尿素溶液，增强植株抗寒能力。'
            },
            {
              level: 'normal',
              icon: 'fa-seedling',
              title: '中耕保墒',
              description: '雨后及时中耕松土，切断土壤毛细管，减少水分蒸发。'
            }
          ]
        },
        {
          id: 'lycium',
          name: '枸杞',
          icon: 'fa-apple-alt',
          riskLevel: 'low',
          threats: ['大风影响'],
          analysis: '当前主要风险为大风可能导致落花落果，但对整体产量影响较小。',
          timeRange: '24h',
          chartType: 'line',
          measures: [
            {
              level: 'important',
              icon: 'fa-wind',
              title: '防风措施',
              description: '检查并加固防风林，破损处及时修补，降低风速30%以上。'
            },
            {
              level: 'normal',
              icon: 'fa-clipboard-list',
              title: '花果监测',
              description: '大风过后检查花果脱落情况，评估损失程度。'
            }
          ]
        }
      ],
      showCropDetails: {},
      tempChart: null,
      impactCharts: {},
      trendCharts: {},
      resizeListenerAdded: false
    };
  },
  computed: {
    sortedCrops() {
      const highRisk = this.crops.filter(c => c.riskLevel === 'high');
      const mediumRisk = this.crops.filter(c => c.riskLevel === 'medium');
      const lowRisk = this.crops.filter(c => c.riskLevel === 'low');
      return [...highRisk, ...mediumRisk, ...lowRisk];
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
      this.crops.forEach(crop => {
        this.$set(this.showCropDetails, crop.id, false);
      });
      this.addResizeListener();
    });
  },
  methods: {
    updateForecastChart() {
      const dayData = this.weatherForecast[this.selectedForecastDay];
      this.forecastChart.setOption({
        animation: false,
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: Array.from({length: 24}, (_, i) => `${i}:00`),
          axisLine: {
            lineStyle: {
              color: '#e0e0e0'
            }
          },
          axisLabel: {
            color: '#666'
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#e0e0e0'
            }
          },
          axisLabel: {
            color: '#666'
          },
          splitLine: {
            lineStyle: {
              color: '#f0f0f0'
            }
          }
        },
        series: [
          {
            data: dayData.hoursTemp,
            type: 'line',
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#3b82f6'
            },
            itemStyle: {
              color: '#3b82f6'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: 'rgba(59, 130, 246, 0.5)'},
                {offset: 1, color: 'rgba(59, 130, 246, 0.1)'}
              ])
            }
          }
        ]
      });
    },
    initCharts() {
      this.initNingxiaMap();
      this.initForecastChart();
      this.initCropCharts();
    },
    initNingxiaMap() {
      if (!this.$refs.ningxiaMap) return;
      this.ningxiaMap = echarts.init(this.$refs.ningxiaMap);
      echarts.registerMap('ningxia', ningxia);
      this.ningxiaMap.setOption({
        animation: false,
        tooltip: {
          trigger: 'item',
          formatter: params => {
            const riskLevels = {
              '银川市': 'high',
              '石嘴山市': 'medium',
              '吴忠市': 'low',
              '固原市': 'medium',
              '中卫市': 'low'
            };
            const crops = {
              '银川市': '葡萄、枸杞',
              '石嘴山市': '小麦、玉米',
              '吴忠市': '枸杞、红枣',
              '固原市': '马铃薯、胡麻',
              '中卫市': '枸杞、西瓜'
            };
            return `
<div class="text-sm">
<div class="font-medium">${params.name}</div>
<div class="my-1">主要作物: ${crops[params.name]}</div>
<div>风险等级: <span class="${
                riskLevels[params.name] === 'high' ? 'text-red-500' :
                    riskLevels[params.name] === 'medium' ? 'text-yellow-500' : 'text-green-500'
            }">${
                riskLevels[params.name] === 'high' ? '高风险' :
                    riskLevels[params.name] === 'medium' ? '中风险' : '低风险'
            }</span></div>
</div>
`;
          }
        },
        visualMap: {
          min: 0,
          max: 2,
          inRange: {
            color: ['#10b981', '#f59e0b', '#ef4444']
          },
          text: ['低', '高'],
          calculable: true
        },
        series: [
          {
            name: '宁夏',
            type: 'map',
            map: 'ningxia',
            roam: true,
            label: {
              show: true,
              color: '#333'
            },
            emphasis: {
              label: {
                color: '#111'
              },
              itemStyle: {
                areaColor: '#3b82f6'
              }
            },
            data: [
              {name: '银川市', value: 2},
              {name: '石嘴山市', value: 1},
              {name: '吴忠市', value: 0},
              {name: '固原市', value: 1},
              {name: '中卫市', value: 0}
            ]
          }
        ]
      });
    },
    initForecastChart() {
      if (!this.$refs.forecastChart) return;
      this.forecastChart = echarts.init(this.$refs.forecastChart);
      this.updateForecastChart();
    },
    initCropCharts() {
      this.crops.forEach(crop => {
        if (this.$refs[`impactChart-${crop.id}`]) {
          this.impactCharts[crop.id] = echarts.init(this.$refs[`impactChart-${crop.id}`]);
          this.initImpactChart(crop);
        }
        if (this.$refs[`trendChart-${crop.id}`]) {
          this.trendCharts[crop.id] = echarts.init(this.$refs[`trendChart-${crop.id}`]);
          this.updateTrendChart(crop);
        }
      });
    },
    addResizeListener() {
      if (!this.resizeListenerAdded) {
        window.addEventListener('resize', this.handleResize);
        this.resizeListenerAdded = true;
      }
    },
    handleResize() {
      if (this.ningxiaMap) this.ningxiaMap.resize();
      if (this.forecastChart) this.forecastChart.resize();
      Object.values(this.impactCharts).forEach(chart => chart && chart.resize());
      Object.values(this.trendCharts).forEach(chart => chart && chart.resize());
    },
    generateRandomData(timeRange, min, max) {
      const lengths = {
        '24h': 24,
        '7d': 7,
        '30d': 30
      };
      const length = lengths[timeRange] || 24;
      return Array.from({length}, () => Math.floor(Math.random() * (max - min + 1)) + min);
    },
    // ... 其他方法 ...
    beforeDestroy() {
      // 销毁所有图表实例
      if (this.ningxiaMap) {
        this.ningxiaMap.dispose();
        this.ningxiaMap = null;
      }
      if (this.forecastChart) {
        this.forecastChart.dispose();
        this.forecastChart = null;
      }
      // 销毁作物图表实例
      Object.keys(this.impactCharts).forEach((key) => {
        if (this.impactCharts[key]) {
          this.impactCharts[key].dispose();
          this.impactCharts[key] = null;
        }
      });
      // 移除resize监听器
      if (this.resizeListenerAdded) {
        window.removeEventListener('resize', this.handleResize);
        this.resizeListenerAdded = false;
      }
    }
};

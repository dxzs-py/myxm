<template>
  <div class="p-4">
     <!-- 作物选择下拉框 -->
    <div class=" top-4 z-10">
      <el-select
        v-model="currentCrop"
        placeholder="请选择作物"
        size="small"
        @change="handleCropChange"
        class="w-32"
      >
        <el-option
          v-for="crop in cropOptions"
          :key="crop.value"
          :label="crop.label"
          :value="crop.value">
        </el-option>
      </el-select>
    </div>

    <!-- 生长阶段 -->
    <div @click="showDetail('growth')"
         class="mb-6 cursor-pointer rounded-lg border-gray-200 p-4 shadow-sm transition-all hover:shadow-md">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-base font-semibold text-gray-800">生长阶段</h3>
        <i class="fas fa-seedling text-green-500"></i>
      </div>
      <div class="mb-2">
        <div class="flex justify-between text-xs text-gray-600">
          <span>{{ growthStage.current }}</span>
          <span>{{ growthStage.next }}</span>
        </div>
        <div class="mt-1 h-2 w-full rounded-full bg-gray-200">
          <div :style="{ width: growthStage.progress + '%' }"
               class="h-2 rounded-full bg-green-500"></div>
        </div>
      </div>
      <p class="text-xs text-gray-500">预计{{ growthStage.daysLeft }}天后进入下一阶段</p>
    </div>

    <!-- 环境参数 -->
    <div @click="showDetail('environment')"
         class="mb-6 cursor-pointer rounded-lg border-gray-200 p-4 shadow-sm transition-all hover:shadow-md">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-base font-semibold text-gray-800">环境参数</h3>
        <i class="fas fa-temperature-low text-blue-500"></i>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div class="text-center">
          <p class="text-xs text-gray-600">温度</p>
          <p class="text-xl font-bold">{{ environment.temperature }}°C</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">湿度</p>
          <p class="text-xl font-bold">{{ environment.humidity }}%</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">光照</p>
          <p class="text-xl font-bold">{{ environment.light }}lux</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">土壤湿度</p>
          <p class="text-xl font-bold">{{ environment.soilMoisture }}%</p>
        </div>
      </div>
    </div>

    <!-- 警报 -->
    <div @click="showDetail('alerts')"
         class="mb-6 cursor-pointer rounded-lg border-gray-200 p-4 shadow-sm transition-all hover:shadow-md">
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-base font-semibold text-gray-800">预警信息</h3>
        <i class="fas fa-exclamation-triangle text-red-500"></i>
      </div>
      <div v-if="alerts.length" class="space-y-2">
        <div v-for="(alert, index) in alerts" :key="index"
             class="flex items-start rounded border-l-4 border-red-500 bg-red-50 p-2 text-xs">
          <i :class="['mt-1 mr-2', alert.icon]" :style="{ color: '#ef4444' }"></i>
          <div>
            <p class="font-medium text-red-800">{{ alert.title }}</p>
            <p class="text-red-600">{{ alert.message }}</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-gray-400">
        <p class="text-xs">暂无警报</p>
      </div>
    </div>

    <!-- 弹窗详情 -->
    <div v-if="showDetailModal"
         class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="w-full max-w-xl rounded-lg bg-white p-4 shadow-xl md:max-w-2xl">
        <div class="mb-3 flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-800">{{ detailModalTitle }}</h3>
          <button @click="closeDetailModal" class="text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="max-h-[60vh] overflow-y-auto px-2 py-1">

          <!-- 生长阶段详情 -->
          <div v-if="detailType === 'growth'" class="space-y-4">
            <div class="flex items-center space-x-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
                <i :class="growthStage.icon" class="text-xl"></i>
              </div>
              <div>
                <p class="font-medium">{{ growthStage.current }}</p>
                <p class="text-sm text-gray-600">开始于 {{ growthStage.startDate }}</p>
              </div>
            </div>
            <div>
              <p class="mb-2 text-sm font-medium text-gray-700">生长进度</p>
              <div class="h-2 w-full rounded-full bg-gray-200">
                <div :style="{ width: growthStage.progress + '%' }"
                     class="h-2 rounded-full bg-green-500"></div>
              </div>
              <div class="mt-1 flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>{{ growthStage.progress }}%</span>
                <span>100%</span>
              </div>
            </div>
            <div class="rounded-lg border border-gray-200 p-3">
              <div class="flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                  <i :class="growthStage.nextIcon" class="text-lg"></i>
                </div>
                <div>
                  <p class="font-medium">{{ growthStage.next }}</p>
                  <p class="text-sm text-gray-600">预计 {{ growthStage.daysLeft }} 天后开始</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 环境详情 -->
          <div v-if="detailType === 'environment'" class="space-y-4">
            <div class="grid grid-cols-2 gap-3">
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-temperature-high"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">温度</p>
                    <p class="font-semibold">{{ environment.temperature }}°C</p>
                  </div>
                </div>
              </div>
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-tint"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">湿度</p>
                    <p class="font-semibold">{{ environment.humidity }}%</p>
                  </div>
                </div>
              </div>
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-sun"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">光照</p>
                    <p class="font-semibold">{{ environment.light }}lux</p>
                  </div>
                </div>
              </div>
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-water"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">土壤湿度</p>
                    <p class="font-semibold">{{ environment.soilMoisture }}%</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="h-40 w-full rounded border bg-gray-50 p-2">
              <div ref="environmentDetailChart" class="h-full w-full"></div>
            </div>
          </div>

          <!-- 预警详情 -->
          <div v-if="detailType === 'alerts'" class="space-y-3">
            <div v-if="alerts.length" class="space-y-3">
              <div v-for="(alert, index) in alerts" :key="index"
                   class="flex items-start rounded border-l-4 border-red-500 bg-red-50 p-3">
                <i :class="alert.icon" class="mt-1 mr-3 text-red-500"></i>
                <div>
                  <p class="text-sm font-medium text-red-800">{{ alert.title }}</p>
                  <p class="text-xs text-red-600">{{ alert.message }}</p>
                  <p class="mt-1 text-xs text-gray-500">检测时间: {{ alert.time }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center text-gray-500">
              <p class="text-sm">当前没有预警信息</p>
            </div>
          </div>

        </div>

        <!-- 按钮 -->
        <div class="mt-6 flex justify-end space-x-3">
          <button @click="closeDetailModal"
                  class="rounded border border-gray-300 px-4 py-1 text-sm text-gray-700 hover:bg-gray-50">
            关闭
          </button>
          <button v-if="detailType === 'alerts' && alerts.length > 0"
                  @click="markAlertsAsRead"
                  class="rounded bg-blue-600 px-4 py-1 text-sm text-white hover:bg-blue-700">
            标记为已读
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: "App",
  data() {
    return {
      showMonitoringSettings: false,
      showDetailModal: false,
      detailType: '',
      // 作物选项
      cropOptions: [
        { label: '葡萄', value: '葡萄' },
        { label: '枸杞', value: '枸杞' },
        { label: '春小麦', value: '春小麦' },
        { label: '冬小麦', value: '冬小麦' }
      ],
      currentCrop: this.$store.state.selectedCrop, // 从 Vuex 获取默认作物
      growthStage: {
        current: '开花期',
        next: '结果期',
        progress: 65,
        daysLeft: 12,
        startDate: '2023-05-15',
        icon: 'fas fa-flower',
        nextIcon: 'fas fa-apple-alt'
      },
      environment: {
        temperature: 24.5,
        humidity: 68,
        light: 12500,
        soilMoisture: 42
      },
      alerts: [
        {
          title: '温度异常',
          message: '昨日最高温度超过30°C，可能影响作物生长',
          time: '2023-05-20 14:30',
          icon: 'fas fa-temperature-high'
        },
        {
          title: '湿度不足',
          message: '土壤湿度低于40%，建议增加灌溉',
          time: '2023-05-21 09:15',
          icon: 'fas fa-tint'
        }
      ],
      environmentDetailChart: null
    };
  },
  computed: {
    detailModalTitle() {
      switch (this.detailType) {
        case 'growth':
          return '生长阶段详情';
        case 'environment':
          return '环境参数详情';
        case 'alerts':
          return '预警信息详情';
        default:
          return '';
      }
    }
  },
  methods: {
    // 处理作物选择变化
    handleCropChange(value) {
      // 更新 Vuex 状态
      this.$store.commit('change_selectedCrop', value);
    },
    showDetail(type) {
      this.detailType = type;
      this.showDetailModal = true;
      this.$nextTick(() => {
        if (type === 'environment') {
          // 只有在打开环境详情时才初始化图表
          this.initEnvironmentDetailChart();
        }
      });
    },
    closeDetailModal() {
      this.showDetailModal = false;
    },
    markAlertsAsRead() {
      // 示例：清空警报
      this.alerts = [];
      // 你也可以在这里添加其他逻辑，比如调用 API 标记为已读、本地存储等
    },

    initEnvironmentDetailChart() {
      // 如果图表已经初始化，则更新数据而不是重新创建
      if (this.environmentDetailChart) {
        this.updateEnvironmentDetailChart();
      } else {
        try {
          // 使用全局挂载的 echarts 实例
          this.environmentDetailChart = this.$echarts.init(this.$refs.environmentDetailChart);
          this.updateEnvironmentDetailChart();
        } catch (error) {
          console.error('ECharts 初始化失败:', error);
        }
      }
    },
    updateEnvironmentDetailChart() {
      if (!this.environmentDetailChart) return;

      const option = {
        animation: false,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['温度', '湿度', '土壤湿度']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.generateDateLabels('7')
        },
        yAxis: [
          {
            type: 'value',
            name: '温度 (°C)',
            position: 'left',
            axisLabel: {
              formatter: '{value}'
            }
          },
          {
            type: 'value',
            name: '湿度 (%)',
            position: 'right',
            axisLabel: {
              formatter: '{value}'
            }
          }
        ],
        series: [
          {
            name: '温度',
            type: 'line',
            smooth: true,
            data: this.generateRealisticData(7, 15, 30, this.environment.temperature),
            itemStyle: {
              color: '#EF4444'
            }
          },
          {
            name: '湿度',
            type: 'line',
            smooth: true,
            yAxisIndex: 0,
            data: this.generateRealisticData(7, 40, 80, this.environment.humidity),
            itemStyle: {
              color: '#3B82F6'
            }
          },
          {
            name: '土壤湿度',
            type: 'line',
            smooth: true,
            yAxisIndex: 1,
            data: this.generateRealisticData(7, 30, 60, this.environment.soilMoisture),
            itemStyle: {
              color: '#10B981'
            }
          }
        ]
      };
      this.environmentDetailChart.setOption(option);
    },
    generateDateLabels(range, count = 7) {
      const dates = [];
      const now = new Date();
      for (let i = 0; i < count; i++) {
        const date = new Date(now);
        date.setDate(date.getDate() - (count - i - 1));
        dates.push(`${date.getMonth() + 1}/${date.getDate()}`);
      }
      return dates;
    },
    // 生成更真实的模拟数据，基于当前值进行波动
    generateRealisticData(count, min, max, currentValue) {
      const data = [];
      const baseValue = Math.max(min, Math.min(max, currentValue));
      for (let i = 0; i < count; i++) {
        // 创建基于当前值的小幅波动
        const fluctuation = (Math.random() - 0.5) * 10; // -5 到 +5 的波动
        const value = Math.round(baseValue + fluctuation);
        data.push(Math.max(min, Math.min(max, value)));
      }
      return data;
    },

  },
  beforeDestroy() {
    if (this.environmentDetailChart) {
      try {
        this.environmentDetailChart.dispose(); // 正确销毁 ECharts 实例
      } catch (error) {
        console.error('ECharts 销毁失败:', error);
      }
      this.environmentDetailChart = null;
    }
  },
  watch: {
    // 监听环境数据变化，如果弹窗打开则更新图表
    environment: {
      handler() {
        if (this.showDetailModal && this.detailType === 'environment' && this.environmentDetailChart) {
          this.updateEnvironmentDetailChart();
        }
      },
      deep: true
    }
  }
};
</script>


<style scoped>

</style>

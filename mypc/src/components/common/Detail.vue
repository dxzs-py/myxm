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
      <div v-if="growthStage.hasData" class="mb-2">
        <div class="flex justify-between text-xs text-gray-600">
          <span>{{ growthStage.current }}</span>
          <span>{{ growthStage.next }}</span>
        </div>
        <div class="mt-1 h-2 w-full rounded-full bg-gray-200">
          <div :style="{ width: growthStage.progress + '%' }"
               class="h-2 rounded-full bg-green-500"></div>
        </div>
      </div>
      <p v-if="growthStage.hasData" class="text-xs text-gray-500">预计{{ growthStage.daysLeft }}天后进入下一阶段</p>
      <p v-else class="text-xs text-orange-500">当前作物不在生长阶段</p>
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
          <p class="text-xl font-bold">{{ environment.currentTemp }}°C</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">湿度</p>
          <p class="text-xl font-bold">{{ environment.currentHumidity }}%</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">土壤湿度</p>
          <p class="text-xl font-bold">{{ environment.currentWindLevel }}%</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-600">气压</p>
          <p class="text-xl font-bold">{{ environment.currentPressure }}pa</p>
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
    <button @click="getAlertDetail">
      查看详情
    </button>

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
            <div v-if="growthStage.hasData">
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
            <div v-else class="rounded-lg border border-orange-200 bg-orange-50 p-4 text-center text-orange-700">
              <i class="fas fa-info-circle mr-2"></i>
              当前作物不在生长阶段
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
                    <p class="font-semibold">{{ environment.currentTemp }}°C</p>
                  </div>
                </div>
              </div>
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-wind"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">风速</p>
                    <p class="font-semibold">{{ environment.currentWindLevel }}%</p>
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
                    <p class="font-semibold">{{ environment.currentHumidity }}%</p>
                  </div>
                </div>
              </div>
              <div class="rounded-lg border border-gray-200 p-3">
                <div class="flex items-center space-x-2">
                  <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <i class="fas fa-compress"></i>
                  </div>
                  <div>
                    <p class="text-xs text-gray-600">气压</p>
                    <p class="font-semibold">{{ environment.currentPressure }}lux</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="h-96 w-full md:h-[500px] rounded border bg-gray-50 p-2">
              <button v-show="use_future===false" @click="updateDate(true)"
                      class="rounded bg-purple-600 px-4 py-1 text-sm text-white hover:bg-purple-700">
                查看未来预报数据
              </button>
              <button v-show="use_future===true" @click="updateDate(false)"
                      class="rounded bg-blue-600 px-4 py-1 text-sm text-white hover:bg-blue-700">
                查看历史气象数据
              </button>
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
  props: {
    environment: {
      type: Object,
      default: () => {
        return {
          currentTemp: 24.5,
          currentHumidity: 68,
          currentWindLevel: 3,
          currentPressure: 112
        }
      }
    }
  },
  data() {
    return {
      showMonitoringSettings: false,
      showDetailModal: false,
      detailType: '',
      // 作物选项
      cropOptions: [
        /*{label: '葡萄', value: '葡萄'},
        {label: '枸杞', value: '枸杞'},
        {label: '春小麦', value: '春小麦'},
        {label: '冬小麦', value: '冬小麦'}*/
      ],
      currentCrop: this.$store.getters.selectedCrop, // 从 Vuex 获取默认作物
      growthStage: {
        current: '结果期',
        next: '休眠期',
        progress: 65,
        daysLeft: 12,
        startDate: '2025-10-14',
        icon: 'fas fa-flower',
        nextIcon: 'fas fa-apple-alt',
        hasData: false
      },
      alerts: [
        {
          title: '温度异常',
          message: '昨日最低温度低于0°C，可能影响作物生长',
          time: '2025-11-04 14:30',
          icon: 'fas fa-temperature-high'
        },
        {
          title: '湿度不足',
          message: '土壤湿度低于40%，建议增加灌溉',
          time: '2025-11-06 09:15',
          icon: 'fas fa-tint'
        }
      ],
      environmentDetailChart: null,
      use_future: false,
      // 添加真实气象数据
      weatherData: [/*{
        "年份": 2022,
        "月份": 10,
        "日": 25,
        "最高气温（℃）": 18.1,
        "最低气温（℃）": 4.7,
        "平均气温（℃）": 10.9,
        "10m平均风速（m/s）": 2.6,
        "日照时数（小时）": 8.6,
        "相对湿度（%）": 48.3,
        "降水量（mm）": 0.0
      },*/
      ],
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
  created() {
    this.getCropOptions();
    this.updateDate();
    this.getCropGrowthStage();
  },
  methods: {
    getAlertDetail() {
      const selectedArea = this.$store.state.selectedArea
      this.$axios.get(`${this.$settings.HOST}/meteorology/`, {
        params: {
          address: "银川,石嘴山,固原,吴忠,中卫",
          choose: 4
        }
      }).then(response => {
        console.log(response.data)
      }).catch(error => {
        this.$message.error('获取预警详情失败:', error);
      });


    },
    // 处理作物选择变化
    handleCropChange(value) {
      // 更新 Vuex 状态
      this.$store.commit('change_selectedCrop', value);
      this.getCropGrowthStage()
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
      // 在关闭弹窗前销毁图表实例
      if (this.environmentDetailChart) {
        try {
          this.environmentDetailChart.dispose();
        } catch (error) {
          console.error('ECharts 销毁失败:', error);
        }
        this.environmentDetailChart = null;
      }
      this.showDetailModal = false;
    },
    markAlertsAsRead() {
      // 示例：清空警报
      this.alerts = [];
      // 你也可以在这里添加其他逻辑，比如调用 API 标记为已读、本地存储等
    },
    getCropGrowthStage() {
      this.$axios.get(`${this.$settings.HOST}crop/growth/`, {
        params: {
          crop: this.currentCrop
        }
      }).then(response => {
        const growth = []
        for (let item of response.data.data) {
          if ("is_previous" in item) {
            growth.push(item)
          } else if ("is_current" in item) {
            growth.push(item)
          } else if ("is_next" in item) {
            growth.push(item)
          }
        }
        // console.log(growth)
        if (growth.length === 3) {
          this.growthStage.current = growth[1].growth_cycle
          // this.growthStage.startDate = growth[1].start_date
          new Date()
          // console.log((new Date(growth[1].end_date) - new Date()) / (1000 * 60 * 60 * 24))
          // console.log((new Date(growth[2].start_date) - new Date()) / (1000 * 60 * 60 * 24))
          this.growthStage.daysLeft = ((new Date(growth[2].start_date) - new Date()) / (1000 * 60 * 60 * 24)).toFixed(2)
          this.growthStage.progress = ((new Date() - (new Date(growth[1].start_date))) / (new Date(growth[1].end_date) - new Date(growth[1].start_date)) * 100).toFixed(2)
          this.growthStage.next = growth[2].growth_cycle
          this.growthStage.hasData = true // 添加标志位
        } else if (growth.length === 0) {
          this.growthStage.hasData = false // 添加标志位
          // 清空其他属性
          this.growthStage.current = ''
          this.growthStage.next = ''
          this.growthStage.daysLeft = ''
          this.growthStage.progress = ''

        }
      }).catch(error => {
        this.$message.error("获取作物生长阶段失败");
      });
    },
    getCropOptions() {
      this.$axios.get(`${this.$settings.HOST}crop/cropClass/`).then(response => {
        for (let item of response.data.crops) {
          this.cropOptions.push({
            label: item.name,
            value: item.name
          })
        }
      }).catch(error => {
        this.$message.error("获取作物选项失败");
      });
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
    updateDate(use_future = false) {
      this.use_future = use_future;
      this.$axios.get(`${this.$settings.HOST}forecast/meteorological-data/`, {
        params: {
          use_future: use_future
        }
      }).then(response => {
        if (response.data.status === "success") {
          this.weatherData = response.data.data;
          /*console.log(this.weatherData === response.data.data)
          console.log(response.data.data)*/
          if (this.showDetailModal && this.detailType === 'environment' && this.environmentDetailChart) {
            this.updateEnvironmentDetailChart();
          }
        }
      }).catch(error => {
        this.$message.error("获取气象数据失败");
      });
    },
    updateEnvironmentDetailChart() {
      if (!this.environmentDetailChart) return;
      // 提取日期标签和温度数据
      const dateLabels = this.weatherData.map(item => `${item["月份"]}/${item["日"]}`);
      const maxTempData = this.weatherData.map(item => item["最高气温（℃）"]);
      const minTempData = this.weatherData.map(item => item["最低气温（℃）"]);
      const avgTempData = this.weatherData.map(item => item["平均气温（℃）"]);
      const windSpeedData = this.weatherData.map(item => item["10m平均风速（m/s）"]);
      const precipitationData = this.weatherData.map(item => item["降水量（mm）"]);
      const humidityData = this.weatherData.map(item => item["相对湿度（%）"]);

      const option = {
        // 启用动画效果
        animation: true,
        animationDuration: 1500,
        // 图表标题
        title: {
          text: '气象数据趋势',
          left: 'center',
          textStyle: {
            fontWeight: 'normal',
            fontSize: 14
          }
        },
        // 工具箱
        toolbox: {
          feature: {
            saveAsImage: {},
            dataZoom: {
              yAxisIndex: 'none'
            }
          },
          right: 10,
          top: 10
        },
        // 提示框
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          textStyle: {
            color: '#fff'
          },
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: function (params) {
            let result = `${params[0].axisValue}<br/>`;
            params.forEach(item => {
              // 格式化数值显示
              let value = item.value;
              if (typeof value === 'number') {
                value = value.toFixed(1);
              }
              result += `${item.marker} ${item.seriesName}: ${value}<br/>`;
            });
            return result;
          }
        },
        // 图例 - 改为横向布局，放置在顶部标题下方
        legend: {
          data: ['最高气温（℃）', '最低气温（℃）', '平均气温（℃）', '10m平均风速（m/s）', '相对湿度（%）', '降水量（mm）'],
          top: 40,
          left: 'center',
          textStyle: {
            fontSize: 11
          },
          itemWidth: 8,
          itemHeight: 8,
          orient: 'horizontal',
          // 设置图例的最大宽度，自动换行
          width: '120%'
        },
        // 网格 - 增大上下左右边距
        grid: {
          left: '6%',
          right: '15%', // 增加右侧空间以容纳多个Y轴
          bottom: '15%', // 增加底部空间以避免X轴标签重叠
          top: '40%', // 增加顶部空间以容纳标题和图例
          containLabel: true
        },
        // X轴
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dateLabels,
          axisLabel: {
            rotate: 30, // 稍微减小旋转角度
            interval: 0,
            fontSize: 10
          },
          axisLine: {
            lineStyle: {
              color: '#ccc'
            }
          }
        },
        // Y轴 - 优化布局，减少重叠
        yAxis: [
          {
            type: 'value',
            name: '温度 (°C)',
            position: 'left',
            axisLabel: {
              formatter: '{value}°C',
              fontSize: 10
            },
            nameTextStyle: {
              fontSize: 10
            },
            splitLine: {
              lineStyle: {
                type: 'dashed',
                color: '#f0f0f0'
              }
            }
          },
          {
            type: 'value',
            name: '湿度 (%)',
            position: 'right',
            axisLabel: {
              formatter: '{value}%',
              fontSize: 10
            },
            nameTextStyle: {
              fontSize: 10
            },
            splitLine: {
              show: false
            }
          },
          {
            type: 'value',
            name: '风速/降水量',
            position: 'right',
            offset: 50, // 适当调整偏移量
            axisLabel: {
              formatter: '{value}',
              fontSize: 10
            },
            nameTextStyle: {
              fontSize: 10,
              padding: [0, 0, 0, 50] // 调整名称位置，避免重叠
            },
            splitLine: {
              show: false
            }
          }
        ],
        // 数据系列 - 保持原有样式，但适当调整宽度
        series: [
          // 最高气温
          {
            name: '最高气温（℃）',
            type: 'line',
            smooth: true,
            data: maxTempData,
            lineStyle: {
              width: 2
            },
            itemStyle: {
              color: '#EF4444'
            },
            areaStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: 'rgba(239, 68, 68, 0.3)'},
                {offset: 1, color: 'rgba(239, 68, 68, 0.1)'}
              ])
            },
          },
          // 最低气温
          {
            name: '最低气温（℃）',
            type: 'line',
            smooth: true,
            data: minTempData,
            lineStyle: {
              width: 2
            },
            itemStyle: {
              color: '#3B82F6'
            },
            areaStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: 'rgba(59, 130, 246, 0.3)'},
                {offset: 1, color: 'rgba(59, 130, 246, 0.1)'}
              ])
            },
          },
          // 平均气温
          {
            name: '平均气温（℃）',
            type: 'line',
            smooth: true,
            yAxisIndex: 0,
            data: avgTempData,
            lineStyle: {
              width: 1.5,
              type: 'dashed'
            },
            itemStyle: {
              color: '#0EA5E9'
            },
            showSymbol: false
          },
          // 风速
          {
            name: '10m平均风速（m/s）',
            type: 'line',
            smooth: true,
            yAxisIndex: 2,
            data: windSpeedData,
            lineStyle: {
              width: 2
            },
            itemStyle: {
              color: '#10B981'
            },
            showSymbol: false
          },
          // 湿度
          {
            name: '相对湿度（%）',
            type: 'line',
            smooth: true,
            yAxisIndex: 1,
            data: humidityData,
            lineStyle: {
              width: 2
            },
            itemStyle: {
              color: '#1E40AF'
            },
            areaStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: 'rgba(30, 64, 175, 0.3)'},
                {offset: 1, color: 'rgba(30, 64, 175, 0.1)'}
              ])
            }
          },
          // 降水量
          {
            name: '降水量（mm）',
            type: 'bar',
            yAxisIndex: 2,
            data: precipitationData,
            itemStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: '#60A5FA'},
                {offset: 1, color: '#3B82F6'}
              ])
            },
            barWidth: '50%' // 稍微减小柱状图宽度
          }
        ]
      };

      this.environmentDetailChart.setOption(option);

      // 响应式调整保持不变
      const resizeHandler = () => {
        if (this.environmentDetailChart) {
          this.environmentDetailChart.resize();
        }
      };

      window.removeEventListener('resize', resizeHandler);
      window.addEventListener('resize', resizeHandler);

      this.$once('hook:beforeDestroy', () => {
        window.removeEventListener('resize', resizeHandler);
      });
    }

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
    },
    weatherData: {
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

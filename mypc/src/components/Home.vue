<template>
  <div class="min-h-screen bg-gray-50">
    <section class="container mx-auto px-6 py-8">
      <div class="p-6 bg-gray-100">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

          <div class=" p-6 rounded-xl shadow-lg">
            <h2 class="mb-6 text-2xl font-bold text-slate-800">实时气象数据({{ selectedArea }})</h2>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-700">当前气象状况</h3>
              <p class="ml-auto text-sm text-gray-500">更新时间: {{ currentTime }}</p>
              <i class="fas fa-sync-alt cursor-pointer text-blue-500" style="padding-left: 5px" ref="refreshIcon"
                 @click="refreshData"></i>
            </div>
            <div class="text-sm text-gray-600">
              主要作物：{{ areaData[selectedArea].crops.join('、') }}
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center">
                <div
                  class="text-6xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500">
                  {{ currentenvironment.currentTemp }}°C
                </div>
                <p class="text-sm text-gray-500">当前温度</p>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-blue-600">{{ currentenvironment.currentHumidity }}%</div>
                <p class="text-sm text-gray-500">湿度</p>
              </div>
              <div class="text-center">
                <div class="flex items-center justify-center">
                  <i class="fas fa-wind mr-2 text-blue-600"></i>
                  <span class="text-xl font-bold">{{ currentenvironment.currentWindLevel }}级</span>
                </div>
              </div>
              <div class="text-center">
                <div class="text-xl font-bold text-blue-600">{{ currentenvironment.currentPressure }} hPa</div>
                <p class="text-sm text-gray-500">气压</p>
              </div>
            </div>
            <div class="my-6 border-t border-gray-200"></div>
            <!-- 预测数据 -->
            <!-- 下拉框和预测数据内容 -->
            <div class="flex items-center justify-between mb-4">
              <h2 class="mb-6 text-xl font-semibold text-gray-800">气象预测({{ selectedArea }})</h2>
              <select v-model="selectedForecastDay"
                      class="bg-white/50 backdrop-blur-sm border border-gray-300/30 rounded-xl px-4 py-2 text-sm font-medium">
                <option v-for="(day, index) in weatherForecast" :key="index" :value="index">
                  {{ day.date }}
                </option>
              </select>
            </div>
            <!-- 预测数据展示内容 -->
            <div class="bg-gray-50/50 p-4 rounded-lg ">
              <div class="flex items-center justify-between mb-4">
                <h2 class="mb-6 text-2xl font-bold text-slate-800">气象预测</h2>
                <p class="ml-auto text-sm text-gray-500">更新时间: {{ currentTime }}</p>
                <i class="fas fa-sync-alt cursor-pointer text-blue-500" style="padding-left: 5px" ref="refreshIcon"
                 @click="refreshData"></i>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                  <div
                    class="text-6xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500">
                    {{
                      (weatherForecast[selectedForecastDay].temp_max +
                        weatherForecast[selectedForecastDay].temp_min) /
                      2
                    }}°C
                  </div>
                  <p class="text-sm text-gray-500">平均温度</p>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-blue-600">
                    {{ weatherForecast[selectedForecastDay].humidity }}%
                  </div>
                  <p class="text-sm text-gray-500">湿度</p>
                </div>

                <div class="text-center">
                  <div class="flex items-center justify-center">
                    <i class="fas fa-wind mr-2 text-blue-600"></i>
                    <span class="text-xl font-bold">
                    {{ weatherForecast[selectedForecastDay].windSpeedDay }}级
                  </span>
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-xl font-bold text-blue-600">
                    {{ weatherForecast[selectedForecastDay].pressure }} hPa
                  </div>
                  <p class="text-sm text-gray-500">气压</p>
                </div>
              </div>
            </div>
          </div>
          <div class="hidden md:block md:col-span-1 border-l border-gray-200 shadow-lg">
            <!-- 地图区块 -->
            <div class="overflow-hidden md:col-span-2 p-4  rounded-lg">
              <div class=" w-full" style="height: 677px; width: 24vw">
                <NXmap></NXmap>
              </div>
            </div>
          </div>
          <div class="hidden md:block md:col-span-1 border-l border-gray-200 shadow-lg h-full">

            <Detail :environment="currentenvironment"></Detail>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>

import NXmap from "./common/NingXiaMap.vue";
import Detail from "./common/Detail.vue";
import {debounce} from 'lodash'

export default {
  components: {NXmap, Detail},
  data() {
    return {
      // 地图实例
      combinedMap: null,
      // 实时气象数据

      currentenvironment: {
        currentTemp: 12,
        currentHumidity: 65,
        currentWindLevel: 3,
        currentPressure: 112,
      },

      isRefreshing: false,

      // 地区数据
      areaData: {
        '银川市': {temp: 12, humidity: 65, windLevel: 3, pressure: 1012, crops: ['葡萄', '枸杞'],status: false},
        '石嘴山市': {temp: 10, humidity: 58, windLevel: 4, pressure: 1015, crops: ['小麦'],status: false},
        '吴忠市': {temp: 11, humidity: 62, windLevel: 2, pressure: 1013, crops: ['枸杞', '葡萄'],status: false},
        '固原市': {temp: 8, humidity: 55, windLevel: 3, pressure: 1018, crops: ['葡萄'],status: false},
        '中卫市': {temp: 13, humidity: 60, windLevel: 2, pressure: 1014, crops: ['枸杞', '小麦'],status: false}
      },

      // 天气预测数据
      weatherForecast: [
        {date: '2025-05-16', temp_max: 15, temp_min: 4, humidity: 45, windSpeedDay: 3, pressure: 1012},
        {date: '2025-05-17', temp_max: 13, temp_min: 3, humidity: 55, windSpeedDay: 4, pressure: 1015},
        {date: '2025-05-18', temp_max: 2, temp_min: 10, humidity: 75, windSpeedDay: 3, pressure: 1018},
        {date: '2025-05-19', temp_max: 8, temp_min: 1, humidity: 65, windSpeedDay: 2, pressure: 1020},
        {date: '2025-05-20', temp_max: 12, temp_min: 0, humidity: 50, windSpeedDay: 3, pressure: 1015},
        {date: '2025-05-21', temp_max: 11, temp_min: -1, humidity: 55, windSpeedDay: 4, pressure: 1018},
        {date: '2025-05-22', temp_max: 5, temp_min: -3, humidity: 70, windSpeedDay: 3, pressure: 1022}
      ],
      selectedForecastDay: 0,
      // 显示状态
      currentTime: new Date().toLocaleString()
    };
  },
  computed: {
    selectedArea() {
      return this.$store.state.selectedArea;
    },
  },
  created() {
    this.currentAreaData()
    this.ForecastAreaData()
  },
  mounted() {
    this.$nextTick(() => {
      this.initData();
    });
  },
  methods: {
    ForecastAreaData() {
      this.$axios.get(`${this.$settings.HOST}/meteorology/`, {
        params: {
          address: this.selectedArea,
          choose: 2,
          days: 7
        }
      }).then(response => {
        this.weatherForecast = response.data[0].forecast
      }).catch(error => {
        this.$message.error(error.response.data.message + '，请稍后再试');
      })
    },
    // 包装刷新逻辑
    refreshData: debounce(async function () {
      this.isRefreshing = true
      try {
        this.$refs.refreshIcon.classList.add('animate-spin');
        await this.currentAreaData() // 等待数据更新完成
        this.$message.success({
          message: '数据刷新成功',
          duration: 700
        })  // 成功提示
      } catch (error) {
        this.$message.error({
          message: '数据刷新失败，请稍后再试',
          duration: 700
        }) // 失败提示
      } finally {
        this.$refs.refreshIcon.classList.remove('animate-spin');
        this.isRefreshing = false
      }
    }, 300),
    currentAreaData() {
      if (this.areaData[this.selectedArea].status ) {
        // 更新数据
        this.initData();
        // 更新时间戳
        // 修改时间显示格式
        this.currentTime = new Date().toLocaleString('zh-CN', {
          hour12: false,
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });
        return;
      }
      this.$axios.get(`${this.$settings.HOST}/meteorology/`, {
        params: {
          address: this.selectedArea,
          choose: 1
        }
      }).then(response => {
        const data = response.data[0].current
        // 使用 Vue.set 确保响应式更新
        this.$set(this.areaData[this.selectedArea], 'temp', data.temperature)
        this.$set(this.areaData[this.selectedArea], 'humidity', data.humidity)
        this.$set(this.areaData[this.selectedArea], 'windLevel', data.windspeed)
        this.$set(this.areaData[this.selectedArea], 'pressure', data.pressure)
        this.$set(this.areaData[this.selectedArea], 'status', true)
        // 更新数据
        this.initData();
        // 更新时间戳
        // 修改时间显示格式
        this.currentTime = new Date().toLocaleString('zh-CN', {
          hour12: false,
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });

      }).catch(error => {
        this.$message.error(error.response.data.message + '，请稍后再试');
      })
    },
    updateAreaData(areaName) {
      const data = this.areaData[areaName];
      if (data) {
        this.$set(this.currentenvironment, 'currentTemp', data.temp);
        this.$set(this.currentenvironment, 'currentHumidity', data.humidity);
        this.$set(this.currentenvironment, 'currentWindLevel', data.windLevel);
        this.$set(this.currentenvironment, 'currentPressure', data.pressure);
      }
    },
    initData(value) {
      this.updateAreaData(this.selectedArea || value);
    },
  },
  watch: {
    selectedArea(newVal) {
      this.currentAreaData();
      this.ForecastAreaData();
    }
  },
};

</script>


<style scoped>

.rounded-lg {
  transition: all 0.3s ease;
}

/* 在样式表中补充 */
@media (min-width: 768px) {
  .data-section {
    padding: 2rem; /* p-8 */
  }
}


</style>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <Header class="bg-white shadow-sm h-16 sticky w-full top-0 z-50">
    </Header>

    <main class="container mx-auto px-4 py-6">
<div class="bg-gradient-to-br from-purple-50 via-purple-100 to-purple-200 rounded-3xl shadow-xl mb-16 overflow-hidden transition-all duration-500 hover:shadow-2xl">
  <div class="p-12 max-w-8xl mx-auto">
    <h2 class="text-5xl font-bold mb-12 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-100 flex items-center animate-gradient-x">
      <i class="fas fa-sun-cloud  mr-5 text-4xl animate-pulse"></i>
      气象数据概览
    </h2>
    <div class="flex flex-col lg:flex-row gap-8 justify-between">
      <div
        v-for="(weatherData, D) in Data"
        :key="D"
        class="transform transition-all duration-500 hover:scale-[1.02] flex-1"
      >
        <WeatherCard
          :title="weatherData.title"
          :data="weatherData.DataDetaile"
          class="w-full max-w-4xl transition-all duration-300 hover:shadow-xl hover:shadow-purple-300/30 mx-auto"
        />
      </div>
    </div>
  </div>
</div>


      <!-- 种植区域分布 -->
      <div class="bg-white rounded-lg shadow-sm mb-6" >
        <div class="p-4 border-b">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-medium">种植区域分布</h2>
            <DropdownMenu
              :show="dropdownStates.crop"
              :options="cropTypes"
              :selected="selectedCrop"
              @select="selectCrop"
              @toggle="toggleDropdown('crop')"
            >
              <template #trigger>
                <button class="bg-gray-100 px-4 py-2 rounded-lg flex items-center">
                  {{ selectedCrop ? getCropLabel(selectedCrop) : '选择关注作物' }}
                  <i class="fas fa-chevron-down ml-2"></i>
                </button>
              </template>
            </DropdownMenu>
          </div>
        </div>
        <div class="p-4">
          <div ref="plantingMapChart" class="w-full h-96"></div>
          <div v-if="selectedCrop" :class="['mt-4 p-4 rounded-lg', cropConfig.alertClass]">
            <h3 class="font-medium">{{ cropConfig.title }}</h3>
            <p class="mt-1">{{ cropConfig.message }}</p>
          </div>
        </div>
      </div>

      <!-- 风险预警和趋势分析 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-sm">
          <div class="p-4 border-b">
            <div class="flex justify-between items-center">
              <h2 class="text-lg font-medium">风险等级分布</h2>
              <div class="flex space-x-2">
                <button class="bg-green-600 text-white px-4 py-2 !rounded-button whitespace-nowrap flex items-center">
                  <i class="fas fa-download mr-2"></i>导出数据
                </button>
                <button class="bg-green-600 text-white px-4 py-2 !rounded-button whitespace-nowrap flex items-center">
                  <i class="fas fa-share mr-2"></i>分享
                </button>
              </div>
            </div>
          </div>
          <div ref="riskMapChart" class="w-full h-80"></div>
        </div>

        <div class="bg-white rounded-lg shadow-sm">
          <div class="p-4 border-b">
            <h2 class="text-lg font-medium">未来气象趋势</h2>
          </div>
          <div ref="weatherTrendChart" class="w-full h-80"></div>
        </div>
      </div>

      <!-- 作物防护建议 -->
      <div class="bg-white rounded-lg shadow-sm mb-6">
        <div class="p-4 border-b">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-medium">作物防护建议</h2>
            <DropdownMenu
              :show="dropdownStates.cropType"
              :options="cropTypes"
              :selected="cropType"
              @select="selectCropType"
              @toggle="toggleDropdown('cropType')"
            >
              <template #trigger>
                <button class="bg-gray-100 px-4 py-2 rounded-lg flex items-center">
                  {{ cropType ? getCropLabel(cropType) : '选择作物类型' }}
                  <i class="fas fa-chevron-down ml-2"></i>
                </button>
              </template>
            </DropdownMenu>
          </div>
        </div>
        <div class="p-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="(advice, index) in cropAdvice" :key="index"
                 class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div class="relative">
                <img
                  :data-src="advice.image"
                  alt="作物防护"
                  class="w-full h-48 object-cover rounded-t-lg lazyload"
                />
                <span
                  :class="['absolute top-2 right-2 px-2 py-1 rounded text-sm text-white', riskLevelStyles[advice.riskLevel]]">
                  {{ riskLevelTexts[advice.riskLevel] }}
                </span>
                </div>
                <div class="p-4">
                  <h3 class="font-medium mb-2">{{ advice.crop }}</h3>
                  <p class="text-gray-600 text-sm">{{ advice.suggestion }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 用户反馈 -->
        <div class="bg-white rounded-lg shadow-sm">
          <div class="p-4 border-b">
            <h2 class="text-lg font-medium">用户反馈</h2>
          </div>
          <div class="p-4">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">反馈类型</label>
                <DropdownMenu
                  :show="dropdownStates.feedback"
                  :options="feedbackOptions"
                  :selected="feedback.type"
                  @select="selectFeedbackType"
                  @toggle="toggleDropdown('feedback')"
                >
                  <template #trigger>
                    <button class="w-full bg-gray-100 px-4 py-2 rounded-lg text-left flex items-center justify-between">
                      {{ feedback.type ? getFeedbackLabel(feedback.type) : '请选择反馈类型' }}
                      <i class="fas fa-chevron-down"></i>
                    </button>
                  </template>
                </DropdownMenu>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">反馈内容</label>
                <textarea
                  v-model="feedback.content"
                  rows="4"
                  class="w-full px-4 py-2 bg-gray-100 rounded-lg border-none resize-none focus:outline-none"
                  placeholder="请输入您的反馈内容"
                ></textarea>
              </div>
              <div>
                <button @click="submitFeedback"
                        class="bg-green-600 text-white px-6 py-2 !rounded-button whitespace-nowrap hover:bg-green-700">
                  提交反馈
                </button>
              </div>
            </div>
          </div>
        </div>
    </main>
  </div>
</template>

<script>
import Header from "./common/Header.vue";
import DropdownMenu from "./common/DropdownMenu.vue";
import WeatherCard from "./common/WeatherCard.vue";
import * as echarts from 'echarts';
// 引入ningxia地图数据,不知道干嘛呢


export default {
  components: {
    Header,
    DropdownMenu,
    WeatherCard
  },
  data() {
    return {
      dropdownStates: {
        crop: false,
        cropType: false,
        feedback: false
      },
      chartInstances: {
        plantingMap: null,
        riskMap: null,
        weatherTrend: null
      },

      Data: [
        {
          title: '当前天气',
          DataDetaile: [
            {label: '温度', value: '-8.5°C', icon: 'fa-sun', iconColor: 'text-yellow-500'},
            {label: '湿度', value: '59.0%', icon: 'fa-cloud', iconColor: 'text-blue-500'},
            {label: '降水量', value: '0.0mm', icon: 'fa-bolt', iconColor: 'text-purple-500'},
            {label: '风速', value: '1m/s', icon: 'fa-wind', iconColor: 'text-green-500'}
          ],
        },
        {
          title: '预测天气',
          DataDetaile: [
            {label: '温度', value: '-6.8°C', icon: 'fa-sun', iconColor: 'text-yellow-500'},
            {label: '湿度', value: '66.0%', icon: 'fa-cloud', iconColor: 'text-blue-500'},
            {label: '降水量', value: '0.0mm', icon: 'fa-bolt', iconColor: 'text-purple-500'},
            {label: '风速', value: '2.7m/s', icon: 'fa-wind', iconColor: 'text-green-500'}
          ],
        }
      ],

      cropTypes: [
        {label: '枸杞', value: 'goji'},
        {label: '葡萄', value: 'grape'},
        {label: '硒砂瓜', value: 'watermelon'}
      ],
      cropAdvice: [
        {
          crop: '宁夏枸杞',
          suggestion: '近期有霜冻风险，建议采取防寒措施，可使用防寒布覆盖。',
          image: '/static/image/gq1.jpg/',
          riskLevel: 'high'
        },
        {
          crop: '贺兰山葡萄',
          suggestion: '预计未来三天降雨，注意排水防涝，加强病害防治。',
          image: '/static/image/pt1.jpg/',
          riskLevel: 'medium'
        },
        {
          crop: '中卫硒砂瓜',
          suggestion: '当前温度适宜生长，建议适时进行追肥和灌溉。',
          image: '/static/image/xsg1.png/',
          riskLevel: 'low'
        }
      ],
      cropConfigMap: {
        goji: {
          title: '高风险预警',
          message: '当前气温偏低，预计未来3天将出现霜冻天气，建议及时采取防寒措施。',
          alertClass: 'bg-red-50 text-red-700'
        },
        grape: {
          title: '注意事项',
          message: '近期降水偏多，葡萄园需注意排涝防渍，同时注意防范病害发生。',
          alertClass: 'bg-yellow-50 text-yellow-700'
        },
        watermelon: {
          title: '适宜生长',
          message: '目前气温和降水条件适宜硒砂瓜生长，建议按照常规种植方案进行管理。',
          alertClass: 'bg-green-50 text-green-700'
        }
      },
      feedback: {
        type: '',
        content: ''
      },
      feedbackOptions: [
        {label: '系统建议', value: 'system'},
        {label: '数据问题', value: 'data'},
        {label: '其他', value: 'other'}
      ],
      riskLevelStyles: {
        low: 'bg-green-500',
        medium: 'bg-yellow-500',
        high: 'bg-red-500'
      },
      riskLevelTexts: {
        low: '低风险',
        medium: '中度风险',
        high: '高风险'
      },
      searchQuery: '',
      cropType: '',
      selectedCrop: ''
    };
  },
  computed: {
    cropConfig() {
      return this.cropConfigMap[this.selectedCrop] || {};
    }
  },
  methods: {
    initLazyLoad() {
      const lazyImages = this.$el.querySelectorAll('.lazyload'); // 获取所有具有 .lazyload 类的元素
      const observer = new IntersectionObserver((entries) => {
        //
        for (let i = 0; i < entries.length; i++) {
          const entry = entries[i];
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
          }
        }
      }, {rootMargin: '0px 0px 200px 0px'});

      // IntersectionObserver 是浏览器提供的 API，用于监听元素是否进入视口（即是否可见）
      // entries 是一组观察目标的集合
      // entry.isIntersecting 表示该图片是否进入可视区域
      // img.src = img.dataset.src 将图片的真实地址赋值给 src 属性，触发加载
      // observer.unobserve(img) 一旦图片加载完成，就停止监听，避免重复操作
      // rootMargin: '0px 0px 200px 0px' 表示在图片距离底部还有 200px 的时候就开始加载，提前加载一部分，提升用户体验

      // 替换 lazyImages.forEach(img => ...) 为 for 循环
      for (let i = 0; i < lazyImages.length; i++) {
        const img = lazyImages[i];
        observer.observe(img);
      }// 对每个带有 .lazyload 类的图片元素，调用 observer.observe(img) 进行监听
    },

    toggleDropdown(type) {
      // 关闭所有下拉菜单 确保同一时间只有一个下拉菜单处于打开状态
      for (let key in this.dropdownStates) {
        this.dropdownStates[key] = key === type ? !this.dropdownStates[key] : false;
      }
    },
    selectCrop(value) {
      this.selectedCrop = value;
      this.dropdownStates.crop = false;
    },
    selectCropType(value) {
      this.cropType = value;
      this.dropdownStates.cropType = false;
    },
    selectFeedbackType(value) {
      this.feedback.type = value;
      this.dropdownStates.feedback = false;
    },
    getCropLabel(value) {
      const crop = this.cropTypes.find(c => c.value === value);
      return crop ? crop.label : '';
    },
    getFeedbackLabel(value) {
      const option = this.feedbackOptions.find(o => o.value === value);
      return option ? option.label : '';
    },
    submitFeedback() {
      if (!this.feedback.type || !this.feedback.content) {
        this.$message.error('请完整填写反馈信息');
        return;
      }
      this.$message.success('反馈提交成功');
      this.feedback = {
        type: '',
        content: ''
      };
    },
    initChart(refName, chartKey, optionGetter) {
      try {
        const chartDom = this.$refs[refName];
        if (!chartDom) return;

        const chart = this.$echarts.init(chartDom);
        const option = optionGetter.call(this);
        chart.setOption(option);
        this.chartInstances[chartKey] = chart;
      } catch (error) {
        console.error(`图表初始化失败: ${chartKey}`, error);
      }
    },
    getPlantingMapOption() {
      return {
        animation: false,
        title: {text: '宁夏主要特色作物种植区域'},
        tooltip: {trigger: 'item', formatter: '{b}: {c}'},
        visualMap: {
          min: 0,
          max: 100,
          text: ['种植密度高', '种植密度低'],
          calculable: true,
          inRange: {color: ['#e0f3db', '#43a2ca', '#0868ac']}
        },
        series: [{
          name: '宁夏',
          type: 'map',
          map: 'ningxia',
          label: {show: true, fontSize: 14},
          data: [
            {name: '银川市', value: 95},
            {name: '石嘴山市', value: 80},
            {name: '吴忠市', value: 85},
            {name: '固原市', value: 60},
            {name: '中卫市', value: 75}
          ],
          emphasis: {
            itemStyle: {
              areaColor: '#91cc75',
              borderWidth: 2
            }
          }
        }]
      };
    },
    getRiskMapOption() {
      return {
        animation: false,
        title: {text: '区域风险分布'},
        tooltip: {trigger: 'item'},
        series: [{
          type: 'pie',
          radius: '70%',
          data: [
            {value: 30, name: '低风险', itemStyle: {color: '#67C23A'}},
            {value: 40, name: '中风险', itemStyle: {color: '#E6A23C'}},
            {value: 20, name: '高风险', itemStyle: {color: '#F56C6C'}},
            {value: 10, name: '严重风险', itemStyle: {color: '#909399'}}
          ]
        }]
      };
    },
    getWeatherTrendOption() {
      return {
        animation: false,
        title: {text: '未来7天温度趋势'},
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value',
          name: '温度(°C)'
        },
        series: [{
          data: [23, 24, 25, 26, 25, 24, 23],
          type: 'line',
          smooth: true
        }]
      };
    },

    initCharts() {
      this.initChart('plantingMapChart', 'plantingMap', this.getPlantingMapOption);
      this.initChart('riskMapChart', 'riskMap', this.getRiskMapOption);
      this.initChart('weatherTrendChart', 'weatherTrend', this.getWeatherTrendOption);

      window.addEventListener('resize', this.resizeCharts);
    },
    resizeCharts() {
      for (let key in this.chartInstances) {
        const chart = this.chartInstances[key];
        if (chart) chart.resize();
      }
    },

    closeAllDropdowns() {
      for (let key in this.dropdownStates) {
        this.dropdownStates[key] = false;
      }
    }
  }
  ,
  mounted() {
    this.initCharts();
    this.initLazyLoad();

    // 添加点击外部关闭下拉菜单
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.relative')) {
        this.closeAllDropdowns();
      }
    });
  }
  ,
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeCharts);
    document.removeEventListener('click', this.closeAllDropdowns);

    // 销毁所有图表实例
    for (let key in this.chartInstances) {
      const chart = this.chartInstances[key];
      if (chart) chart.dispose();
    }
  }
}
;
</script>

<style scoped>



textarea:focus,
input:focus {
  outline: none;
}

.lazyload {
  opacity: 80%;
  transition: opacity 0.3s;
}

.lazyload.loaded {
  opacity: 1;
}
</style>

<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->

<template>
<div class="min-h-screen bg-gray-50">
<!-- 顶部导航 -->
<header class="bg-white shadow-sm">
<div class="container mx-auto px-4 h-16 flex items-center justify-between">
<div class="flex items-center space-x-2">
<i class="fas fa-seedling text-2xl text-green-600"></i>
<h1 class="text-xl font-medium">宁夏特色作物气象灾害风险识别与预警系统</h1>
</div>
<div class="flex items-center space-x-8">
<nav class="flex space-x-6">
<a href="home" class="text-gray-700 hover:text-green-600">首页</a>
<a href="#" class="text-gray-700 hover:text-green-600">数据中心</a>
<a href="klg" class="text-gray-700 hover:text-green-600">种植指南</a>
<a href="#" class="text-gray-700 hover:text-green-600">用户反馈</a>
</nav>
<div class="relative">
<div class="relative flex items-center">
  <input
    v-model="searchQuery"
    class="w-64 h-10 pl-10 pr-4 rounded-lg border-none bg-gray-100 focus:outline-none"
    placeholder="搜索作物或地区"
  />
  <i class="fas fa-search absolute left-3 text-gray-400"></i>
</div>
</div>
<div class="flex items-center space-x-4">
<button class="bg-green-600 text-white px-4 py-2 !rounded-button whitespace-nowrap hover:bg-green-700"><router-link to="/user/login/?isLogin=true">登录</router-link></button>
<button class="bg-gray-100 px-4 py-2 !rounded-button whitespace-nowrap hover:bg-gray-200"><router-link to="/user/login/?isLogin=false">注册</router-link></button>
</div>
</div>
</div>
</header>

<main class="container mx-auto px-4 py-6">
<!-- 实时气象数据 -->
<div class="grid grid-cols-4 gap-4 mb-6">
<div v-for="(item, index) in weatherData" :key="index" class="bg-white p-4 rounded-lg shadow-sm">
<div class="flex justify-between items-center mb-2">
<span class="text-gray-600">{{ item.label }}</span>
<i :class="['fas', item.icon, item.iconColor]"></i>
</div>
<div class="text-2xl font-semibold">{{ item.value }}</div>
</div>
</div>

<!-- 种植区域分布 -->
<div class="bg-white rounded-lg shadow-sm mb-6">
<div class="p-4 border-b">
<div class="flex justify-between items-center">
<h2 class="text-lg font-medium">种植区域分布</h2>
<div class="relative">
  <button @click="toggleCropSelect" class="bg-gray-100 px-4 py-2 rounded-lg flex items-center">
    {{ selectedCrop ? getCropLabel(selectedCrop) : '选择关注作物' }}
    <i class="fas fa-chevron-down ml-2"></i>
  </button>
  <div v-if="showCropSelect" class="absolute top-full mt-1 right-0 bg-white shadow-lg rounded-lg z-10">
    <div v-for="crop in cropTypes"
         :key="crop.value"
         @click="selectCrop(crop.value)"
         class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
      {{ crop.label }}
    </div>
  </div>
</div>
</div>
</div>
<div class="p-4">
<div ref="plantingMapChart" class="w-full h-96"></div>
<div v-if="selectedCrop" :class="['mt-4 p-4 rounded-lg', alertClass]">
<h3 class="font-medium">{{ getCropAlertTitle }}</h3>
<p class="mt-1">{{ getCropAlertMessage }}</p>
</div>
</div>
</div>

<!-- 风险预警和趋势分析 -->
<div class="grid grid-cols-2 gap-6 mb-6">
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
<div class="relative">
  <button @click="toggleCropTypeSelect" class="bg-gray-100 px-4 py-2 rounded-lg flex items-center">
    {{ cropType ? getCropLabel(cropType) : '选择作物类型' }}
    <i class="fas fa-chevron-down ml-2"></i>
  </button>
  <div v-if="showCropTypeSelect" class="absolute top-full mt-1 right-0 bg-white shadow-lg rounded-lg z-10">
    <div v-for="crop in cropTypes"
         :key="crop.value"
         @click="selectCropType(crop.value)"
         class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
      {{ crop.label }}
    </div>
  </div>
</div>
</div>
</div>
<div class="p-4">
<div class="grid grid-cols-3 gap-4">
<div v-for="(advice, index) in cropAdvice" :key="index" class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
<div class="relative">
<img :src="advice.image" :alt="advice.crop" class="w-full h-48 object-cover rounded-t-lg" />
<span :class="['absolute top-2 right-2 px-2 py-1 rounded text-sm text-white', getRiskLevelClass(advice.riskLevel)]">
  {{ getRiskLevelText(advice.riskLevel) }}
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
<div class="relative">
  <button @click="toggleFeedbackSelect" class="w-full bg-gray-100 px-4 py-2 rounded-lg text-left flex items-center justify-between">
    {{ feedback.type ? getFeedbackLabel(feedback.type) : '请选择反馈类型' }}
    <i class="fas fa-chevron-down"></i>
  </button>
  <div v-if="showFeedbackSelect" class="absolute top-full mt-1 left-0 right-0 bg-white shadow-lg rounded-lg z-10">
    <div v-for="option in feedbackOptions"
         :key="option.value"
         @click="selectFeedbackType(option.value)"
         class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
      {{ option.label }}
    </div>
  </div>
</div>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">反馈内容</label>
<textarea
  v-model="feedback.content"
  rows="4"
  class="w-full px-4 py-2 bg-gray-100 rounded-lg border-none resize-none focus:outline-none"
  placeholder="请输入您的反馈内容">
</textarea>
</div>
<div>
<button @click="submitFeedback" class="bg-green-600 text-white px-6 py-2 !rounded-button whitespace-nowrap hover:bg-green-700">
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
export default {
  data() {
    return {
      searchQuery: '',
      cropType: '',
      selectedCrop: '',
      showCropSelect: false,
      showCropTypeSelect: false,
      showFeedbackSelect: false,
      weatherData: [
        { label: '温度', value: '26°C', icon: 'fa-sun', iconColor: 'text-yellow-500' },
        { label: '湿度', value: '65%', icon: 'fa-cloud', iconColor: 'text-blue-500' },
        { label: '降水量', value: '2.5mm', icon: 'fa-bolt', iconColor: 'text-purple-500' },
        { label: '风速', value: '3.2m/s', icon: 'fa-wind', iconColor: 'text-green-500' }
      ],
      cropTypes: [
        { label: '枸杞', value: 'goji' },
        { label: '葡萄', value: 'grape' },
        { label: '玉米', value: 'corn' }
      ],
      cropAdvice: [
        {
          crop: '宁夏枸杞',
          suggestion: '近期有霜冻风险，建议采取防寒措施，可使用防寒布覆盖。',
          image: 'https://ai-public.mastergo.com/ai/img_res/93f47791e9086f4dc35be5d98286f595.jpg',
          riskLevel: 'high'
        },
        {
          crop: '贺兰山葡萄',
          suggestion: '预计未来三天降雨，注意排水防涝，加强病害防治。',
          image: 'https://ai-public.mastergo.com/ai/img_res/558cc0da8280e09a4d6ff81ebb9cf976.jpg',
          riskLevel: 'medium'
        },
        {
          crop: '青铜峡玉米',
          suggestion: '当前温度适宜生长，建议适时进行追肥和灌溉。',
          image: 'https://ai-public.mastergo.com/ai/img_res/22c41fd68d91139f9b35c8d8bc65e8c0.jpg',
          riskLevel: 'low'
        }
      ],
      feedback: {
        type: '',
        content: ''
      },
      feedbackOptions: [
        { label: '系统建议', value: 'system' },
        { label: '数据问题', value: 'data' },
        { label: '其他', value: 'other' }
      ]
    };
  },
  computed: {
    getCropAlertTitle() {
      const titles = {
        goji: '高风险预警',
        grape: '注意事项',
        corn: '适宜生长'
      };
      return titles[this.selectedCrop] || '';
    },
    getCropAlertMessage() {
      const messages = {
        goji: '当前气温偏低，预计未来3天将出现霜冻天气，建议及时采取防寒措施。',
        grape: '近期降水偏多，葡萄园需注意排涝防渍，同时注意防范病害发生。',
        corn: '目前气温和降水条件适宜玉米生长，建议按照常规种植方案进行管理。'
      };
      return messages[this.selectedCrop] || '';
    },
    alertClass() {
      const classes = {
        goji: 'bg-red-50 text-red-700',
        grape: 'bg-yellow-50 text-yellow-700',
        corn: 'bg-green-50 text-green-700'
      };
      return classes[this.selectedCrop] || '';
    }
  },
  methods: {
    toggleCropSelect() {
      this.showCropSelect = !this.showCropSelect;
    },
    toggleCropTypeSelect() {
      this.showCropTypeSelect = !this.showCropTypeSelect;
    },
    toggleFeedbackSelect() {
      this.showFeedbackSelect = !this.showFeedbackSelect;
    },
    selectCrop(value) {
      this.selectedCrop = value;
      this.showCropSelect = false;
    },
    selectCropType(value) {
      this.cropType = value;
      this.showCropTypeSelect = false;
    },
    selectFeedbackType(value) {
      this.feedback.type = value;
      this.showFeedbackSelect = false;
    },
    getCropLabel(value) {
      const crop = this.cropTypes.find(c => c.value === value);
      return crop ? crop.label : '';
    },
    getFeedbackLabel(value) {
      const option = this.feedbackOptions.find(o => o.value === value);
      return option ? option.label : '';
    },
    getRiskLevelClass(level) {
      const classes = {
        low: 'bg-green-500',
        medium: 'bg-yellow-500',
        high: 'bg-red-500'
      };
      return classes[level] || '';
    },
    getRiskLevelText(level) {
      const texts = {
        low: '低风险',
        medium: '中度风险',
        high: '高风险'
      };
      return texts[level] || '';
    },
    submitFeedback() {
      if (!this.feedback.type || !this.feedback.content) {
        alert('请完整填写反馈信息');
        return;
      }
      alert('反馈提交成功');
      this.feedback = {
        type: '',
        content: ''
      };
    },
    initCharts() {
      if (this.$refs.plantingMapChart && this.$refs.riskMapChart && this.$refs.weatherTrendChart) {
        const plantingMap = this.$echarts.init(this.$refs.plantingMapChart);
        const riskMap = this.$echarts.init(this.$refs.riskMapChart);
        const weatherTrend = this.$echarts.init(this.$refs.weatherTrendChart);

        const plantingMapOption = {
          animation: false,
          title: {
            text: '宁夏主要特色作物种植区域'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b}: {c}'
          },
          visualMap: {
            min: 0,
            max: 100,
            text: ['种植密度高', '种植密度低'],
            calculable: true,
            inRange: {
              color: ['#e0f3db', '#43a2ca', '#0868ac']
            }
          },
          series: [{
            name: '宁夏',
            type: 'map',
            map: 'ningxia',
            label: {
              show: true,
              fontSize: 14
            },
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

        const riskMapOption = {
          animation: false,
          title: {
            text: '区域风险分布'
          },
          tooltip: {
            trigger: 'item'
          },
          series: [{
            type: 'pie',
            radius: '70%',
            data: [
              { value: 30, name: '低风险', itemStyle: { color: '#67C23A' } },
              { value: 40, name: '中风险', itemStyle: { color: '#E6A23C' } },
              { value: 20, name: '高风险', itemStyle: { color: '#F56C6C' } },
              { value: 10, name: '严重风险', itemStyle: { color: '#909399' } }
            ]
          }]
        };

        const weatherTrendOption = {
          animation: false,
          title: {
            text: '未来7天温度趋势'
          },
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

        plantingMap.setOption(plantingMapOption);
        riskMap.setOption(riskMapOption);
        weatherTrend.setOption(weatherTrendOption);

        window.addEventListener('resize', () => {
          plantingMap.resize();
          riskMap.resize();
          weatherTrend.resize();
        });
      }
    }
  },
  mounted() {
    this.initCharts();
    document.addEventListener('click', (e) => {
      const target = e.target;
      if (!target.closest('.relative')) {
        this.showCropSelect = false;
        this.showCropTypeSelect = false;
        this.showFeedbackSelect = false;
      }
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', () => {});
    document.removeEventListener('click', () => {});
  }
};
</script>

<style scoped>
.select-wrapper {
  position: relative;
  width: 100%;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

textarea:focus {
  outline: none;
}

input:focus {
  outline: none;
}
</style>


<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 特色作物信息 -->
    <div class="bg-white p-8 shadow-sm">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-2xl font-medium mb-6">宁夏特色作物基本信息</h2>
        <div class="grid grid-cols-3 gap-6">
          <div class="p-6 rounded-lg bg-gradient-to-br from-red-50 to-white border border-red-100">
            <div class="flex items-center mb-4">
              <img src="https://ai-public.mastergo.com/ai/img_res/26df82fbbfaa58a9cef9ee413f726253.jpg"
                   class="w-20 h-20 object-cover rounded-lg" alt="枸杞"/>
              <div class="ml-4">
                <h3 class="text-xl font-medium">枸杞</h3>
                <p class="text-gray-500 text-sm mt-1">主产区：中卫、吴忠</p>
              </div>
            </div>
            <div class="space-y-2">
              <p class="text-gray-600"><span class="font-medium">生长周期：</span>4 - 5 年</p>
              <p class="text-gray-600"><span class="font-medium">最适温度：</span>20 - 25℃</p>
              <p class="text-gray-600"><span class="font-medium">易发灾害：</span>干旱、霜冻</p>
            </div>
          </div>
          <div class="p-6 rounded-lg bg-gradient-to-br from-purple-50 to-white border border-purple-100">
            <div class="flex items-center mb-4">
              <img src="https://ai-public.mastergo.com/ai/img_res/7d5efdce325c3208ee0d9e7c95ec6efb.jpg"
                   class="w-20 h-20 object-cover rounded-lg" alt="葡萄"/>
              <div class="ml-4">
                <h3 class="text-xl font-medium">酿酒葡萄</h3>
                <p class="text-gray-500 text-sm mt-1">主产区：贺兰山东麓</p>
              </div>
            </div>
            <div class="space-y-2">
              <p class="text-gray-600"><span class="font-medium">生长周期：</span>20 - 30 年</p>
              <p class="text-gray-600"><span class="font-medium">最适温度：</span>25 - 30℃</p>
              <p class="text-gray-600"><span class="font-medium">易发灾害：</span>冰雹、病虫害</p>
            </div>
          </div>
          <div class="p-6 rounded-lg bg-gradient-to-br from-green-50 to-white border border-green-100">
            <div class="flex items-center mb-4">
              <img src="https://ai-public.mastergo.com/ai/img_res/0724a49586918dae9dfb4a9017743a52.jpg"
                   class="w-20 h-20 object-cover rounded-lg" alt="甘草"/>
              <div class="ml-4">
                <h3 class="text-xl font-medium">甘草</h3>
                <p class="text-gray-500 text-sm mt-1">主产区：固原、中卫</p>
              </div>
            </div>
            <div class="space-y-2">
              <p class="text-gray-600"><span class="font-medium">生长周期：</span>3 - 4 年</p>
              <p class="text-gray-600"><span class="font-medium">最适温度：</span>15 - 20℃</p>
              <p class="text-gray-600"><span class="font-medium">易发灾害：</span>涝灾、病虫害</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 气象灾害防治指南 -->
    <div class="bg-gray-50 p-8">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-2xl font-medium mb-6">气象灾害防治指南</h2>
        <div class="grid grid-cols-4 gap-6">
          <div class="p-6 rounded-lg bg-white shadow-sm">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-blue-100 mb-4">
              <i class="fas fa-cloud-rain text-xl text-blue-600"></i>
            </div>
            <h3 class="text-lg font-medium mb-3">暴雨灾害</h3>
            <ul class="space-y-2 text-gray-600 text-sm">
              <li>• 加强排水设施维护</li>
              <li>• 适时调整灌溉计划</li>
              <li>• 注意病虫害防治</li>
              <li>• 加固作物支架</li>
            </ul>
          </div>
          <div class="p-6 rounded-lg bg-white shadow-sm">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-red-100 mb-4">
              <i class="fas fa-temperature-high text-xl text-red-600"></i>
            </div>
            <h3 class="text-lg font-medium mb-3">高温灾害</h3>
            <ul class="space-y-2 text-gray-600 text-sm">
              <li>• 采用遮阳网防护</li>
              <li>• 增加灌溉频次</li>
              <li>• 喷施叶面肥</li>
              <li>• 控制棚室温度</li>
            </ul>
          </div>
          <div class="p-6 rounded-lg bg-white shadow-sm">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-yellow-100 mb-4">
              <i class="fas fa-wind text-xl text-yellow-600"></i>
            </div>
            <h3 class="text-lg font-medium mb-3">大风灾害</h3>
            <ul class="space-y-2 text-gray-600 text-sm">
              <li>• 加固大棚设施</li>
              <li>• 及时采收成熟果实</li>
              <li>• 扎牢支架</li>
              <li>• 准备防风网</li>
            </ul>
          </div>
          <div class="p-6 rounded-lg bg-white shadow-sm">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-indigo-100 mb-4">
              <i class="fas fa-snowflake text-xl text-indigo-600"></i>
            </div>
            <h3 class="text-lg font-medium mb-3">霜冻灾害</h3>
            <ul class="space-y-2 text-gray-600 text-sm">
              <li>• 采用防霜设施</li>
              <li>• 喷施防冻剂</li>
              <li>• 调整种植时间</li>
              <li>• 做好温度监测</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm h-16 fixed w-full top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
        <h1 class="text-xl font-medium text-gray-800">宁夏特色作物分布与灾害监测</h1>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input type="text" placeholder="搜索区域或作物" class="pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-500">
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"></i>
          </div>
          <button class="!rounded-button flex items-center px-4 py-2 bg-blue-600 text-white text-sm whitespace-nowrap">
            <i class="fas fa-filter mr-2"></i>筛选
          </button>
        </div>
      </div>
    </header>
    <!-- 主要内容区 -->
    <main class="pt-16 pb-8">
      <div class="max-w-7xl mx-auto px-4 mt-8">
        <!-- 灾害预警区域 -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-medium">灾害预警信息</h2>
            <div class="flex items-center space-x-2">
              <button class="!rounded-button px-3 py-1.5 border border-gray-200 text-sm whitespace-nowrap">
                最近一周
                <i class="fas fa-chevron-down ml-2"></i>
              </button>
            </div>
          </div>
          <div class="relative">
            <el-carousel :interval="3000" arrow="always" :loop="true" height="180px">
              <el-carousel-item v-for="(warning, index) in warningList" :key="index">
                <div :class="['p-4 rounded-lg', warning.bgColor]">
                  <div class="flex items-start">
                    <div :class="['w-10 h-10 rounded-full flex items-center justify-center', warning.iconBg]">
                      <i :class="['fas', warning.icon,  warning.iconColor]"></i>
                    </div>
                    <div class="ml-3 flex-1">
                      <div class="flex items-center">
                        <span :class="['px-2 py-0.5 rounded text-xs', warning.levelBg]">{{  warning.level  }}</span>
                        <span class="ml-2 text-sm text-gray-500">{{ warning.time  }}</span>
                      </div>
                      <h4 class="font-medium mt-2">{{ warning.title  }}</h4>
                      <p class="text-sm text-gray-600 mt-1">{{ warning.description  }}</p>
                      <div class="mt-3">
                        <span class="text-sm text-gray-500">影响作物：</span>
                        <span class="text-sm text-gray-800">{{ warning.crops  }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import * as echarts from 'echarts';
// 引入ningxia地图数据
const ningxiaJson = {
  type: 'FeatureCollection',
  features: []
};

export default {
  data() {
    return {
      warningList: [
        {
          icon: 'fa-cloud-rain',
          iconColor: 'text-blue-100',
          iconBg: 'bg-blue-600',
          bgColor: 'bg-blue-50',
          level: '蓝色预警',
          levelBg: 'bg-blue-600 text-white',
          time: '2024-01-15 08:00',
          title: '暴雨预警',
          description: '预计未来24小时内，中卫市南部地区将出现强降雨天气',
          crops: '枸杞、葡萄'
        },
        {
          icon: 'fa-temperature-high',
          iconColor: 'text-red-100',
          iconBg: 'bg-red-600',
          bgColor: 'bg-red-50',
          level: '红色预警',
          levelBg: 'bg-red-600 text-white',
          time: '2024-01-15 10:00',
          title: '高温预警',
          description: '银川市未来三天最高气温将达到38℃以上',
          crops: '硒砂瓜、甘草'
        },
        {
          icon: 'fa-wind',
          iconColor: 'text-yellow-100',
          iconBg: 'bg-yellow-600',
          bgColor: 'bg-yellow-50',
          level: '黄色预警',
          levelBg: 'bg-yellow-600 text-white',
          time: '2024-01-15 09:00',
          title: '大风预警',
          description: '吴忠市局部地区将出现8级以上大风',
          crops: '中宁枣、枸杞'
        }
      ]
    };
  },
  methods: {

  }
};
</script>

<style scoped>
/* 轮播基础样式 */
.el-carousel {
  @apply mb-4;
}



.el-carousel__item:nth-child(n) {
  background-color: #d3dce6;
}
</style>

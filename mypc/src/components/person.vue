<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航区 -->
    <Header class="bg-white shadow-sm h-16 sticky w-full top-0 z-50">

    </Header>
    <!-- 主体内容区 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 用户基本信息 -->
      <div class="bg-white rounded-lg p-6 mb-6 shadow-sm">
        <h2 class="text-lg font-semibold mb-4 flex items-center">
          <i class="fas fa-user text-green-600 mr-2"></i>
          基本信息
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="flex items-center">
            <img class="w-16 h-16 rounded-full border-2 border-gray-200"
                 src="/static/image/logo@2x.png" alt="用户头像">
            <div class="ml-4">
              <h3 class="text-lg font-medium">{{ userInfo.username }}</h3>
              <p class="text-gray-500 text-sm">普通用户</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-gray-500 text-sm">用户名</label>
              <p class="font-medium">{{ userInfo.username }}</p>
            </div>
            <div>
              <label class="text-gray-500 text-sm">手机号</label>
              <p class="font-medium">{{ userInfo.phone || '未绑定' }}</p>
            </div>
            <div>
              <label class="text-gray-500 text-sm">注册时间</label>
              <p class="font-medium">{{ userInfo.registerDate }}</p>
            </div>
            <div>
              <label class="text-gray-500 text-sm">上次登录</label>
              <p class="font-medium">{{ userInfo.lastLogin }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 关注区域 -->
      <div class="bg-white rounded-lg p-6 mb-6 shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold flex items-center">
            <i class="fas fa-map-marker-alt text-green-600 mr-2"></i>
            关注区域
          </h2>
          <span class="text-sm text-gray-500">已选择 {{ selectedAreas.length }}/5</span>
        </div>
        <div class="grid grid-cols-3 gap-3">
          <div v-for="(select, index) in areaSelects" :key="index" class="w-full">
            <select v-model="selectedAreas[index]" class="w-full border border-gray-300 rounded-md p-2 text-sm">
              <option value="">{{ select.placeholder }}</option>
              <option v-for="option in select.options" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
        </div>
        <div class="mt-4 flex flex-wrap gap-2">
          <div v-for="(area, index) in selectedAreaTags" :key="index"
               class="!rounded-button whitespace-nowrap bg-green-50 text-green-700 px-3 py-1 text-sm flex items-center">
            {{ area }}
            <i class="fas fa-times ml-2 cursor-pointer" @click="removeArea(index)"></i>
          </div>
        </div>
      </div>
      <!-- 作物类型 -->
      <div class="bg-white rounded-lg p-6 mb-6 shadow-sm">
        <h2 class="text-lg font-semibold mb-4 flex items-center">
          <i class="fas fa-seedling text-green-600 mr-2"></i>
          作物类型
        </h2>
        <div class="grid grid-cols-3 gap-3">
          <div v-for="crop in crops" :key="crop.name"
               :class="{'bg-green-50 border-green-600': crop.selected}"
               class="border rounded-lg p-4 cursor-pointer hover:border-green-600 transition-colors"
               @click="toggleCrop(crop)">
            <div class="flex items-center">
              <img :src="crop.image" class="w-12 h-12 object-cover rounded-lg" :alt="crop.name">
              <span class="ml-3 text-sm">{{ crop.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 预览确认区 -->
      <div class="bg-green-50 rounded-lg p-6 mb-6">
        <h3 class="font-semibold mb-2">订阅预览</h3>
        <p class="text-gray-600 mb-4">您将收到：宁夏银川市的枸杞、玉米中度及以上预警，通过短信+微信通知</p>
        <div class="flex justify-end space-x-4">
          <button class="!rounded-button whitespace-nowrap px-6 py-2 border border-gray-300 hover:bg-gray-50">
            重置
          </button>
          <button class="!rounded-button whitespace-nowrap px-6 py-2 bg-green-600 text-white hover:bg-green-700">
            保存订阅
          </button>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
import Footer from "./common/Footer.vue";
import Header from "./common/Header.vue"
export default {
  components: {Footer, Header},
  data() {
    return {
      userInfo: {
        username: '张三',
        phone: '138****8888',
        registerDate: '2023-05-15',
        lastLogin: '2024-01-20 14:30'
      },
      selectedAreas: ['', '', '', ''],
      selectedAreaTags: ['宁夏银川市兴庆区', '宁夏中卫市沙坡头区'],
      areaSelects: [
        {
          placeholder: '选择省份',
          options: ['宁夏回族自治区']
        },
        {
          placeholder: '选择城市',
          options: ['银川市', '石嘴山市', '吴忠市', '固原市', '中卫市']
        },
        {
          placeholder: '选择区县',
          options: ['兴庆区', '金凤区', '西夏区', '贺兰县']
        },
      ],
      crops: [
        {
          name: '枸杞',
          selected: true,
          image: 'https://ai-public.mastergo.com/ai/img_res/c00369851c4fd793d1b22c1a91525c5e.jpg'
        },
        {
          name: '小麦',
          selected: false,
          image: 'https://ai-public.mastergo.com/ai/img_res/1f10c17cf7e568fc689437e723dcc6e5.jpg'
        },
        {
          name: '葡萄',
          selected: false,
          image: 'https://ai-public.mastergo.com/ai/img_res/a21ed9725da973eb4cd0924a3c5c4f28.jpg'
        }
      ],
      notifyMethods: [
        {
          type: 'wechat',
          name: '微信通知',
          icon: 'fab fa-weixin',
          selected: true
        },
        {
          type: 'app',
          name: '短信通知',
          icon: 'fas fa-mobile-alt',
          selected: false
        }
      ],
      selectedLevel: 2
    };
  },
  methods: {
    removeArea(index) {
      this.selectedAreaTags.splice(index, 1);
    },
    toggleCrop(crop) {
      crop.selected = !crop.selected;
    },
    toggleNotify(method) {
      method.selected = !method.selected;
    }
  }
};
</script>
<style scoped>
input[type="range"] {
  -webkit-appearance: none;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  background-image: linear-gradient(#16a34a, #16a34a);
  background-repeat: no-repeat;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #16a34a;
  cursor: pointer;
  box-shadow: 0 0 2px 0 #555;
}

input[type="range"]::-webkit-slider-runnable-track {
  -webkit-appearance: none;
  box-shadow: none;
  border: none;
  background: transparent;
}

select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  appearance: none;
}

select:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 1px #16a34a;
}
</style>

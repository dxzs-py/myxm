// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings"
Vue.prototype.$settings = settings;  // 设置个人配置的全局变量

Vue.config.productionTip = false



// element-ui配置
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 调用插件
Vue.use(ElementUI);

// 导入echarts
import * as echarts from 'echarts'; // ✅ 完整导入
import 'echarts-gl'; // ✅ 确保地理扩展包正确加载

// 修改地图数据加载方式（删除原china.js的引入）  // 引入中国基础地图数据
import chinaJson from './assets/map/json/china.json';
echarts.registerMap('china', chinaJson);

import ningxiaJson from './assets/map/json/province/ningxia.json'; // 宁夏地图JSON数据路径
echarts.registerMap('ningxia', ningxiaJson);  // 注册宁夏地图
Vue.prototype.$echarts = echarts;

// 导入axios
import axios from "axios"
axios.defaults.withCredentials = false; // false表示阻止ajax请求携带cookie
Vue.prototype.$axios = axios; // 把对象挂载vue中

// 导入gt极验
import '../static/js/gt.js'

// 导入css初始化样式
import "../static/css/reset.css";
import "tailwindcss/tailwind.css";
import '@fortawesome/fontawesome-free/css/all.css';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

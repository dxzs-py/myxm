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
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts;
import 'echarts-gl'; // 引入地理扩展包
import './assets/map/js/china.js';   // 引入中国基础地图数据
import ningxiaJson from './assets/map/json/province/ningxia.json'; // 宁夏地图JSON数据路径
// 注册宁夏地图
echarts.registerMap('ningxia', ningxiaJson);
Vue.use(echarts)


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

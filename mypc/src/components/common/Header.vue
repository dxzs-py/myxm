<template>
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

<div v-if="token" class="flex items-center space-x-3">
<div class="login-box login-box1 full-left" style="padding-bottom: 10px">
            <router-link to="">用户中心</router-link>
            <el-menu class="member el-menu-demo" mode="horizontal">
              <el-submenu index="2" popper-class="custom-user-menu">
                <template ><img style="width: 40px;height: 40px " src="/static/image/logo@2x.png" alt="">
                  <span class="shop-cart-total" style="padding-left: 10px">
                    {{ username }}
                  </span>
                </template>
                <el-menu-item index="2-1">我的账户</el-menu-item>
                <el-menu-item index="2-2">我的订单</el-menu-item>
                <el-menu-item index="2-3">我的优惠卷</el-menu-item>
                <span @click="logoutHander"><el-menu-item index="2-3">退出登录</el-menu-item></span>
              </el-submenu>
            </el-menu>
</div>
</div>

<div v-else class="flex items-center space-x-4">
  <button class="bg-green-600 text-white px-4 py-2 !rounded-button whitespace-nowrap hover:bg-green-700">
    <router-link to="/user/login/">登录</router-link>
  </button>
  <button class="bg-gray-100 px-4 py-2 !rounded-button whitespace-nowrap hover:bg-gray-200">
    <router-link to="/user/rgt/">注册</router-link>
  </button>
</div>

</div>
</div>
</header>
</template>


<script>
export default {
  name:"Header",
  data(){
    return{
      token:"",
      searchQuery: '',
      // nav_list:[],
      username:""
    }
  },
  created() {
    this.check_user_login();
  },
  methods:{
    check_user_login(){
      // 获取用户登录状态
      this.token = localStorage.user_token || sessionStorage.user_token;
      this.username = localStorage.user_name || sessionStorage.user_name; // 获取 username
      return this.token;
    },
    logoutHander() {
      // 退出登录
      localStorage.removeItem('user_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_name');
      sessionStorage.removeItem('user_token');
      sessionStorage.removeItem('user_id');
      sessionStorage.removeItem('user_name');
      this.check_user_login();
    }
  }
}


</script>

<style scoped>



.member {
  display: inline-block;
  height: 34px;
  margin-left: 20px;
}

.member img {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
}

.member img:hover {
  border: 1px solid yellow;
}


/* 修改全局样式块 */
.custom-user-menu .el-menu-item {
  padding: 5px 10px !important;
  font-size: 14px !important; /* 补充字体统一 */
}

.custom-user-menu .el-menu-item:hover {
  background-color: #f5f7fa !important; /* 增加背景色 */
  color: #409EFF !important;
}

</style>

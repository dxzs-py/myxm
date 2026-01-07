<template>
  <div>
    <header class="bg-white shadow-sm relative">
      <!-- 时间显示移动到右侧 -->
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <!-- 左侧Logo区 -->
        <div class="flex items-center space-x-3 flex-1">
          <i class="fas fa-seedling text-2xl text-green-500 transform hover:rotate-12 transition-all"></i>
          <h1 class="text-xl font-medium text-gray-800">宁夏特色作物气象灾害风险预测与预警系统</h1>
        </div>

        <!-- 中间导航区 -->
        <nav class="flex space-x-4 mx-8 flex-1 justify-center">
          <router-link
            to="home"
            class="px-3 py-2 rounded-md transition-colors duration-200 text-gray-600 hover:text-green-600 hover:bg-green-50 ">
            首页
          </router-link>
          <router-link
            to="klg"
            class="px-3 py-2 rounded-md transition-colors duration-200 text-gray-600 hover:text-green-600 hover:bg-green-50">
            种植指南
          </router-link>
        </nav>

        <!-- 右侧功能区 -->
        <div class="flex items-center space-x-6 flex-1 justify-end">
          <!-- 搜索框 -->
          <div class="relative w-72 mr-4">
            <input
              v-model="searchQuery"
              class="w-full h-10 pl-10 pr-4 rounded-lg border border-gray-200 bg-gray-50 focus:outline-none
                 focus:ring-2 focus:ring-green-500 focus:bg-white transition-all"
              placeholder="搜索作物或地区"
            />
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2
         text-gray-400 leading-[0] transform"></i>
          </div>

          <!-- 时间显示 -->
          <div class="time-box bg-gray-800 text-white px-3 py-1.5 rounded-lg shadow-md">
            <div class="text-lg font-mono leading-tight">{{ formattedTime }}</div>
            <div class="text-sm opacity-80 tracking-tight">{{ formattedDate }}</div>
          </div>

          <!-- 用户操作区 -->
          <div v-if="token" class="flex items-center space-x-3" style="width: 130px">
            <router-link
              to="person"
              class="px-3 py-2 rounded-md transition-colors duration-200 text-gray-600 hover:text-green-600 hover:bg-green-50">
              用户中心
            </router-link>
            <el-menu class="member el-menu-demo relative" mode="horizontal" style="padding-bottom: 55px">
              <el-submenu index="2" popper-class="custom-user-menu">
                <template>
                  <div class="flex items-center">
                    <img class="w-10 h-10 rounded-full border-2 border-white"
                         src="/static/image/logo@2x.png" alt="用户头像">
                    <span class="ml-2 text-gray-700 font-medium">{{ username }}</span>
                  </div>
                </template>
                <el-menu-item index="2-1">我的账户</el-menu-item>
                <el-menu-item index="2-2">我的订单</el-menu-item>
                <el-menu-item index="2-3">我的优惠券</el-menu-item>
                <el-menu-item index="2-4" @click="logoutHander">退出登录</el-menu-item>
              </el-submenu>
            </el-menu>
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
    <router-view></router-view>
    <Footer/>
  </div>
</template>


<script>
import Footer from "./Footer.vue";

export default {
  name: "Header",
  components: {
    Footer
  },
  data() {
    return {
      token: "",
      searchQuery: '',
      username: "",
      currentTime: new Date(),
    }
  },
  computed: {
    formattedTime() {
      return this.currentTime.toLocaleTimeString('zh-CN', {hour12: false})
    },
    formattedDate() {
      return this.currentTime.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).replace(/\//g, '-')
    }
  },
  created() {
    this.getuserInfo();
  },
  methods: {
    getuserInfo() {
      // 获取用户信息
      let token = this.check_user_login();
      if (token) {
        this.$axios.get(`${this.$settings.HOST}user/self/`, {
          headers: {
            "Authorization": `Bearer ${token}`
          },
        }).then(response => {
          this.$store.commit('change_selectedArea', response.data[0].city);
        }).catch(error => {
          this.$message.error("未登录或者登录已过期");
        })
      }
    },
    check_user_login() {
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
  },
  mounted() {
    this.timer = setInterval(() => {
      this.currentTime = new Date()
    }, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
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


.time-box {
  min-width: 100px;
  backdrop-filter: blur(4px);
  background: rgba(31, 41, 31, 0.9);
}

.member :deep(.el-submenu__title) {
  padding: 0 !important;
  border-bottom: none !important;
}

.custom-user-menu {
  @apply shadow-lg rounded-lg overflow-hidden;

  .el-menu-item {
    @apply px-4 py-3 text-sm text-gray-600 hover:bg-green-50 hover:text-green-600 transition-colors;
  }
}

/* 统一按钮过渡效果 */
button, .el-menu-item {
  @apply transition-all duration-200;
}

a.router-link-active {
  background-color: #10B981;
}

a:hover {
  background-color: #555;
}
</style>

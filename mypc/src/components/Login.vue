<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->

```vue
<template>
  <div class="min-h-screen relative">
    <!-- 背景图 -->
    <div class="absolute inset-0 z-0">
      <img
        :src="'https://ai-public.mastergo.com/ai/img_res/71bf7e3f1a65d0107e7f248cd00ed74b.jpg'"
        class="w-full h-full object-cover object-center"
        alt="Background"
      />
      <div class="absolute inset-0 bg-black/30"></div>
    </div>

    <!-- 主容器 -->
    <div class="container mx-auto px-4 min-h-screen relative z-10 flex items-center justify-center">
      <!-- Logo -->
      <div class="absolute top-8 -translate-x-1/2">
        <div class="flex items-center gap-3">
          <i class="fas fa-leaf text-4xl text-green-500"></i>
          <span class="text-3xl font-bold text-purple-300">宁夏特色作物气象灾害风险识别与预警系统</span>
        </div>
      </div>

      <!-- 登录/注册卡片 -->
      <div class="w-[420px] bg-white/95 backdrop-blur rounded-xl p-8 shadow-2xl">
        <!-- 切换标签 -->
        <div class="flex gap-8 mb-8">
          <button
            :class="[
              'text-xl font-medium pb-2 px-2',
              isLogin ? 'text-green-600 border-b-2 border-green-600' : 'text-gray-400'
            ]"
            @click="isLogin = true"
          >
            登录
          </button>
          <button
            :class="[
              'text-xl font-medium pb-2 px-2',
              !isLogin ? 'text-green-600 border-b-2 border-green-600' : 'text-gray-400'
            ]"
            @click="isLogin = false"
          >
            注册
          </button>
        </div>

        <!-- 登录表单 -->
        <div v-if="isLogin">
          <div class="space-y-6">
            <div>
              <div class="relative">
                <i class="fas fa-user absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  type="text"
                  class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请输入手机号/用户名"
                  v-model="loginForm.username"
                />
              </div>
            </div>
            <div>
              <div class="relative">
                <i class="fas fa-lock absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请输入密码"
                  v-model="loginForm.password"
                />
                <button
                  class="absolute right-3 top-1/3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  @click="showPassword = !showPassword"
                >
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="w-4 h-4 accent-green-600" v-model="loginForm.remember"/>
                <span class="text-sm text-gray-600">记住密码</span>
              </label>
              <a href="#" class="text-sm text-green-600 hover:text-green-700">忘记密码？</a>
            </div>
            <button
              class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors !rounded-button whitespace-nowrap">
              登 录
            </button>
          </div>
        </div>

        <!-- 注册表单 -->
        <div v-else>
          <div class="space-y-6">
            <div>
              <div class="relative">
                <i class="fas fa-mobile-alt absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  type="text"
                  class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请输入手机号"
                  v-model="registerForm.phone"
                />
              </div>
            </div>
            <div>
              <div class="relative">
                <i class="fas fa-shield-alt absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  type="text"
                  class="w-full pl-10 pr-32 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请输入验证码"
                  v-model="registerForm.code"
                />
                <button
                  class="absolute right-2 -translate-y-1/2 px-4 py-1.5 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition-colors !rounded-button whitespace-nowrap"
                  style="top:7px"
                >
                  获取验证码
                </button>
              </div>
            </div>
            <div>
              <div class="relative">
                <i class="fas fa-lock absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请设置密码"
                  v-model="registerForm.password"
                />
                <button
                  class="absolute right-3 top-1/3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  @click="showPassword = !showPassword"
                >
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
            <div>
              <div class="relative">
                <i class="fas fa-lock absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请确认密码"
                  v-model="registerForm.confirmPassword"
                />
              </div>
            </div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="w-4 h-4 accent-green-600" v-model="registerForm.agreement"/>
              <span class="text-sm text-gray-600">
                我已阅读并同意
                <a href="#" class="text-green-600 hover:text-green-700">《用户协议》</a>
                和
                <a href="#" class="text-green-600 hover:text-green-700">《隐私政策》</a>
              </span>
            </label>
            <button
              class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors !rounded-button whitespace-nowrap">
              注 册
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLogin: true,
      showPassword: false,
      loginForm: {
        username: '',
        password: '',
        remember: false
      },
      registerForm: {
        phone: '',
        code: '',
        password: '',
        confirmPassword: '',
        agreement: false
      }
    }
  },
  mounted() {
    // 获取登录状态
    this.isLogin = this.$route.query.isLogin === 'true'
  },
}
</script>

<style scoped>

</style>


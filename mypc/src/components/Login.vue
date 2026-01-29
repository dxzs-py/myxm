<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->

<template>
  <div class="min-h-screen relative">
    <!-- 背景图 -->
    <div class="absolute inset-0 z-0">
      <img
        src="/static/image/bj.jpg"
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
              'text-green-600 border-b-2 border-green-600'
            ]"
          >
            登录
          </button>
          <button
            :class="[
              'text-xl font-medium pb-2 px-2',
              'text-gray-400'
            ]"
            @click="goToRegister">
            注册
          </button>
        </div>

        <!-- 登录表单 -->
        <div>
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
                <i class="fas fa-lock absolute left-3 top-1/3 -translate-y-1/2 text-gray-400 " style="padding-top: 71px; z-index: 1001"></i>

                <button
                  class="absolute right-3 top-1/3 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  @click="showPassword = !showPassword" style="z-index: 1001"
                >
                  <i :class="[showPassword ? 'fas fa-eye-slash' : 'fas fa-eye',]" style="padding-top: 71px"></i>
                </button>
              </div>
            </div>
            <div>
              <div class="relative">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full pl-10 pr-12 py-3 border border-gray-200  rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                  placeholder="请输入密码"
                  v-model="loginForm.password"
                />

                 <div id="geetest1"></div>
              </div>
            </div>
            <div class="flex items-center justify-between mt-6 relative">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="w-4 h-4 accent-green-600" v-model="loginForm.remember"/>
                <span class="text-sm text-gray-600">记住密码</span>
              </label>
              <a href="#"
                class="text-sm text-green-600 hover:text-green-700" style="position: absolute;  right: 0;"
                >忘记密码？</a>
            </div>
            <button
              @click="get_geetest_captcha"
              class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors !rounded-button whitespace-nowrap">
              登 录
            </button>
          </div>
        </div>


      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      showPassword: false,
      loginForm: {
        username: '',
        password: '',
        remember: false,
      },
    }
  },
  methods: {
    goToRegister() {
      this.$router.push('/user/rgt');
    },
    loginHander() {
      this.$axios.post(`${this.$settings.HOST}/user/login/token/`, {
        username: this.loginForm.username,
        password: this.loginForm.password,
      }).then(res => {
        // 保存登录状态
        this.$auth.saveLoginStatus(res.data.access, res.data.id, res.data.username, this.loginForm.remember);
        // 页面跳转 - 检查是否有保存的跳转路径
        let self = this;
        this.$alert("登陆成功", "欢迎回来", {}, {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'success'
        }).then(() => {
          // 处理登录后跳转
          this.$auth.handleLoginRedirect(this);
        });
      }).catch(err => {
        const h = this.$createElement;
        this.$message({
          message: h('p', null, [
            h('span', '登录失败，请检查用户名或密码是否正确！'),
            h('i', {style: 'color: red'},)
          ]),
          type: 'error',
          duration: 1000
        });
      })
    },
    handlerPopup(captchaObj) {
      // 极验验证码的验证方法

      let self = this;
      // 成功时回调
      captchaObj.onSuccess(function () {
        var validate = captchaObj.getValidate();
        // 当用户拖动验证码成功后，发送请求到后台
        self.$axios.post(`${self.$settings.HOST}/user/captcha/`, {
          geetest_challenge: validate.geetest_challenge,
          geetest_validate: validate.geetest_validate,
          geetest_seccode: validate.geetest_seccode,
        }).then(response => {
          if (response.data.status) {
            // 验证码通过以后才发送账号和密码进行登录！
            self.loginHander();
          }
        }).catch(error => {
          console.log(error.response)
        })
      });
      // 将验证码加到id为geetest1的元素里
      document.getElementById('geetest1').innerHTML = ''; // 移除之前的验证码元素，避免因用户多次点击时，验证码重复加载
      captchaObj.appendTo("#geetest1");
      self.captchaObj = captchaObj;  // 存储验证码实例
      // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    },
    get_geetest_captcha() {
      // 获取验证码
      this.$axios.get(`${this.$settings.HOST}/user/captcha/`, {
        params: {
          username: this.loginForm.username,  // get传入参数要通过params传，不然参数不会传
        }
      }).then(response => {
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        let data = JSON.parse(response.data)  // 服务端返回的字符串，要转换为json
        console.log(data)
        initGeetest({  //initGeetest需要在main.js导包
          gt: data.gt,
          challenge: data.challenge,
          product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
          offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
          // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
        }, this.handlerPopup);
      }).catch(error => {
        const h = this.$createElement;
        this.$message({
          message: h('p', null, [
            h('span', {style: 'color: red'}, '对不起，账号未注册'),
            h('i', {style: 'color: teal'}, '请注册后登录')
          ])
        });
      });
    },
  },
}
</script>

<style scoped>

</style>

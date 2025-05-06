<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->

```vue
<template>
  <div class="min-h-screen relative">
    <!-- 背景图 -->
    <div class="absolute inset-0 z-0">
      <img
        :src="'/static/image/bj.jpg'"
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
               'text-gray-400'
            ]"
            @click="goToRegister"
          >
            登录
          </button>
          <button
            :class="[
              'text-xl font-medium pb-2 px-2',
               'text-green-600 border-b-2 border-green-600'
            ]"

          >
            注册
          </button>
        </div>


        <!-- 注册表单 -->

        <div class="space-y-6">
          <div>
            <div class="relative">
              <i class="fas fa-mobile-alt absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
              <input
                type="text"
                @blur="CheckMobile"
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                placeholder="请输入手机号"
                v-model="registerForm.mobile"
              />
            </div>
          </div>
          <div>
            <div class="relative sms-box">
              <i class="fas fa-shield-alt absolute left-3 top-1/3 -translate-y-1/2 text-gray-400"></i>
              <input
                type="text"
                class="w-full pl-10 pr-32 py-3 border border-gray-200 rounded-lg focus:border-green-500 outline-none transition-colors text-sm"
                placeholder="请输入验证码"
                v-model="registerForm.sms_code"
              />
              <button
                class="absolute right-2 -translate-y-1/2 px-4 py-1.5 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition-colors !rounded-button whitespace-nowrap"
                style="top:7px" @click="smsHandle"
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
          <button @click="registerHander"
            class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors !rounded-button whitespace-nowrap">
            注 册
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      showPassword: false,
      registerForm: {
        mobile: '',
        sms_code: "",
        password: '',
        confirmPassword: '',
        agreement: false,
        is_send_sms: false, // 发送短信的标记
      }
    }
  },
  methods: {
    goToRegister() {
      this.$router.push('/user/login')
    },
    CheckMobile() {
      this.$axios.get(`${this.$settings.HOST}/user/mobile/${this.registerForm.mobile}/`)
        .catch(error => {
          // 当网络完全中断时，error.response 可能为 undefined
          const response = error.response || {};//作用：确保 response 始终是对象
          // 等价于
          // let response;
          // if(error.response){
          //   response = error.response;
          // }else{
          //   response = {};
          // }
          let message = '请求异常，请检查网络';
          if (response.status) {
            message = {
              400: `手机号已被注册: ${response.data && response.data.message || ''}`,
              404: '手机号格式错误',
            }[response.status] || message;
          }
          // 手机号码的合法性(包括格式和是否已经注册)，通过@blur当用户离开（失去焦点）某个表单元素时触发指定的处理函数。
          this.$message.error(`错误提示：${message}`);
        })
    },

    registerHander() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.$message.error("两次密码不一致");
        return false;
      }
      // 用户注册
      this.$axios.post(`${this.$settings.HOST}/user/reg/`, {
        mobile: this.registerForm.mobile,
        password: this.registerForm.password,
        sms_code: this.registerForm.sms_code,
      }).then(res => {

        console.log(res.data);
        localStorage.removeItem('user_token');  // 为了避免登录状态被覆盖
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_name');
        sessionStorage.user_token = res.data.access;
        sessionStorage.user_id = res.data.id;
        sessionStorage.user_name = res.data.username;

        let self = this;
        this.$alert("注册成功", "欢迎成为我们的用户", {}, {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'success'
        }).then(() => {
          self.$router.push('/');  // 这里如果用this是alert对象，我们要重新回调到Vue
        });

      }).catch(error => {
        let data = error.response.data;
        let message = "";
        for (let key in data) {
          message = data[key][0];
        }  // 循环遍历所有错误信息，等价于下面代码
        // let message = " "
        // if(error.response.data.mobile){
        //   message = error.response.data.mobile[0];
        // }
        // if(error.response.data.password){
        //   message = error.response.data.password[0];
        // }
        // if(error.response.data.sms_code){
        //   message = error.response.data.sms_code[0];
        // }
        // if(error.response.data.non_field_errors){
        //   message = error.response.data.non_field_errors;
        // }
        this.$message.error(`对不起，注册失败！错误提示：${message}`)
      });
    },

    smsHandle() {
      // 发送短信
      // 1.检查手机格式
      if (!/1[3-9]\d{9}/.test(this.registerForm.mobile)) {
        this.$message.error("手机号码格式错误");
        return false;
      }
      // 2.判断手机号码是否60秒内发送过短信
      if (this.registerForm.is_send_sms) {
        this.$message.error("当前手机号已经在60秒内发送过短信，请不要频繁发送！");
        return false;
      }
      // 3.发送ajax
      this.$axios.get(`${this.$settings.HOST}/user/sms/${this.registerForm.mobile}/`).then(response => {
        console.log(response.data);
        this.registerForm.is_send_sms = true;
        let interval_time = 60;
        let timer = setInterval(() => {
          if (interval_time <= 1) {
            // 停止倒计时，允许用户发送短信
            clearInterval(timer);
            this.registerForm.is_send_sms = false; // 设置短信发送段的间隔状态为false，允许点击发送短信
          } else {
            interval_time--;
          }
        }, 1000);
        this.registerForm.is_send_sms = true;
      }).catch(error => {
        console.log(error.response.data)
      });
    },

  }
}
</script>

<style scoped>
.sms-box {
  position: relative;
}

</style>


<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="min-h-screen bg-gray-50">
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
                 :src="userInfo.avatar ? `${userInfo.avatar}` : '/static/image/logo@2x.png'" alt="用户头像">
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
              <p class="font-medium">{{ userInfo.mobile || '未绑定' }}</p>
            </div>
            <div>
              <label class="text-gray-500 text-sm">电子邮件地址</label>
              <p class="font-medium">{{ userInfo.email || '未绑定' }}</p>
            </div>
            <div>
              <label class="text-gray-500 text-sm">上次登录</label>
              <p class="font-medium">{{ userInfo.last_login | timeformat }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 关注区域 -->
      <!-- 关注区域和作物类型 -->
      <div class="bg-white rounded-lg p-6 mb-6 shadow-sm">
        <!-- 居中的标题 -->
        <div class="text-center mb-6">
          <h2
            class="text-lg font-semibold inline-flex items-center justify-center bg-green-100 text-green-700 px-3 py-1 rounded-full">
            <i class="fas fa-map-marker-alt text-green-600 mr-2"></i>
            关注区域和作物类型
          </h2>
        </div>

        <!-- 左右两列布局 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- 左侧：关注区域选择 -->
          <div>
            <h3 class="text-md font-medium mb-4 flex items-center">
              <i class="fas fa-map-marker-alt text-blue-500 mr-2"></i>
              选择关注区域
            </h3>

            <div class="flex flex-col items-start">
              <!-- 使用Element UI的级联选择器 -->
              <el-cascader
                v-model="selectedArea"
                :options="areaOptions"
                :props="defaultProps"
                @change="handleChange"
                placeholder="请选择省/市/区"
                clearable
                class="w-full mb-4"
              />

              <div v-if="selectedArea.length" class="mt-4 bg-gray-50 p-3 rounded-lg w-full">
                <p class="text-gray-700">选中结果：{{ selectedAreaLabels }}</p>
              </div>
            </div>
          </div>

          <!-- 右侧：作物类型选择 -->
          <div>
            <h3 class="text-md font-medium mb-4 flex items-center">
              <i class="fas fa-seedling text-green-600 mr-2"></i>
              选择作物类型
            </h3>

            <div class="grid grid-cols-2 gap-2">
              <div v-for="crop in crops" :key="crop.name"
                   :class="{'bg-green-50 border-green-600': crop.selected}"
                   class="border rounded-lg p-4 cursor-pointer hover:border-green-600 transition-colors"
                   @click="toggleCrop(crop)">
                <div class="flex flex-col items-center">
                  <img :src="crop.image" class="w-12 h-12 object-cover rounded-lg mb-2" :alt="crop.name">
                  <span class="text-sm">{{ crop.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- 预览确认区 -->
      <div class="bg-green-50 rounded-lg p-6 mb-6">
        <h3 class="font-semibold mb-2">订阅预览</h3>
        <p class="text-gray-600 mb-4">您将收到：{{ selectedAreaLabels }}的{{ this.$store.state.selectedCropClass.join('、') }}中度及以上预警，通过短信</p>
        <div class="flex justify-end space-x-4">
          <button @click="reset()"
                  class="!rounded-button whitespace-nowrap px-6 py-2 border border-gray-300 hover:bg-gray-50">
            重置
          </button>
          <button @click="save()"
                  class="!rounded-button whitespace-nowrap px-6 py-2 bg-green-600 text-white hover:bg-green-700">
            保存修改
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  data() {
    return {
      userInfo: {
        username: '张三',
        mobile: '138****8888',
        email: '3309201506@qq.com',
        last_login: '2024-01-20 14:30',
        avatar: null,
        province_name: "宁夏回族自治区",
        county_name: "银川市",
        crops_interest: [],
        province_city: "宁夏回族自治区"
      },
      selectedArea: [],
      selectedArea0: [],
      areaOptions: [
        {
          id: '1',
          name: '宁夏回族自治区',
          children: [
            {
              id: '2',
              name: '银川市',
              children: [
                {id: '640105', name: '西夏区'},
                {id: '640121', name: '永宁县'},
                {id: '640122', name: '贺兰县'}
              ]
            },
            {
              id: '1',
              name: '石嘴山市',
              children: [
                {id: '640202', name: '大武口区'},
                {id: '640221', name: '惠农县'}
              ]
            }
          ]
        },
        {
          id: '2',
          name: '新疆维吾尔自治区',
          children: [
            {
              id: '6',
              name: '乌鲁木齐市',
              children: [
                {id: '650102', name: '独山子区'}
              ]
            }
          ]
        }
      ],
      defaultProps: {
        children: 'children',
        label: 'name',
        value: 'id'
      },
      selectedCrops: [],
      selectedCrops0: [],
      crops: [
        {
          name: '枸杞',
          value: 2,
          selected: true,
          image: 'http://www.mtl.cn:8000/media/crop_img/gq.jpg'
        },
        {
          name: '葡萄',
          value: 1,
          selected: false,
          image: 'http://www.mtl.cn:8000/media/crop_img/pt3.jpg'
        },
        {
          name: '冬小麦',
          value: 4,
          selected: false,
          image: 'http://www.mtl.cn:8000/media/crop_img/xm3.jpg'
        },
        {
          name: '春小麦',
          value: 3,
          selected: false,
          image: 'http://www.mtl.cn:8000/media/crop_img/xm.jpg'
        },
      ],

      selectedLevel: 2
    };
  },
  computed: {
    // 获取选中区域的标签名称
    selectedAreaLabels() {
      if (!this.selectedArea.length) return '';

      // 通过递归查找获取所有选中节点的名称
      const labels = [];
      let currentNode = this.areaOptions;

      this.selectedArea.forEach(value => {
        const node = currentNode.find(item => item.id === value);
        if (node) {
          labels.push(node.name);
          currentNode = node.children || [];
        }
      });

      return labels.join(' - ');
    }
  },
  filters: {
    timeformat(value) {
      let datetime = new Date(value);
      let Y = datetime.getFullYear(); // 年
      let m = datetime.getMonth() + 1;
      let d = datetime.getDate();
      let H = datetime.getHours();
      let M = datetime.getMinutes();
      let S = datetime.getSeconds();
      m = m < 10 ? '0' + m : m;
      d = d < 10 ? '0' + d : d;
      H = H < 10 ? '0' + H : H;
      M = M < 10 ? '0' + M : M;
      S = S < 10 ? '0' + S : S;
      return `${Y}-${m}-${d} ${H}:${M}`;
    }
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
          this.userInfo = response.data[0];
          this.selectedArea0 = [this.userInfo.province_id, this.userInfo.city_id, this.userInfo.county_id]
          this.selectedArea = this.selectedArea0.length === 3 ? this.selectedArea0 : [];
          // console.log(this.selectedArea0.length)
          this.selectedCrops0 = this.userInfo.crops_interest
          this.selectedCrops = this.selectedCrops0
          this.getCrops()
        }).catch(error => {
          this.$message.error("未登录或者登录已过期，请重新登陆");
          // 保存当前路径，以便登录后跳转回来
          localStorage.setItem('redirectAfterLogin', this.$route.fullPath);
          this.$router.push("/user/login");
        })
      }
    },
    check_user_login() {
      let token = localStorage.user_token || sessionStorage.user_token;
      if (!token) {
        let self = this;
        this.$confirm("对不起，您尚未登录！", "宁夏气象灾害风险识别预测预警系统", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // 保存当前路径，以便登录后跳转回来
          localStorage.setItem('redirectAfterLogin', this.$route.fullPath);
          self.$router.push("/user/login");
        }).catch(() => {
          // 用户点击取消，跳转到首页
          self.$router.push("/");
        });
        return false; // 阻止js继续往下执行
      }
      return token;
    },
    toggleCrop(crop) {
      crop.selected = !crop.selected;
      const selectedCrops = this.crops.filter(crop => crop.selected);
      this.selectedCrops = selectedCrops.map(crop => crop.value);
      // this.$message.success(`已${crop.selected ? '添加' : '删除'}作物：${crop.name}`);
    },
    getAreaOptions() {
      // 获取地区选项
      this.$axios.get(`${this.$settings.HOST}user/areas/hierarchy/`).then(response => {
        this.areaOptions = response.data;
      }).catch(error => {
        this.$message.error("获取地区选项失败");
      })
    },
    handleChange(value) {
      console.log('选中值变化:', value);
      // 这里可以添加其他业务逻辑
    },
    getCrops() {
      this.$axios.get(`${this.$settings.HOST}crop/cropClass/`).then(response => {
        this.crops = response.data['crops'];
        const selectedCropClass = []
        for (let i = 0; i < this.crops.length; i++) {
          if (this.userInfo.crops_interest.includes(this.crops[i].value)) {
            this.crops[i].selected = true;
            selectedCropClass.push(this.crops[i].name);
          }
        }
        this.$store.commit('change_selectedCropClass', selectedCropClass);
      }).catch(error => {
        this.$message.error("获取作物选项失败");
      })
    },
    reset() {
      // 创建selectedArea0的副本而不是直接引用
      this.selectedArea = this.selectedArea0 ? [...this.selectedArea0] : [];
      // 创建selectedCrops0的副本而不是直接引用
      this.selectedCrops = this.selectedCrops0 ? [...this.selectedCrops0] : [];
      /*this.crops.forEach(crop => {
        crop.selected = this.selectedCrops.includes(crop.value);
      });*/  // 这是我的写法，下面是优化的写法这种语法我不太清楚
      const selectedCropValues = new Set(this.selectedCrops);
      this.crops = this.crops.map(crop => ({
        ...crop,
        selected: selectedCropValues.has(crop.value)
      }));
      this.$message.success("已重置");
    },
    save() {
      // 使用 parseInt（更明确地指定基数为 10）
      let token = this.check_user_login();
      if (!token) return; // 未登录直接返回
      if (!this.selectedArea.length === 3) {
        this.$message.error("请选择地区");
        return;
      }
      const numericArea = this.selectedArea.map(id => parseInt(id, 10));
      this.$axios.post(`${this.$settings.HOST}user/self/`, {
        selectedArea: numericArea,
        selectedCrops: this.selectedCrops,
      }, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      }).then(response => {
        this.$message.success("保存成功", {
          duration: 100
        });
        this.getuserInfo();
      }).catch(error => {
        if (error.response.status === 401) {
          this.$message.error("身份验证失效，请重新登录");
          this.$router.push("/user/login");
        } else {
          this.$message.error("保存失败：" + (error.message || "未知错误"));
        }
      });

    }
  },
  created() {
    this.getuserInfo();
    this.getAreaOptions();
  }
}
;
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

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="bg-white shadow-sm">

    </div>
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- 标题区 -->
      <div
        class="text-center mb-12 bg-gradient-to-r from-blue-50 to-green-50 rounded-xl p-6 sm:p-8 shadow-lg border border-blue-100">
        <h1
          class="text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent mb-4">
          霜冻防御建议</h1>
        <p class="text-base sm:text-lg text-gray-600">为宁夏特色作物保驾护航，科学防护，精准预警</p>
        <div class="mt-4 flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-8">
          <div class="flex items-center text-blue-600">
            <i class="fas fa-shield-alt mr-2"></i>
            <span class="font-medium text-sm sm:text-base">科学防护</span>
          </div>
          <div class="flex items-center text-green-600">
            <i class="fas fa-chart-line mr-2"></i>
            <span class="font-medium text-sm sm:text-base">精准预警</span>
          </div>
          <div class="flex items-center text-purple-600">
            <i class="fas fa-leaf mr-2"></i>
            <span class="font-medium text-sm sm:text-base">作物保护</span>
          </div>
        </div>
      </div>
      <!-- 预警等级区 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8 mb-12">
        <div
          class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 sm:p-8 shadow-lg border border-blue-200 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
          <div class="flex items-center mb-6">
            <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mr-4">
              <i class="fas fa-exclamation-circle text-white text-xl"></i>
            </div>
            <h3 class="text-2xl font-bold text-blue-700">蓝色预警</h3>
          </div>
          <div class="bg-white rounded-lg p-4 mb-6 shadow-sm">
            <p class="text-gray-700 font-medium">24小时或48小时内最低气温将要下降到3℃以下0℃以上</p>
          </div>
          <ul class="space-y-3 text-gray-700">
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-blue-500 mr-3 w-5"></i>
              <span class="font-medium">加强田间监测</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-blue-500 mr-3 w-5"></i>
              <span class="font-medium">准备防霜设备</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-blue-500 mr-3 w-5"></i>
              <span class="font-medium">关注天气变化</span>
            </li>
          </ul>
        </div>
        <div
          class="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-6 sm:p-8 shadow-lg border border-yellow-200 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
          <div class="flex items-center mb-6">
            <div class="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center mr-4">
              <i class="fas fa-exclamation-triangle text-white text-xl"></i>
            </div>
            <h3 class="text-2xl font-bold text-yellow-700">黄色预警</h3>
          </div>
          <div class="bg-white rounded-lg p-4 mb-6 shadow-sm">
            <p class="text-gray-700 font-medium">24小时内最低气温将要下降到0℃以下-3℃以上</p>
          </div>
          <ul class="space-y-3 text-gray-700">
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-yellow-500 mr-3 w-5"></i>
              <span class="font-medium">立即开展防护</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-yellow-500 mr-3 w-5"></i>
              <span class="font-medium">准备灌溉设备</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-yellow-500 mr-3 w-5"></i>
              <span class="font-medium">组织人员值守</span>
            </li>
          </ul>
        </div>
        <div
          class="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6 sm:p-8 shadow-lg border border-orange-200 transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
          <div class="flex items-center mb-6">
            <div class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center mr-4">
              <i class="fas fa-radiation-alt text-white text-xl"></i>
            </div>
            <h3 class="text-2xl font-bold text-orange-700">橙色预警</h3>
          </div>
          <div class="bg-white rounded-lg p-4 mb-6 shadow-sm">
            <p class="text-gray-700 font-medium">24小时内最低气温将要下降到-3℃以下</p>
          </div>
          <ul class="space-y-3 text-gray-700">
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-orange-500 mr-3 w-5"></i>
              <span class="font-medium">全面启动应急预案</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-orange-500 mr-3 w-5"></i>
              <span class="font-medium">实施紧急防护措施</span>
            </li>
            <li class="flex items-center bg-white rounded-lg p-3 shadow-sm">
              <i class="fas fa-check text-orange-500 mr-3 w-5"></i>
              <span class="font-medium">24小时人员值守</span>
            </li>
          </ul>
        </div>
      </div>
      <!-- AI 智能问答区域 -->
      <div class="mb-12">
        <div class="bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-xl p-6 sm:p-8 border border-blue-100">
          <div class="flex flex-col sm:flex-row items-center mb-8">
            <div
              class="w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-0 sm:mr-4 mb-4 sm:mb-0 shadow-lg">
              <i class="fas fa-robot text-white text-xl sm:text-2xl"></i>
            </div>
            <div class="text-center sm:text-left">
              <h2
                class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                智能农业助手</h2>
              <p class="text-gray-600 mt-1 text-sm sm:text-base">AI驱动的农业专家，为您提供专业的霜冻防护建议</p>
            </div>
          </div>
          <div class="chat-container max-h-[500px] overflow-y-auto mb-6">
            <div v-for="(message, index) in chatMessages" :key="index"
                 :class="['mb-4 flex', message.type === 'user' ? 'justify-end' : 'justify-start']">
              <div :class="['max-w-[70%] rounded-lg p-4',
        message.type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700']">
                <div class="flex items-start">
                  <i :class="['fas mr-3 mt-1', message.type === 'user' ? 'fa-user' : 'fa-robot']"></i>
                  <div>
                    <div class="font-medium mb-1">{{ message.type === 'user' ? '您' : 'AI助手' }}</div>
                    <div>{{ message.content }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-4 sm:p-6 border border-gray-200 shadow-sm">
            <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 mb-6">
              <div class="flex-1 relative">
                <input v-model="userInput" type="text"
                       @keyup.enter="sendMessage"
                       placeholder="请输入您的农业相关问题..."
                       class="w-full px-4 py-3 pr-12 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200">
                <i class="fas fa-keyboard absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
              </div>
              <button @click="sendMessage"
                      class="px-6 sm:px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-200 transform hover:scale-105 shadow-lg font-medium whitespace-nowrap">
                <i class="fas fa-paper-plane mr-2"></i>
                <span class="hidden sm:inline">发送问题</span>
                <span class="sm:hidden">发送</span>
              </button>
            </div>
            <div class="flex justify-between items-center text-sm">
              <div class="flex items-center text-gray-500">
                <i class="fas fa-brain mr-2 text-blue-500"></i>
                <span>由智能农业大模型提供支持</span>
              </div>
              <button @click="clearChat"
                      class="text-gray-500 hover:text-red-600 transition-colors duration-200 flex items-center">
                <i class="fas fa-trash-alt mr-2"></i>
                <span>清空对话</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- FAQ区域 -->
      <div class="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-xl p-6 sm:p-8 border border-gray-100">
        <div class="flex flex-col sm:flex-row items-center mb-8">
          <div
            class="w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mr-0 sm:mr-4 mb-4 sm:mb-0 shadow-lg">
            <i class="fas fa-question-circle text-white text-xl sm:text-2xl"></i>
          </div>
          <div class="text-center sm:text-left">
            <h2
              class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              常见问题解答</h2>
            <p class="text-gray-600 mt-1 text-sm sm:text-base">快速获取霜冻防护的常见问题答案</p>
          </div>
        </div>
        <div class="space-y-4 sm:space-y-6">
          <div v-for="(item, index) in faqs" :key="index"
               class="bg-white rounded-xl p-4 sm:p-6 shadow-md border border-gray-100 transition-all duration-300 hover:shadow-lg">
            <div class="flex justify-between items-center cursor-pointer"
                 @click="toggleFaq(index)">
              <div class="flex items-center flex-1 mr-4">
                <div
                  class="w-6 h-6 sm:w-8 sm:h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3 sm:mr-4 flex-shrink-0">
                  <span class="text-white font-bold text-xs sm:text-sm">Q</span>
                </div>
                <span class="text-gray-800 font-semibold text-base sm:text-lg">{{ item.question }}</span>
              </div>
              <div
                class="w-6 h-6 sm:w-8 sm:h-8 bg-gray-100 rounded-full flex items-center justify-center transition-transform duration-200 flex-shrink-0"
                :class="{'rotate-180': item.isOpen}">
                <i :class="['fas', 'fa-chevron-down', 'text-gray-600']"></i>
              </div>
            </div>
            <div v-show="item.isOpen" class="mt-4 sm:mt-6 pl-0 sm:pl-12 transition-all duration-300">
              <div class="bg-gradient-to-r from-orange-50 to-yellow-50 rounded-lg p-4 border-l-4 border-orange-500">
                <div class="flex items-start">
                  <div
                    class="w-5 h-5 sm:w-6 sm:h-6 bg-orange-500 rounded-full flex items-center justify-center mr-3 mt-1 flex-shrink-0">
                    <span class="text-white font-bold text-xs">A</span>
                  </div>
                  <span class="text-gray-700 leading-relaxed text-sm sm:text-base">{{ item.answer }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      userInput: '',
      chatMessages: [
        {
          type: 'ai',
          content: '您好！我是智能农业助手，可以为您解答农业相关的问题，特别是关于霜冻预警和防护措施方面的咨询。请问有什么可以帮您的吗？'
        }
      ],
      faqs: [
        {
          question: '如何获取最新的霜冻预警信息？',
          answer: '您可以在本系统的预警信息页面查看最新的霜冻预警信号，也可以关注宁夏气象局的官方网站、微信公众号、微博等平台获取相关信息。',
          isOpen: false
        },
        {
          question: '霜冻预警信号的等级是如何划分的？',
          answer: '霜冻预警信号分三级，分别以蓝色、黄色、橙色表示。蓝色预警标准为24小时或48小时内最低气温将要下降到3℃以下0℃以上（含3℃），对农业将产生影响；黄色预警标准为24小时内最低气温将要下降到0℃以下-3℃以上（含0℃），对农业将产生严重影响；橙色预警标准为24小时内最低气温将要下降到-3℃以下，对农业将产生特别严重影响。',
          isOpen: false
        },
        {
          question: '葡萄在霜冻来临前有哪些具体的防护措施？',
          answer: '尚未出土的酿酒葡萄种植基地可暂缓出土，已经出土的要做好园区巡查，适时上架。霜冻防御可采用灌水的方式，漫灌效果最好，喷灌次之，滴灌效果最差，灌溉面积越大效果越好。',
          isOpen: false
        }
      ],
      isLoading: false // 添加加载状态
    };
  },
  methods: {
    toggleFaq(index) {
      this.faqs[index].isOpen = !this.faqs[index].isOpen;
    },
    sendMessage() {
      if (!this.userInput.trim()) return;

      // 添加用户消息
      this.chatMessages.push({
        type: 'user',
        content: this.userInput
      });

      // 模拟AI回复
      setTimeout(() => {
        this.chatMessages.push({
          type: 'ai',
          content: '我理解您的问题。根据当前的农业知识库，建议您可以采取以下措施...[这里是模拟的回复内容]'
        });
      }, 1000);

      this.userInput = '';

      // 滚动到底部
      this.$nextTick(() => {
        const container = document.querySelector('.chat-container');
        container.scrollTop = container.scrollHeight;
      });
    },
    clearChat() {
      this.chatMessages = [{
        type: 'ai',
        content: '您好！我是智能农业助手，可以为您解答农业相关的问题，特别是关于霜冻预警和防护措施方面的咨询。请问有什么可以帮您的吗？'
      }];
    },
    //  async sendMessage() {
    //   if (!this.userInput.trim() || this.isLoading) return;
    //
    //   // 添加用户消息
    //   this.chatMessages.push({
    //     type: 'user',
    //     content: this.userInput
    //   });
    //
    //   const userMessage = this.userInput;
    //   this.userInput = '';
    //   this.isLoading = true;
    //
    //
    //     try {
    //       // 调用Flask后端API
    //       const response = await fetch('http://localhost:5000/api/chat', {
    //         method: 'POST',
    //         headers: {
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //           message: userMessage
    //         })
    //       });
    //
    //     const result = await response.json();
    //
    //     if (result.success) {
    //       this.chatMessages.push({
    //         type: 'ai',
    //         content: result.data
    //       });
    //     } else {
    //       throw new Error(result.error || 'AI服务出错');
    //     }
    //   } catch (error) {
    //     console.error('AI请求失败:', error);
    //     this.chatMessages.push({
    //       type: 'ai',
    //       content: '抱歉，AI助手暂时无法响应，请稍后再试。'
    //     });
    //   } finally {
    //     this.isLoading = false;
    //     this.$nextTick(() => {
    //       const container = document.querySelector('.chat-container');
    //       if (container) {
    //         container.scrollTop = container.scrollHeight;
    //       }
    //     });
    //   }
    // },

  }
};
</script>
<style scoped>
.custom-input::-webkit-inner-spin-button,
.custom-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>

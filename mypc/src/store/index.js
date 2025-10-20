import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue组件里面的data
  state: {
    selectedArea: "银川市",
    selectedCropClass:["枸杞","葡萄",],
  },
  // 计算属性，用于获取派生状态
  getters: {
    selectedCrop: (state) => {
      return state.selectedCropClass.length > 0 ? state.selectedCropClass[0] : null;
    }
  },
  // 数据操作方法,类似vue里面的methods
  mutations: {
    change_selectedArea(state, area) {
      state.selectedArea = area;
    },
    change_selectedCrop(state, crop) {
      state.selectedCrop = crop;
    },
    change_selectedCropClass(state, cropClass) {
      state.selectedCropClass = cropClass;
      // 不需要在这里手动更新selectedCrop，getter会自动处理
    }
  }
});

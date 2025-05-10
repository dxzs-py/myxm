import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue组件里面的data
  state: {
    selectedArea: "银川市",
    selectedCrop: "葡萄"
  },
  // 数据操作方法,类似vue里面的methods
  mutations: {
    change_selectedArea(state, area) {
      state.selectedArea = area;
    },
    change_selectedCrop(state, crop) {
      state.selectedCrop = crop;
    }
  }
});

import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import settings from '../settings'
import { checkLogin } from '../utils/auth' // 添加这行导入

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedArea: "银川市",
    selecteAreas:["宁夏回族自治区","银川市","西夏区"],
    selectedCropClass: ["枸杞", "葡萄"],
  },
  getters: {
    selectedCrop: (state) => {
      return state.selectedCropClass.length > 0 ? state.selectedCropClass[0] : null;
    },

  },
  mutations: {
    change_selectedArea(state, area) {
      state.selectedArea = area;
    },
    change_selectedCrop(state, crop) {
      const index = state.selectedCropClass.indexOf(crop);
      if (index >= 0) {
        state.selectedCropClass.splice(index, 1);
        state.selectedCropClass.unshift(crop);
      } else {
        state.selectedCropClass.unshift(crop);
      }
    },
    change_selectedCropClass(state, cropClass) {
      state.selectedCropClass = cropClass;
    }
  },
  actions: {
    fetchSelectedArea({commit}) {
      // 检查用户是否已登录，如果已登录则不执行IP定位
      if (checkLogin()) {
        return; // 用户已登录，直接返回
      }

      axios.get(`${settings.HOST}/user/user-location/`)
        .then(response => {
          let city = null;
          if (response.data && response.data.location && response.data.location.content && response.data.location.content.address_detail) {
            city = response.data.location.content.address_detail.city;
          }

          const allowedCities = ["银川市", "石嘴山市", "吴忠市", "固原市", "中卫市"];
          const selectedCity = city && allowedCities.includes(city) ? city : "中卫市";

          commit('change_selectedArea', selectedCity);
        })
        .catch(error => {
          console.error("获取用户位置失败:", error);
          commit('change_selectedArea', "石嘴山市");
        });
    }
  }
});

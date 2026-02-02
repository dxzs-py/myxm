import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import settings from '../settings'
import {checkLogin} from '../utils/auth' // 添加这行导入

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selecteAreas: ["宁夏回族自治区", "银川市", "西夏区"],
    selectedCropClass: ["枸杞", "葡萄"],
    areaOptions: [], // 地区选项数据
  },
  getters: {
    selectedCrop: (state) => {
      return state.selectedCropClass.length > 0 ? state.selectedCropClass[0] : null;
    },
    selectedArea: (state) => {
      return state.selecteAreas.length === 3 ? state.selecteAreas[1] : "银川市";
    },
    // 获取完整的地区层级结构
    fullAreaPath: (state) => {
      return state.selecteAreas.join(" > ");
    },
    // 根据当前选中的地区获取对应的areaOptions节点
    currentAreaNode: (state) => {
      if (state.selecteAreas.length < 3 || state.areaOptions.length === 0) return null;

      const [province, city, district] = state.selecteAreas;

      // 查找省份
      const provinceNode = state.areaOptions.find(area => area.name === province);
      if (!provinceNode || !provinceNode.children) return null;

      // 查找城市
      const cityNode = provinceNode.children.find(area => area.name === city);
      if (!cityNode || !cityNode.children) return null;

      // 查找区县
      const districtNode = cityNode.children.find(area => area.name === district);
      return districtNode || null;
    },
  },
  mutations: {
    change_selectedArea(state, area) {
      // 更新selecteAreas的第二个元素（城市）
      if (state.selecteAreas.length >= 3) {
        state.selecteAreas.splice(1, 1, area);
      } else {
        // 如果selecteAreas长度不足3，确保有完整的地区信息
        if (state.areaOptions.length > 0) {
          // 从areaOptions中查找对应的省份和区县
          const province = state.selecteAreas[0] || "宁夏回族自治区";
          const provinceNode = state.areaOptions.find(p => p.name === province);
          if (provinceNode && provinceNode.children) {
            const cityNode = provinceNode.children.find(c => c.name === area);
            if (cityNode && cityNode.children) {
              // 默认取第一个区县
              const district = cityNode.children[0].name;
              state.selecteAreas = [province, area, district];
            } else {
              state.selecteAreas = [province, area, ""];
            }
          }
        }
      }
    },
    change_selecteAreas(state, areas) {
      state.selecteAreas = areas;
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
    },
    // 设置地区选项数据
    set_areaOptions(state, options) {
      state.areaOptions = options;
    }
  },
  actions: {
    fetchSelectedArea({commit}) {
      // 使用后端提供的IP定位接口
      return axios.get(`${settings.HOST}/user/user-location/`)
        .then(response => {
          let city = null;
          let district = null;
          let province = null;

          // 检查响应数据结构
          if (response.data && response.data.location && response.data.location.content) {
            // 适配不同的响应格式
            const addressDetail = response.data.location.content.address_detail || response.data.location.content;
            if (addressDetail) {
              city = addressDetail.city;
              district = addressDetail.district;
              province = addressDetail.province;
            }
          }

          // 确保省份、城市、区县有值
          province = province || "宁夏回族自治区";
          city = city || "银川市";
          district = district || "西夏区";

          // 验证城市是否在允许的列表中
          const allowedCities = ["银川市", "石嘴山市", "吴忠市", "固原市", "中卫市"];
          if (!allowedCities.includes(city)) {
            city = "银川市";
            district = "西夏区";
          }

          const selectedAreas = [province, city, district];
          commit('change_selecteAreas', selectedAreas);
          return selectedAreas;
        })
        .catch(error => {
          console.error("获取用户位置失败:", error);
          // 默认地址
          const defaultAreas = ["宁夏回族自治区", "中卫市", "沙坡头区"];
          commit('change_selecteAreas', defaultAreas);
          return defaultAreas;
        });
    },
    // 获取地区选项数据
    getAreaOptions({commit}) {
      return axios.get(`${settings.HOST}user/areas/hierarchy/`)
        .then(response => {
          commit('set_areaOptions', response.data);
          return response.data;
        })
        .catch(error => {
          console.error("获取地区选项失败:", error);
          throw error;
        });
    }
  }
});

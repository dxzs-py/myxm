<template>

  <div ref="Map" style="width: 100%;height: 100%;"/>

</template>

<script>

// 引入控件图标
import LeftArrowhead from '@/assets/test/left.png'

// 引入地图json数据
import NingXiaMap from '@/assets/test/map/NingXiaMap.json'
import ShiZuiShanMap from '@/assets/test/map/ShiZuiShanMap.json'
import YinChuanMap from '@/assets/test/map/YinChuanMap.json'
import WuZhongMap from '@/assets/test/map/WuZhongMap.json'
import ZhongWeiMap from '@/assets/test/map/ZhongWeiMap.json'
import GuYuanMap from '@/assets/test/map/GuYuanMap.json'

export default {
  name: 'Echarts',
  data() {
    return {
      productionArea: [
        {
          city: '石嘴山市', value: [{name: '石嘴山产区', value: [106.39, 39.02, 2]}],
        },
        {
          city: '银川市',
          value: [{name: '贺兰产区', value: [106.01, 38.63, 10]},
            {name: '永宁产区', value: [106.10, 38.28, 15]},
            {name: '银川产区', value: [106.20, 38.48, 12]},],
        },
        {
          city: '吴忠市',
          value: [{name: '红寺堡产区', value: [106.28, 37.40, 11]},
            {name: '青铜峡产区', value: [105.90, 38.05, 16]},]
        },
        {
          city: '中卫市', value: [],
        },
        {
          city: '固原市', value: [],
        },
      ],
      myChart: null, // 保存图表实例
      chartOption: null, // 保存图表配置
      totalAreaByCity: {}, // 用于存储各城市的种植总面积
    }
  },
  created() {
    this.getProductionArea()
  },
  computed: {
    selectedCrop() {
      return this.$store.getters.selectedCrop;
    },
  },
  mounted() {
    this.echartsInit(this.$store)
  },
  watch: {
    // 监听productionArea变化，更新图表
    productionArea: {
      handler(newVal) {
        if (this.myChart && this.chartOption) {
          // 更新数据
          const flattenProductionArea = [];
          const totalAreaByCity = {};
          newVal.forEach(item => {
            let totalArea = 0;
            if (Array.isArray(item.value)) {
              item.value.forEach(area => {
                flattenProductionArea.push(area);
                if (area.value && area.value.length >= 3) {
                  totalArea += area.value[2]; // 第三个元素是面积数据
                }
              });
            }
            totalAreaByCity[item.city] = totalArea;
          });
          this.totalAreaByCity = totalAreaByCity;

          // 更新图表配置中的数据
          this.chartOption.series[0].data = flattenProductionArea;

          // 重新设置图表配置
          this.myChart.setOption(this.chartOption);
        }
      },
      deep: true
    },
    selectedCrop(newVal) {
      // 当作物种类改变时，重新获取数据
      this.getProductionArea();
      this.resetToProvince();
    }
  },
  methods: {
    getProductionArea() {
      this.$axios.get(`${this.$settings.HOST}/crop/plantArea/`, {
        params: {
          crop: this.selectedCrop
        }
      }).then(res => {
        this.productionArea = res.data.productionArea
        this.$message.success("数据获取成功")
      }).catch(err => {
        this.$message.error(err.message + "后端错误！请联系管理员处理")
      })
    },
    echartsInit(store) {
      // 注册每个地图
      this.$echarts.registerMap('NingXiaMap', NingXiaMap)
      this.$echarts.registerMap('ShiZuiShanMap', ShiZuiShanMap)
      this.$echarts.registerMap('YinChuanMap', YinChuanMap)
      this.$echarts.registerMap('WuZhongMap', WuZhongMap)
      this.$echarts.registerMap('ZhongWeiMap', ZhongWeiMap)
      this.$echarts.registerMap('GuYuanMap', GuYuanMap)


      // 产区

      const productionArea = this.productionArea;

      // 将嵌套结构转换为扁平结构以适配现有逻辑
      const flattenProductionArea = [];
      productionArea.forEach(item => {
        if (Array.isArray(item.value)) {
          item.value.forEach(area => {
            flattenProductionArea.push(area);
          });
        }
      });

      this.chartOption = {
        geo: {
          map: 'NingXiaMap',
          zoom: 1.2,
          itemStyle: {
            areaColor: '#9e9e9e', // 默认区块颜色
            borderColor: '#183663', // 区块描边颜色
            borderWidth: 1 // 区块描边颜色
          },
          emphasis: {
            itemStyle: {areaColor: '#708a6a'}
          },
          label: {
            show: true,
            color: '#0043ff',
            fontSize: 15,
            fontWeight: 'bolder',
            labelLayout: {
              hideOverlap: true, // 隐藏重叠的标签
              moveOverlap: 'shiftY', // 当标签重叠时，在Y轴方向上移动
              draggable: true, // 允许用户拖拽标签调整位置
              align: 'center', // 标签对齐方式
            }
          },
          // 单独调整某块区域的样式
          regions: [
            {
              name: '石嘴山市',
              label: {
                offset: [-100, -10],
                labelLayout: {
                  moveOverlap: 'shiftY', // 自动避让重叠标签
                  hideOverlap: true     // 隐藏完全重叠的标签
                }
              },
              itemStyle: {
                // areaColor: '#73C0DE'
              },
              tooltip: {
                formatter: (params) => {
                  const cityName = params.name;
                  const totalArea = this.totalAreaByCity[cityName] || 0;
                  return totalArea === 0 ? `${cityName}<br/>未种植${this.selectedCrop}` : `${cityName}<br/>种植${this.selectedCrop}总面积：${totalArea}万亩`;
                }
              },
            },
            {
              name: '银川市',
              label: {
                offset: [65, -10],
                labelLayout: {
                  moveOverlap: 'shiftY', // 自动避让重叠标签
                  hideOverlap: true     // 隐藏完全重叠的标签
                }
              },
              itemStyle: {
                // areaColor: '#91CC75'
              },
              tooltip: {
                formatter: (params) => {
                  const cityName = params.name;
                  const totalArea = this.totalAreaByCity[cityName] || 0;
                  return totalArea === 0 ? `${cityName}<br/>未种植${this.selectedCrop}` : `${cityName}<br/>种植${this.selectedCrop}总面积：${totalArea}万亩`;
                }
              },
            },
            {
              name: '吴忠市',
              label: {
                offset: [60, 70],
                labelLayout: {
                  moveOverlap: 'shiftY', // 自动避让重叠标签
                  hideOverlap: true     // 隐藏完全重叠的标签
                }
              },
              itemStyle: {
                // areaColor: '#EE6666'
              },
              tooltip: {
                formatter: (params) => {
                  const cityName = params.name;
                  const totalArea = this.totalAreaByCity[cityName] || 0;
                  return totalArea === 0 ? `${cityName}<br/>未种植${this.selectedCrop}` : `${cityName}<br/>种植${this.selectedCrop}总面积：${totalArea}万亩`;
                }
              }
            },
            {
              name: '中卫市',
              label: {
                offset: [-70, 25],
                labelLayout: {
                  moveOverlap: 'shiftY', // 自动避让重叠标签
                  hideOverlap: true     // 隐藏完全重叠的标签
                }
              },
              itemStyle: {
                // areaColor: '#FC8452'
              },
              tooltip: {
                formatter: (params) => {
                  const cityName = params.name;
                  const totalArea = this.totalAreaByCity[cityName] || 0;
                  return totalArea === 0 ? `${cityName}<br/>未种植${this.selectedCrop}` : `${cityName}<br/>种植${this.selectedCrop}总面积：${totalArea}万亩`;
                }
              }
            },
            {
              name: '固原市',
              label: {
                offset: [65, 45],
                labelLayout: {
                  moveOverlap: 'shiftY', // 自动避让重叠标签
                  hideOverlap: true     // 隐藏完全重叠的标签
                }
              },
              itemStyle: function (params) {
                // areaColor: '#708a6a'
              },
              tooltip: {
                formatter: (params) => {
                  const cityName = params.name;
                  const totalArea = this.totalAreaByCity[cityName] || 0;
                  return totalArea === 0 ? `${cityName}<br/>未种植${this.selectedCrop}` : `${cityName}<br/>种植${this.selectedCrop}总面积：${totalArea}万亩`;
                }
              }
            }
          ]
        },
        title: {
          text: '宁夏特色作物种植面积可视化',
          subtext: '宁夏特色种植面积',
          textStyle: {
            color: '#2c3e50',
            fontSize: 20,
            fontWeight: 'bold'
          },
          subtextStyle: {
            color: '#7f8c8d',
            fontSize: 14
          },

        },
        toolbox: {
          // 是否显示右侧控件
          show: true,
          orient: 'horizontal',  // 排列方向 vertical-垂直 | horizontal-水平
          left: 'left',    // 水平定位 right-右侧 | 20-20像素 | '20%'-百分比
          top: 'bottom',   // 垂直定位 top-顶部 | 100-100像素 | '30%'-百分比
          itemGap: 10,
          feature: {
            myTool1: {
              show: true,
              title: '返回',
              name: '返回',
              icon: 'image://' + LeftArrowhead,
              onclick: () => { // 改为箭头函数以保持this上下文
                this.chartOption.geo.map = 'NingXiaMap'
                this.chartOption.geo.zoom = 1.2; // 恢复主地图缩放比例

                // 更新数据
                const flattenProductionArea = [];
                this.productionArea.forEach(item => {
                  if (Array.isArray(item.value)) {
                    item.value.forEach(area => {
                      flattenProductionArea.push(area);
                    });
                  }
                });

                this.chartOption.series[0].data = flattenProductionArea
                this.myChart.setOption(this.chartOption)// 刷新显示
              }
            },

          }
        },
        layoutCenter: ['49%', '50%'], // 地图位置
        tooltip: {
          trigger: 'item',
          show: true,
          // formatter: '{b}'
          formatter: function (params) {
            return params.name + '<br/>' + "种植面积：" + params.value[2] + '万亩';
          },
          textStyle: {
            fontSize: 12
          },
        },
        series: [
          {
            type: 'scatter',
            data: flattenProductionArea,
            tooltip: {
              show: true // 开启产区hover显示
            },
            coordinateSystem: 'geo',
            symbol: (params) => {
              if (this.selectedCrop === '葡萄') {
                return 'image://../../../static/svg/grapes.svg';
              } else if (this.selectedCrop === '枸杞') {
                // return 'image://' + require('../../../static/image/gq1.jpg');
                return 'image://../../../static/svg/gouqi.svg';
              } else if (this.selectedCrop === '春小麦' || this.selectedCrop === '冬小麦') {
                // return 'image://' + require('../../../static/image/xm.jpg');
                return 'image://../../../static/svg/wheat-drawing.svg';
              }
            },
            symbolSize: function (val) {
              // 用平方根确保面积与数据值成正比
              return Math.sqrt(val[2]) * 8;
            },
            label: {
              position: function (params) {
                return 'top'; // 中部区域标签在上方
              },
              // 动态调整字体大小（根据圆点大小自适应）
              fontSize: function (params) {
                // 基础字体大小 + 根据圆点半径调整
                const baseSize = 8;
                const radius = Math.sqrt(params.value[2]);
                return Math.min(20, baseSize + radius); // 最大不超过20px
              },
              formatter: '{b}',
              show: true,
              color: '#313131',
              fontWeight: 'bolder',
              // 自动避让布局
              rich: {
                text: {
                  padding: [2, 5],
                  backgroundColor: 'rgba(255,255,255,0.7)'
                }
              },
              // 自动调整标签位置
              labelLayout: {
                moveOverlap: 'shiftY',  // 自动上下移动避让
                hideOverlap: true,      // 隐藏重叠标签
                draggable: true,        // 允许拖拽调整位置
                align: 'center'         // 居中对齐
              }
            },
            itemStyle: {
              /*color: (params) => {
                // 根据 selectedCrop 的值返回不同颜色
                if (this.selectedCrop === '葡萄') {
                  return '#9A60B4'; // 紫色
                } else if (this.selectedCrop === '枸杞') {
                  return '#EE6666'; // 红色
                } else if (this.selectedCrop === '春小麦') {
                  return '#F5DEB3'; // 橙色
                } else if (this.selectedCrop === '冬小麦') {
                  return '#DEB887'; // 橙色
                }
                return '#578bd1'; // 蓝色
              },
              opacity: 0.7 // 增加透明度，使圆面叠加时更清晰*/
            },
            emphasis: {
              label: {
                show: true
              }
            }
          },

        ]
      }

      this.myChart = this.$echarts.init(this.$refs.Map)
      this.myChart.showLoading()
      // 等待获取数据
      this.myChart.hideLoading()
      this.myChart.setOption(this.chartOption)

      // 点击事件使用路由达到下钻效果
      this.myChart.on('click', (params) => { // 改为箭头函数以保持this上下文
        // console.log(params.name, params.value) // 取到对应的数据集
        const validAreas = ['石嘴山市', '银川市', '吴忠市', '中卫市', '固原市'];

        if (validAreas.includes(params.name)) {
          store.commit('change_selectedArea', params.name);
        }

        // 当前是宁夏地图才执行 进入下钻后不使用
        let changeMap = ''

        // 查找城市对应的产区数据
        const cityData = this.productionArea.find(item => item.city === params.name);

        // 刷新函数
        const change = () => { // 改为箭头函数
          this.chartOption.geo.map = changeMap
          this.myChart.setOption(this.chartOption)// 刷新显示
        }

        switch (params.name) {
          case '石嘴山市' :
            changeMap = 'ShiZuiShanMap'
            this.chartOption.geo.zoom = 1.1; // 新增下级地图缩放配置
            this.chartOption.series[0].data = cityData ? cityData.value : []
            change()
            break
          case '银川市' :
            changeMap = 'YinChuanMap'
            this.chartOption.geo.zoom = 0.9; // 新增下级地图缩放配置
            this.chartOption.series[0].data = cityData ? cityData.value : []
            change()
            break
          case '吴忠市' :
            changeMap = 'WuZhongMap'
            this.chartOption.geo.zoom = 0.9; // 新增下级地图缩放配置
            this.chartOption.series[0].data = cityData ? cityData.value : []
            change()
            break
          case '中卫市' :
            changeMap = 'ZhongWeiMap'
            this.chartOption.geo.zoom = 0.9; // 新增下级地图缩放配置
            this.chartOption.series[0].data = cityData ? cityData.value : []
            change()
            break
          case '固原市' :
            changeMap = 'GuYuanMap'
            this.chartOption.geo.zoom = 0.9; // 新增下级地图缩放配置
            this.chartOption.series[0].data = cityData ? cityData.value : []
            change()
            break
        }
      })
    },
    resetToProvince() {
      if (this.myChart && this.chartOption) {
        this.chartOption.geo.map = 'NingXiaMap';
        this.chartOption.geo.zoom = 1.2;
        // 从productionArea中提取所有市的点
        const flattenProductionArea = [];
        this.productionArea.forEach(item => {
          if (Array.isArray(item.value)) {
            item.value.forEach(area => {
              flattenProductionArea.push(area);
            });
          }
        });
        this.chartOption.series[0].data = flattenProductionArea;
        this.myChart.setOption(this.chartOption);
      }
    }
  }
}
</script>

<style scoped>

</style>

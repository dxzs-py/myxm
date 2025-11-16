<template>

  <div class="min-h-screen bg-[#FAFAFA] font-sans">
    <!-- 主体内容 -->
    <main class="pt-14 pb-16">
      <div class="container mx-auto px-10 py-8 max-w-[1200px]">
        <!-- 搜索框（作物/品种实时过滤） -->
        <div class="mb-8">
          <div class="flex items-center gap-3 bg-white/90 border border-green-100 rounded-2xl px-4 py-3 shadow-sm">
            <i class="fas fa-search text-green-500"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索作物或品种，例如：葡萄、赤霞珠、宁杞…"
              class="flex-1 outline-none text-sm placeholder:text-gray-400"
            />
            <button v-if="searchQuery" @click="searchQuery = ''" class="text-gray-400 hover:text-gray-600"><i
              class="fas fa-times"></i></button>
          </div>
        </div>

        <!-- 作物分段展示（不再用按钮切换） -->
        <div v-for="(crop, cropIdx) in filteredCrops" :key="'crop-' + cropIdx" class="mb-12">
          <!-- 分段标题 -->
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg md:text-xl font-extrabold text-[#2E7D32] tracking-wide flex items-center gap-2">
              <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-green-100 text-green-600"><i
                class="fas"
                :class="cropIdx===0 ? 'fa-wine-bottle' : (cropIdx===1 ? 'fa-seedling' : 'fa-leaf')"></i></span>
              {{ crop.name }}
            </h2>
            <div class="text-xs text-gray-500">共 {{ crop.varieties.length }} 个品种</div>
          </div>

          <!-- 品种卡片（自适应/缩小版） -->
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <div
              v-for="(variety, idx) in crop.varieties"
              :key="'var-' + cropIdx + '-' + idx"
              class="bg-white/95 rounded-2xl overflow-hidden shadow-md hover:shadow-xl border border-[#E7F7EF] group transition-all duration-300 hover:-translate-y-1.5 hover:border-green-400 hover:ring-1 hover:ring-green-200/40 backdrop-blur-sm flex flex-col"
            >
              <!-- 图片区域暂时隐藏 -->
               <div class="flex-shrink-0 w-full min-h-28 max-h-40 flex items-center justify-center bg-gradient-to-b from-[#e8fff7] to-[#f7fdfc] border-b border-[#f0f7ee] relative">
                <img
                  :src="variety.image"
                  alt=""
                  loading="lazy"
                  class="w-full h-full max-h-40 object-cover object-center rounded-xl group-hover:scale-105 transition-transform duration-300 shadow-sm cursor-zoom-in"
                  @error="(e) => { e.target.onerror = null; e.target.src='/static/image/bj.jpg'; }"
                  @click="openPreview(variety.image)"
                />
                <div class="absolute top-2 left-2 text-[10px] px-2 py-0.5 rounded-full bg-white/85 border border-green-200 text-green-700 shadow">{{ crop.name }}</div>
              </div>
              <div class="flex-1 p-4 flex flex-col">
                <h3 class="text-[#359668] font-extrabold text-base mb-1 flex items-center gap-2 tracking-tight"><span
                  class="i-mdi-seed-plus bg-green-100 p-1 rounded-full mr-1"></span>{{ variety.title }}</h3>
                <div class="space-y-1.5 flex-1 text-[13px]">
                  <div class="flex items-center gap-2">
                    <span class="inline-block w-1.5 h-1.5 rounded-full bg-green-300"></span>
                    <span class="text-gray-500">关键期：</span> <span class="text-[#32784D]">{{ variety.season }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="inline-block w-1.5 h-1.5 rounded-full bg-yellow-300"></span>
                    <span class="text-gray-500">阈值：</span> <span class="text-[#B68518]">{{
                      variety.temperature
                    }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="inline-block w-1.5 h-1.5 rounded-full bg-blue-200"></span>
                    <span class="text-gray-500">特性：</span> <span class="text-[#298454]">{{
                      variety.characteristics
                    }}</span>
                  </div>
                  <div class="mt-1 text-gray-700/80 leading-relaxed">{{ variety.details }}</div>
                </div>
                <div v-if="variety.measures"
                     class="mt-3 p-2.5 rounded-xl bg-gradient-to-br from-green-50 via-green-100 to-blue-50 text-green-700 shadow-inner flex flex-col gap-1 border-t border-green-100">
                  <div class="mb-0.5 font-bold flex items-center gap-1 text-[13px]"><i
                    class="fas fa-shield-alt text-green-400"></i> 防护措施：
                  </div>
                  <div style="white-space:pre-line" class="text-[12px] text-green-800">{{ variety.measures }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 数据来源 -->
        <div
          class="w-full bg-white/80 rounded-lg p-4 text-center text-gray-600 text-xs shadow flex flex-col items-center gap-1 border border-[#eaf2e8] backdrop-blur-md">
          <span class="mb-1 text-green-400 text-base"><i class="fas fa-seedling"></i></span>
          数据来源：宁夏农业农村厅、宁夏气象服务中心
        </div>
      </div>
    </main>

    <!-- 预览大图弹窗 -->
    <div v-if="previewVisible" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/70"
         @click.self="closePreview">
      <div
        class="max-w-[90vw] max-h-[85vh] p-2 bg-white/10 rounded-2xl backdrop-blur-md shadow-2xl border border-white/20 relative">
        <button @click="closePreview" class="absolute -top-12 right-0 text-white/90 hover:text-white"><i
          class="fas fa-times text-2xl"></i></button>
        <img :src="previewSrc" alt="preview" class="max-w-full max-h-[80vh] object-contain rounded-lg"
             @error="(e)=>{e.target.onerror=null; e.target.src='https://img.zcool.cn/community/0166fe5e2ba516a8012141686724ed.jpg'}"/>
      </div>
    </div>

    <!-- 底部信息 -->
    <footer
      class="bg-gradient-to-tr from-[#2E7D32] to-[#43EA99] text-white text-center py-4 text-sm tracking-wider shadow-inner">
      © 2025 宁夏特色作物霜冻知识库 版权所有
    </footer>

    <!-- 回到顶部按钮 (移动端) -->
    <button
      v-if="showBackTop"
      @click="scrollToTop"
      class="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-[#43EA99] to-[#2E7D32] text-white flex items-center justify-center shadow-xl md:hidden ring-2 ring-green-200/40 animate-bounce"
    >
      <i class="fas fa-arrow-up text-2xl drop-shadow-lg"></i>
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isScrolled: false,
      showBackTop: false,
      // activeCrop: 0,  // 移除切换逻辑
      searchQuery: '',
      previewVisible: false,
      previewSrc: '',
      crops: [
        {
          name: '葡萄',
          varieties: [
            {
              title: '赤霞珠',
              season: '春季（4-6月）',
              temperature: '轻(-4.49℃)/中(-5℃)/重(≤-5.5℃)',
              characteristics: '主栽红葡萄，芽期抗寒弱',
              details: '出埋土期（4月中下旬，-7.7℃芽坏死）\n绒球期（4-5月，-7.7℃抗寒弱）\n芽开放期（5月上中旬，-4.49℃坏死）\n展叶期（5月中下旬，-2.79℃焦枯）',
              measures: '1. 春季结合气温趋势延后出土与展叶时间\n2. 覆盖地膜、酿酒葡萄未完全出土前延迟萌芽\n3. 夜间洒水、烟熏防霜、园区设置小拱棚、风扇等',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '霞多丽',
              season: '春季（4-5月）',
              temperature: '轻(-5℃)/中(-6℃)/重(≤-7℃)',
              characteristics: '主栽白葡萄，新叶敏感',
              details: '绒球期（4-5月，-6℃芽冻伤）\n展叶期（5月中下旬，-3℃萎蔫）',
              measures: '1. 埋土防寒保温，结合天气适时出土\n2. 遇预警实时灌水提温，准备霜冻布、点烟防护',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '梅洛',
              season: '春季（4-5月）',
              temperature: '轻(-5.2℃)/中(-6.1℃)/重(≤-7℃)',
              characteristics: '早熟，抗寒略强',
              details: '芽开放期（4-5月，-5.2℃芽损伤）\n新梢生长期（5月中下旬，-2.5℃冻伤）',
              measures: '1. 春季加强园区气象监测，灵活安排田间管理\n2. 可用膜覆盖、风障减缓低温影响',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '蛇龙珠',
              season: '春季（4-5月）',
              temperature: '轻(-4.8℃)/中(-5.5℃)/重(≤-6.5℃)',
              characteristics: '晚熟果香浓',
              details: '展叶期（5月上中旬，-3.2℃焦枯）\n新梢生长期（5-6月，-2℃冻伤）',
              measures: '1. 注意展叶期和新梢生长期天气变化\n2. 可用临时小棚覆盖弱苗、喷施叶面肥提高抗逆性',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '贵人香',
              season: '春季（4-5月）',
              temperature: '轻(-5.5℃)/中(-6.5℃)/重(≤-7.5℃)',
              characteristics: '酸度高，抗寒中等',
              details: '绒球期（4-5月，-6.5℃芽坏死）\n展叶期（5月上旬，-3.5℃萎蔫）',
              measures: '1. 土壤湿度管理、蓄墒、遇冻易灌溉升温\n2. 必要时早晨覆盖无纺布，低洼地块注意排水防湿冻',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '威代尔',
              season: '春季（4-5月）',
              temperature: '轻(-6℃)/中(-7℃)/重(≤-8℃)',
              characteristics: '抗寒强，用于冰酒',
              details: '芽开放期（5月上旬，-6℃芽损伤）\n展叶期（5月中旬，-4℃冻伤）',
              measures: '1. 加强土壤培肥、灌溉和覆盖保温\n2. 冰葡萄田块加强监测，遇极端低温临时覆盖萌芽层',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
          ],
        },
        {
          name: '枸杞',
          varieties: [
            {
              title: '宁杞1号',
              season: '春季（3-5月）',
              temperature: '轻(-2℃)/中(-3℃)/重(≤-4℃)',
              characteristics: '丰产稳产，花期敏感',
              details: '露冠期（3-4月，-2℃枝冻伤）\n蕾期（4-5月，-2~-1℃蕾脱落）\n初花期（5月上中旬，-2~0℃花粉失活）\n盛花期（5月中下旬，-2~0℃落花）',
              measures: '1. 花前及时覆膜和熏烟防霜\n2. 涉及花期对晚霜区域加强田间巡查\n3. 低洼地块及时排水，增强土壤保温',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁杞4号',
              season: '春季（3-5月）',
              temperature: '同宁杞1号',
              characteristics: '棘刺少早产高产',
              details: '同宁杞1号',
              measures: '与宁杞1号同',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁杞5号',
              season: '春季（4-5月）',
              temperature: '轻(-1.8℃)/中(-2.8℃)/重(≤-3.8℃)',
              characteristics: '大果鲜食，耐寒略弱',
              details: '蕾期（4-5月，-1.8~-0.8℃蕾脱落）\n盛花期（5月中下旬，-1.8~0℃落花）',
              measures: '1. 花芽分化期适量叶面补钙\n2. 盛花期适时薄膜覆盖防霜\n3. 弱苗喷施植物生长调节剂提升抗逆力',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁杞7号',
              season: '春季（3-5月）',
              temperature: '轻(-2.2℃)/中(-3.2℃)/重(≤-4.2℃)',
              characteristics: '抗黑果病',
              details: '露冠期（3-4月，-2.2℃枝冻伤）\n初花期（5月上中旬，-2.2~0℃花粉失活）',
              measures: '1. 田间搭建简易小拱棚应对晚霜\n2. 选用抗逆性较强营养剂增施叶面肥',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁杞10号',
              season: '春季（4-5月）',
              temperature: '同宁杞1号',
              characteristics: '结果早，丰产',
              details: '同宁杞1号',
              measures: '与宁杞1号同',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '大麻叶枸杞',
              season: '春季（3-5月）',
              temperature: '轻(-2.5℃)/中(-3.5℃)/重(≤-4.5℃)',
              characteristics: '栽培历史久，抗逆强',
              details: '露冠期（3-4月，-2.5℃枝冻伤）\n初花期（5月上旬，-2.5~0℃花粉失活）',
              measures: '1. 露冠期及初花期减轻修剪保留弱枝\n2. 如遇极端低温临时增设风障、喷灌升温',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            }
          ],
        },
        {
          name: '水稻',
          varieties: [
            {
              title: '宁粳43号',
              season: '春季（4-5月）',
              temperature: '轻(8~10℃)/中(6~8℃)/重(≤6℃)',
              characteristics: '耐寒中等，稳产',
              details: '播种期（4月中下旬，≤6℃烂种）\n移栽期（5月中下旬，≤8℃缓苗慢）\n分蘖期（6-7月，≤12℃分蘖少）',
              measures: '1. 播种避免低温期、进行地膜覆盖提温\n2. 弱苗地块育秧期采用透气性好无纺布保护',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁粳50号',
              season: '春季（4-5月）',
              temperature: '同宁粳43号',
              characteristics: '优质米，抗寒中等',
              details: '同宁粳43号',
              measures: '与宁粳43号同',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '富源4号',
              season: '春季（4-5月）',
              temperature: '轻(7~9℃)/中(5~7℃)/重(≤5℃)',
              characteristics: '早熟，抗寒略弱',
              details: '播种期（4月中下旬，≤5℃烂芽）\n移栽期（5月下旬，≤7℃烂根）',
              measures: '1. 低温预警前后先育晚播，适时增施磷钾肥\n2. 慎用早日移栽，寒流期间慎用除草剂',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁粳31号',
              season: '春季（4-5月）',
              temperature: '同宁粳43号',
              characteristics: '抗逆强，丰产',
              details: '同宁粳43号',
              measures: '与宁粳43号同',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            },
            {
              title: '宁粳48号',
              season: '春季（4-5月）',
              temperature: '轻(7~9℃)/中(5~7℃)/重(≤5℃)',
              characteristics: '优质耐寒中等',
              details: '播种期（4月中下旬，≤5℃烂种）\n移栽期（5月中下旬，≤7℃缓苗慢）',
              measures: '1. 同富源4号措施\n2. 如遇春季倒春寒及时排除田间积水',
              image: 'https://via.placeholder.com/300x200/CCCCCC/666666?text=+',
            }
          ],
        }
      ]
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    this.checkScroll();
  },
  computed: {
    filteredCrops() {
      if (!this.searchQuery) return this.crops;
      const q = this.searchQuery.trim().toLowerCase();
      return this.crops
        .map(crop => {
          const nameHit = crop.name.toLowerCase().includes(q);
          const matchedVarieties = crop.varieties.filter(v =>
            (v.title && v.title.toLowerCase().includes(q)) ||
            (v.characteristics && v.characteristics.toLowerCase().includes(q)) ||
            (v.details && v.details.toLowerCase().includes(q))
          );
          return nameHit ? {...crop} : {name: crop.name, varieties: matchedVarieties};
        })
        .filter(c => c.varieties && c.varieties.length > 0 || c.name.toLowerCase().includes(q));
    }
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 50;
      this.showBackTop = window.scrollY > 300;
    },
    checkScroll() {
      this.handleScroll();
    },
    scrollToTop() {
      window.scrollTo({top: 0, behavior: 'smooth'});
    },
    openPreview(src) {
      this.previewSrc = src;
      this.previewVisible = true;
    },
    closePreview() {
      this.previewVisible = false;
      this.previewSrc = '';
    },
    handleImageError(event) {
      // 使用更可靠的默认图片，使用中性灰色而不是绿色
      event.target.src = 'https://via.placeholder.com/300x200/CCCCCC/666666?text=作物图片';
      event.target.onerror = null; // 防止无限循环
    }
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

body {
  font-family: 'Noto Sans SC', 'Microsoft YaHei', 'Arial', sans-serif;
  letter-spacing: 0.03em;
}

.container {
  max-width: 1440px;
}

/* 圆角按钮辅助类 */
.rounded-button {
  border-radius: 0.8em !important;
}

/* 为 FontAwesome icons 提供默认大小和居中 */
.fas {
  vertical-align: middle;
}

.i-mdi-seed-plus {
  display: inline-block;
  width: 1.5em;
  height: 1.5em;
  background: url('https://img.icons8.com/external-others-inmotus-design/24/1abc9c/external-seed-food-others-inmotus-design.png') center/contain no-repeat;
}
</style>


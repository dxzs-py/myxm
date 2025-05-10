<template>
  <div class="weather-card bg-white p-8 rounded-2xl">
    <h3 class="text-2xl font-bold mb-5 text-gray-800">{{ title }}</h3>
    <div class="grid grid-cols-2 gap-4">
      <div
        v-for="(item, index) in data"
        :key="index"
        class="bg-white p-6 rounded-xl shadow-lg transition-all duration-300 hover:shadow-xl hover:transform hover:-translate-y-1"
      >
        <div class="flex flex-col justify-between items-start mb-4">
          <span class="text-gray-600 mb-2 text-lg">{{ item.label }}</span>
          <i :class="['fas', item.icon, item.iconColor, 'text-2xl']" aria-hidden="true"></i>
        </div>
        <div class="text-4xl font-extrabold text-green-700 mb-2">{{ item.value }}</div>
        <div v-if="item.unit" class="text-sm text-gray-500 mt-1">{{ item.unit }}</div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'WeatherCard',
  props: {
    title: {
      type: String,
      required: true,
    },
    data: {
      type: Array,
      required: true,
      default: () => []
    }
  }
}
</script>

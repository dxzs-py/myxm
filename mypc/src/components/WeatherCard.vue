<template>
  <div class="weather-card">
    <h3 class="text-3xl font-extrabold mb-8 pb-4 bg-gradient-to-r from-blue-700 to-purple-700 text-transparent bg-clip-text">
      {{ title }}
    </h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div
        v-for="(item, index) in data"
        :key="index"
        class="bg-white p-8 rounded-2xl shadow-lg transition-all duration-500 
               hover:scale-105 hover:shadow-2xl hover:shadow-indigo-200/60 group"
      >
        <div class="flex items-center justify-between mb-6">
          <span class="text-gray-800 text-base font-bold tracking-wide">
            {{ item.label }}
          </span>
          <i :class="['fas', item.icon, item.iconColor, 'text-4xl', 'transition-transform', 'duration-500', 'group-hover:scale-125']" 
             aria-hidden="true"></i>
        </div>
        <div class="text-5xl font-black text-gray-900 mb-3">
          {{ item.value }}
        </div>
        <div v-if="item.unit" class="text-sm text-gray-600 flex items-center font-medium">
          <i class="fas fa-bolt mr-2 text-yellow-500 animate-pulse"></i>
          {{ item.unit }}
        </div>
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
      required: true
    },
    data: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  }
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
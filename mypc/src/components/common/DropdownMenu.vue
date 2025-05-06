<template>
  <div class="relative">
    <div @click.stop="toggle" class="cursor-pointer">
      <slot name="trigger"></slot>
    </div>

    <transition name="fade">
      <div v-show="show" class="absolute top-full mt-1 right-0 bg-white shadow-lg rounded-lg z-10">
        <div
          v-for="option in options"
          :key="option.value"
          @click.stop="handleSelect(option.value)"
          :class="['px-4 py-2 hover:bg-gray-100 cursor-pointer', { 'bg-gray-200': option.value === selected }]"

        >
          {{ option.label }}
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'DropdownMenu',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    options: {
      type: Array,
      required: true
    },
    selected: {
      type: [String, Number],
      default: null
    }
  },
  methods: {
    toggle() {
      this.$emit('toggle');
    },
    handleSelect(value) {
      this.$emit('select', value);
    }
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Header from "./components/common/Header.vue";
import Footer from "./components/common/Footer.vue";
export default {
  components: {Header, Footer,},
  name: 'App'
}
</script>

<style>

</style>

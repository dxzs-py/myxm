import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import KLG from "../components/Knowledge.vue";
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name:"Home",
      component: Home,
    },
    {
      path: '/home',
      name:"Home",
      component: Home,
    },
    {
      path: '/user/login',
      name:"Login",
      component: Login
    },
    {
      path: '/klg',
      name:"knowledge",
      component: KLG
    },
  ]
})

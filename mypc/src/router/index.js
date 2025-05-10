import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home1.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
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
      name:"Home1",
      component: Home,
    },
    {
      path: '/user/login',
      name:"Login",
      component: Login
    },
    {
      path: '/user/rgt',
      name:"Register",
      component: Register
    },
    {
      path: '/klg',
      name:"knowledge",
      component: KLG
    },
  ]
})

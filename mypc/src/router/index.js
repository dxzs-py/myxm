import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import KLG from "../components/Knowledge.vue";
import PS from "../components/person.vue"
import Header from "../components/common/Header.vue"
import Advice from "../components/advice.vue";
import zhishi from "../components/zhishi.vue";

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Header,
      redirect: '/home',
      children: [
        {
          path: '/home',
          name: "Home",
          component: Home,
        },
        {
          path: '/klg',
          name: "knowledge",
          component: KLG
        },
        {
          path: '/person',
          name: "ps",
          component: PS
        },
        {
          path: '/advice',
          name: "Advice",
          component: Advice
        },
        {
          path: '/zhishi',
          name: "zhishi",
          component: zhishi
        },
      ]
    },
    {
      path: '/user/login',
      name: "Login",
      component: Login
    },
    {
      path: '/user/rgt',
      name: "Register",
      component: Register
    },
  ]
})

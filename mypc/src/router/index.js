import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home.vue'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import KLG from "../components/Knowledge.vue";
import MAP from "../components/common/NingXiaMap.vue";
import PS from "../components/person.vue"
import Header from "../components/common/Header.vue"

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

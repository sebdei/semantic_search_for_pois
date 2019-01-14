import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import Welcome from '@/components/Welcome'

const routes = [
  { path: '/', component: Welcome },
]

const router = new VueRouter({
  routes
})

export default router

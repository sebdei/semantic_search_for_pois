import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import Welcome from '@/components/Welcome'
import ListPointsOfInterests from '@/components/points_of_interest/ListPointsOfInterests'
import DetailsPointsOfInterests from '@/components/points_of_interest/DetailsPointsOfInterests'

const routes = [
  { path: '/', component: Welcome },
  { path: '/points_of_interests', name:"list", component: ListPointsOfInterests, props: true },
  { path: '/points_of_interests/:id', name:"detail", component: DetailsPointsOfInterests },
]

const router = new VueRouter({
  routes
})

export default router

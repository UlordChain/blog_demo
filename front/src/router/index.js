import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: () => import('@/views/homeList/index')
    },
    { path: '/login', component: () => import('@/views/login/index') },
    { path: '/register', component: () => import('@/views/register/index') },
    { path: '/publish', component: () => import('@/views/publish/index') },
    { path: '/article', component: () => import('@/views/articleDetail/index')},
    { path: '/info', component: () => import('@/views/info/index')}
    // { path: '/register', component: () => import('@/views/register.vue') }
  ]
})

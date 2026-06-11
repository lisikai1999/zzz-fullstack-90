import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/rsa', name: 'rsa', component: () => import('../views/RsaView.vue') },
  { path: '/hash', name: 'hash', component: () => import('../views/HashView.vue') },
  { path: '/dh', name: 'dh', component: () => import('../views/DhView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})

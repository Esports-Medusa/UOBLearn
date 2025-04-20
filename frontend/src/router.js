import { createRouter, createWebHistory } from 'vue-router'
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import Home from './views/Home.vue'

const routes = [
  { path: '/', component:Home },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

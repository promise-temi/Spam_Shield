import { createRouter, createWebHistory } from 'vue-router'

import TableauDeBord from '@/Views/TableauDeBord.vue'
import BancDeTests from '@/Views/BancDeTests.vue'
import Parametres from '@/Views/Parametres.vue'
import Login from '@/Views/Login.vue'

import api from '@/axios/axios'


const routes = [
  {
    path: '/',
    redirect: '/tableau-de-bord'
  },
  {
    path: '/tableau-de-bord',
    component: TableauDeBord,
    meta: { requiresAuth: true }
  },
  {
    path: '/tests',
    component: BancDeTests,
    meta: { requiresAuth: true }
  },
  {
    path: '/banc-de-tests',
    component: BancDeTests,
    meta: { requiresAuth: true }
  },
  {
    path: '/options',
    component: Parametres,
    meta: { requiresAuth: true }
  },
  {
    path: '/parametres',
    component: Parametres,
    meta: { requiresAuth: true }
  },
  {
    path: '/connexion',
    name: 'connexion',
    component: Login
  }
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


router.beforeEach(async (to) => {
  const requiresAuth = to.matched.some(
    route => route.meta.requiresAuth
  )

  if (!requiresAuth) {
    return true
  }

  try {
    await api.get('/auth/me')
    return true
  } catch {
    return {
      name: 'connexion'
    }
  }
})


export default router
import { createRouter, createWebHistory } from 'vue-router'
import TableauDeBord from '@/Views/TableauDeBord.vue'
import BancDeTests from '@/Views/BancDeTests.vue'
import Parametres from '@/Views/Parametres.vue'
import Login from '@/Views/Login.vue'

const routes = [
  { path: '/', component: TableauDeBord},
  { path: '/tableau-de-bord', component: TableauDeBord},
  {path: '/tests', component: BancDeTests},
  {path: '/banc-de-tests', component: BancDeTests},
  {path: '/options', component: Parametres},
  {path: '/parametres', component: Parametres},
  {path: '/connexion', name:'connexion', component: Login}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router

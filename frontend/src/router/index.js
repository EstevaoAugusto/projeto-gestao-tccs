import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/tccs', name: 'tccs', component: () => import('@/views/TccsView.vue') },
    { path: '/alunos', name: 'alunos', component: () => import('@/views/AlunosView.vue') },
    { path: '/professores', name: 'professores', component: () => import('@/views/ProfessoresView.vue') },
    { path: '/cursos', name: 'cursos', component: () => import('@/views/CursosView.vue') },
    { path: '/departamentos', name: 'departamentos', component: () => import('@/views/DepartamentosView.vue') },
    { path: '/unidades', name: 'unidades', component: () => import('@/views/UnidadesView.vue') },
  ],
})

export default router

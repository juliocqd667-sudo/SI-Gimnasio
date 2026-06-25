import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/usuarios',
    name: 'AdminUsuarios',
    component: () => import('../views/AdminUsuarios.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/finanzas',
    name: 'AdminFinanzas',
    component: () => import('../views/AdminFinanzas.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/clases',
    name: 'AdminClases',
    component: () => import('../views/AdminClases.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/promociones',
    name: 'AdminPromociones',
    component: () => import('../views/AdminPromociones.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/cliente/reservas',
    name: 'ClienteReservas',
    component: () => import('../views/ClienteReservas.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/cliente/rutina',
    name: 'ClienteRutina',
    component: () => import('../views/ClienteRutina.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/instructor/rutinas',
    name: 'InstructorRutinas',
    component: () => import('../views/InstructorRutinas.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/nutricionista/antecedentes',
    name: 'NutricionistaAntecedentes',
    component: () => import('../views/NutricionistaAntecedentes.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = (await import('../stores/auth')).useAuthStore()
  const role = authStore.userRole
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else if (to.meta.requiresAdmin && role !== 'superadmin' && role !== 'admin') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router

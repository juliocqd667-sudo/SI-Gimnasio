<template>
  <div id="app-layout" :class="{ 'has-sidebar': authStore.isAuthenticated && $route.path !== '/' }">
    <!-- SIDEBAR -->
    <aside v-if="authStore.isAuthenticated && $route.path !== '/'" class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-brand">
        <div class="brand-icon">⚡</div>
        <span v-if="!sidebarCollapsed" class="brand-name">NovaFit</span>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section-label" v-if="!sidebarCollapsed">PRINCIPAL</div>
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <span class="nav-icon">📊</span>
          <span v-if="!sidebarCollapsed" class="nav-text">Dashboard</span>
        </router-link>

        <!-- ADMINISTRACIÓN: SuperAdmin + Admin -->
        <template v-if="isSuperOrAdmin">
          <div class="nav-section-label" v-if="!sidebarCollapsed">ADMINISTRACIÓN</div>
          <router-link to="/admin/usuarios" class="nav-item" active-class="active">
            <span class="nav-icon">👥</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Usuarios</span>
          </router-link>
          <router-link to="/admin/finanzas" class="nav-item" active-class="active">
            <span class="nav-icon">💳</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Finanzas</span>
          </router-link>
          <router-link to="/admin/clases" class="nav-item" active-class="active">
            <span class="nav-icon">📅</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Clases</span>
          </router-link>
          <router-link to="/admin/promociones" class="nav-item" active-class="active">
            <span class="nav-icon">🎉</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Promociones</span>
          </router-link>
          <router-link to="/admin/reportes" class="nav-item" active-class="active">
            <span class="nav-icon">📊</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Reportes</span>
          </router-link>
        </template>

        <!-- ENTRENAMIENTO: SuperAdmin + Instructor -->
        <template v-if="role === 'superadmin' || role === 'instructor'">
          <div class="nav-section-label" v-if="!sidebarCollapsed">ENTRENAMIENTO</div>
          <router-link to="/instructor/rutinas" class="nav-item" active-class="active">
            <span class="nav-icon">🏋️</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Rutinas</span>
          </router-link>
        </template>

        <!-- MI GIMNASIO: SuperAdmin + Cliente -->
        <template v-if="role === 'superadmin' || role === 'cliente'">
          <div class="nav-section-label" v-if="!sidebarCollapsed">MI GIMNASIO</div>
          <router-link to="/cliente/reservas" class="nav-item" active-class="active">
            <span class="nav-icon">📅</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Reservas</span>
          </router-link>
          <router-link to="/cliente/rutina" class="nav-item" active-class="active">
            <span class="nav-icon">💪</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Mi Rutina</span>
          </router-link>
        </template>

        <!-- SALUD: SuperAdmin + Nutricionista -->
        <template v-if="role === 'superadmin' || role === 'nutricionista'">
          <div class="nav-section-label" v-if="!sidebarCollapsed">SALUD</div>
          <router-link to="/nutricionista/antecedentes" class="nav-item" active-class="active">
            <span class="nav-icon">🥗</span>
            <span v-if="!sidebarCollapsed" class="nav-text">Antecedentes</span>
          </router-link>
        </template>
      </nav>

      <div class="sidebar-footer">
        <!-- Theme Toggle -->
        <button class="nav-item theme-toggle" @click="authStore.toggleTheme()">
          <span class="nav-icon">{{ authStore.theme === 'dark' ? '☀️' : '🌙' }}</span>
          <span v-if="!sidebarCollapsed" class="nav-text">{{ authStore.theme === 'dark' ? 'Modo Claro' : 'Modo Oscuro' }}</span>
        </button>

        <button class="nav-item collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
          <span class="nav-icon">{{ sidebarCollapsed ? '▶' : '◀' }}</span>
          <span v-if="!sidebarCollapsed" class="nav-text">Colapsar</span>
        </button>

        <div class="user-card" v-if="authStore.user">
          <div class="user-avatar" :class="{ 'super-avatar': role === 'superadmin' }">{{ (authStore.user.first_name || 'U')[0] }}</div>
          <div v-if="!sidebarCollapsed" class="user-info">
            <span class="user-name">{{ authStore.user.first_name }}</span>
            <span class="user-role" :class="{ 'super-role': role === 'superadmin' }">{{ roleName }}</span>
          </div>
        </div>

        <button class="nav-item logout-btn" @click="logout">
          <span class="nav-icon">🚪</span>
          <span v-if="!sidebarCollapsed" class="nav-text">Cerrar Sesión</span>
        </button>
      </div>
    </aside>

    <!-- TOPBAR (Home/Login) -->
    <nav v-if="!authStore.isAuthenticated || $route.path === '/'" class="topbar glass-panel">
      <div class="topbar-brand">
        <span class="brand-icon">⚡</span>
        <span class="text-gradient">NovaFit</span>
      </div>
      <div class="topbar-links">
        <router-link to="/" class="topbar-link">Inicio</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="topbar-link">Panel</router-link>
        <button class="btn btn-outline btn-sm" @click="authStore.toggleTheme()">{{ authStore.theme === 'dark' ? '☀️' : '🌙' }}</button>
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="btn btn-primary btn-sm">Iniciar Sesión</router-link>
        <button v-else @click="logout" class="btn btn-outline btn-sm">Cerrar Sesión</button>
      </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main class="main-content" :class="{ 'with-sidebar': authStore.isAuthenticated && $route.path !== '/', 'sidebar-collapsed': sidebarCollapsed }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const sidebarCollapsed = ref(false)

const role = computed(() => authStore.userRole)
const isSuperOrAdmin = computed(() => role.value === 'superadmin' || role.value === 'admin')
const roleName = computed(() => {
  const r = role.value
  if (r === 'superadmin') return '⭐ SuperAdmin'
  if (r === 'admin') return 'Administrador'
  if (r === 'instructor') return 'Instructor'
  if (r === 'nutricionista') return 'Nutricionista'
  if (r === 'cliente') return 'Cliente'
  return 'Usuario'
})

onMounted(async () => {
  authStore.applyTheme()
  if (authStore.accessToken) await authStore.fetchUser()
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  position: fixed; left: 0; top: 0; bottom: 0;
  width: var(--sidebar-width); background: var(--bg-surface);
  border-right: 1px solid var(--border-color);
  display: flex; flex-direction: column; z-index: 50;
  transition: width 0.25s ease; overflow-x: hidden;
}
.sidebar.collapsed { width: var(--sidebar-collapsed); }

.sidebar-brand {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1.25rem 1rem; border-bottom: 1px solid var(--border-color); min-height: 60px;
}
.brand-icon { font-size: 1.5rem; }
.brand-name { font-size: 1.25rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; white-space: nowrap; }

.sidebar-nav { flex: 1; padding: 0.75rem 0.5rem; overflow-y: auto; }
.nav-section-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); padding: 1rem 0.75rem 0.4rem; font-weight: 600; }

.nav-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.6rem 0.75rem; margin-bottom: 2px;
  border-radius: var(--radius-sm); color: var(--text-secondary);
  text-decoration: none; font-size: 0.875rem; font-weight: 500;
  transition: all 0.15s ease; cursor: pointer;
  border: none; background: none; width: 100%; text-align: left;
  font-family: var(--font-main); white-space: nowrap;
}
.nav-item:hover { background: rgba(99,102,241,0.06); color: var(--text-primary); }
.nav-item.active { background: rgba(99,102,241,0.12); color: var(--accent-hover); }
.nav-icon { font-size: 1.1rem; width: 24px; text-align: center; flex-shrink: 0; }
.nav-text { overflow: hidden; }

.sidebar-footer { padding: 0.5rem; border-top: 1px solid var(--border-color); }
.collapse-btn { margin-bottom: 0.5rem; }
.theme-toggle { margin-bottom: 0.25rem; }

.user-card { display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 0.75rem; margin-bottom: 0.25rem; }
.user-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--accent-gradient); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.8rem; flex-shrink: 0; }
.super-avatar { background: linear-gradient(135deg, #f59e0b, #ef4444) !important; box-shadow: 0 0 12px rgba(245, 158, 11, 0.4); }
.user-info { display: flex; flex-direction: column; overflow: hidden; }
.user-name { font-size: 0.8rem; font-weight: 600; color: var(--text-primary); white-space: nowrap; }
.user-role { font-size: 0.65rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
.super-role { color: #f59e0b !important; font-weight: 700; }
.logout-btn:hover { color: var(--danger) !important; }

.topbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.75rem 1.5rem; margin: 1rem; position: sticky; top: 1rem; z-index: 40;
}
.topbar-brand { display: flex; align-items: center; gap: 0.5rem; font-size: 1.25rem; font-weight: 800; }
.topbar-links { display: flex; align-items: center; gap: 1rem; }
.topbar-link { color: var(--text-secondary); text-decoration: none; font-weight: 500; font-size: 0.9rem; transition: color 0.2s; }
.topbar-link:hover { color: var(--text-primary); }

.main-content { padding: 2rem; max-width: 1400px; margin: 0 auto; width: 100%; }
.main-content.with-sidebar { margin-left: var(--sidebar-width); width: calc(100% - var(--sidebar-width)); transition: margin-left 0.25s ease, width 0.25s ease; }
.main-content.with-sidebar.sidebar-collapsed { margin-left: var(--sidebar-collapsed); width: calc(100% - var(--sidebar-collapsed)); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

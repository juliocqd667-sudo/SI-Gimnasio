<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="login-brand">
        <span class="brand-icon-lg">⚡</span>
        <h2 class="text-gradient">NovaFit</h2>
        <p class="login-subtitle">Sistema de Gestión de Gimnasio</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label>Usuario</label>
          <input type="text" v-model="username" class="input-field" placeholder="ej. admin" required />
        </div>
        <div class="input-group">
          <label>Contraseña</label>
          <input type="password" v-model="password" class="input-field" placeholder="••••••••" required />
        </div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Iniciar Sesión' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref(''); const password = ref(''); const errorMsg = ref(''); const loading = ref(false)

const creds = [
  { label: '⭐ SuperAdmin', user: 'superadmin', pass: 'admin123', isSuper: true },
  { label: 'Admin', user: 'admin', pass: 'admin123' },
  { label: 'Cliente', user: 'cliente1', pass: 'cliente123' },
  { label: 'Instructor', user: 'instructor1', pass: 'instr123' },
  { label: 'Nutricionista', user: 'nutri1', pass: 'nutri123' }
]

const fillCreds = (c) => { username.value = c.user; password.value = c.pass }

const handleLogin = async () => {
  loading.value = true; errorMsg.value = ''
  try { await authStore.login(username.value, password.value); router.push('/dashboard') }
  catch { errorMsg.value = 'Credenciales incorrectas.' }
  finally { loading.value = false }
}
</script>

<style scoped>
.login-wrapper { display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 120px); }
.login-card { width: 100%; max-width: 420px; padding: 2.5rem 2rem; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: var(--radius-lg); }
.login-brand { text-align: center; margin-bottom: 2rem; }
.brand-icon-lg { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
.login-brand h2 { font-size: 1.75rem; }
.login-subtitle { color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.25rem; }
.login-form { display: flex; flex-direction: column; gap: 0.75rem; }
.login-btn { width: 100%; margin-top: 0.5rem; }
.error-msg { color: var(--danger); font-size: 0.8rem; text-align: center; }
.demo-box { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); }
.demo-box h4 { font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.cred-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
.cred-item { padding: 0.5rem 0.75rem; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: var(--radius-sm); cursor: pointer; transition: border-color 0.2s; }
.cred-item:hover { border-color: var(--accent-color); }
.cred-role { display: block; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; }
.cred-user { font-size: 0.85rem; font-weight: 600; color: var(--accent-hover); }
.cred-super { border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.08); grid-column: 1 / -1; }
.cred-super:hover { border-color: #f59e0b; box-shadow: 0 0 12px rgba(245, 158, 11, 0.2); }
.cred-super .cred-role { color: #f59e0b; }
.cred-super .cred-user { color: #fbbf24; }
</style>

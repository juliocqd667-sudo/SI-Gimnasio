<template>
  <div class="dashboard animate-fade-in" v-if="authStore.user">
    <header class="page-header">
      <div>
        <h1>Bienvenido, {{ authStore.user.first_name }} 👋</h1>
        <p class="page-subtitle">Panel de {{ roleName }} — {{ todayStr }}</p>
      </div>
    </header>

    <!-- ═══════════ ADMIN DASHBOARD ═══════════ -->
    <template v-if="isAdmin">
      <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-icon blue">👥</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalUsers }}</span><span class="kpi-label">Usuarios</span></div></div>
        <div class="kpi-card"><div class="kpi-icon green">✅</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalClientes }}</span><span class="kpi-label">Clientes</span></div></div>
        <div class="kpi-card"><div class="kpi-icon purple">💰</div><div class="kpi-data"><span class="kpi-value">${{ stats.ingresos.toFixed(0) }}</span><span class="kpi-label">Ingresos</span></div></div>
        <div class="kpi-card"><div class="kpi-icon orange">📅</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalHorarios }}</span><span class="kpi-label">Horarios</span></div></div>
        <div class="kpi-card"><div class="kpi-icon cyan">🏋️</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalRutinas }}</span><span class="kpi-label">Rutinas</span></div></div>
        <div class="kpi-card"><div class="kpi-icon red">🩺</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalAntecedentes }}</span><span class="kpi-label">Consultas</span></div></div>
      </div>

      <div class="grid-2">
        <!-- Últimos Pagos -->
        <div class="section-panel">
          <div class="section-header"><h3>💳 Últimos Pagos</h3></div>
          <table class="data-table">
            <thead><tr><th>Fecha</th><th>Monto</th><th>Estado</th></tr></thead>
            <tbody>
              <tr v-for="p in ultimosPagos" :key="p.id">
                <td>{{ p.fecha }}</td>
                <td class="font-mono">${{ p.monto_total }}</td>
                <td><span class="badge badge-success">{{ p.estado_pago || 'Pagado' }}</span></td>
              </tr>
              <tr v-if="ultimosPagos.length === 0"><td colspan="3" class="empty-state">Sin pagos recientes</td></tr>
            </tbody>
          </table>
        </div>

        <!-- Clases de Hoy -->
        <div class="section-panel">
          <div class="section-header"><h3>📅 Horarios Programados</h3></div>
          <div class="today-classes">
            <div v-for="h in horarios.slice(0, 6)" :key="h.id" class="class-pill">
              <span class="pill-time">{{ formatTime(h.hora_inicial) }}</span>
              <span class="pill-name">{{ getDisciplinaNombre(h.disciplina) }}</span>
              <span class="pill-day">{{ h.dia }}</span>
            </div>
            <div v-if="horarios.length === 0" class="empty-state">No hay horarios programados</div>
          </div>
        </div>
      </div>
    </template>

    <!-- ═══════════ CLIENTE DASHBOARD ═══════════ -->
    <template v-if="role === 'cliente'">
      <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-icon blue">📅</div><div class="kpi-data"><span class="kpi-value">{{ misReservas.length }}</span><span class="kpi-label">Mis Reservas</span></div></div>
        <div class="kpi-card"><div class="kpi-icon green">💪</div><div class="kpi-data"><span class="kpi-value">{{ misRutinas.length }}</span><span class="kpi-label">Rutinas</span></div></div>
        <div class="kpi-card"><div class="kpi-icon purple">🩺</div><div class="kpi-data"><span class="kpi-value">{{ misAntecedentes.length }}</span><span class="kpi-label">Consultas</span></div></div>
      </div>
      <div class="grid-2">
        <div class="section-panel">
          <div class="section-header"><h3>📅 Próximas Clases</h3><router-link to="/cliente/reservas" class="btn btn-outline btn-sm">Ver Todas</router-link></div>
          <div class="today-classes">
            <div v-for="h in horarios.slice(0, 4)" :key="h.id" class="class-pill">
              <span class="pill-time">{{ formatTime(h.hora_inicial) }}</span>
              <span class="pill-name">{{ getDisciplinaNombre(h.disciplina) }}</span>
              <span class="pill-day">{{ h.dia }}</span>
            </div>
          </div>
        </div>
        <div class="section-panel">
          <div class="section-header"><h3>💪 Mi Rutina</h3><router-link to="/cliente/rutina" class="btn btn-outline btn-sm">Ver Detalles</router-link></div>
          <div v-for="r in misRutinas.slice(0, 2)" :key="r.id" class="rutina-mini">
            <strong>{{ r.nombre }}</strong><br><small>{{ r.descripcion }}</small>
          </div>
          <div v-if="misRutinas.length === 0" class="empty-state">Sin rutinas asignadas</div>
        </div>
      </div>
    </template>

    <!-- ═══════════ INSTRUCTOR DASHBOARD ═══════════ -->
    <template v-if="role === 'instructor'">
      <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-icon blue">🏋️</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalRutinas }}</span><span class="kpi-label">Rutinas Creadas</span></div></div>
        <div class="kpi-card"><div class="kpi-icon green">👥</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalClientes }}</span><span class="kpi-label">Clientes Activos</span></div></div>
        <div class="kpi-card"><div class="kpi-icon orange">📋</div><div class="kpi-data"><span class="kpi-value">{{ seguimientos.length }}</span><span class="kpi-label">Seguimientos</span></div></div>
      </div>
      <div class="grid-2">
        <div class="section-panel">
          <div class="section-header"><h3>🏋️ Rutinas</h3><router-link to="/instructor/rutinas" class="btn btn-outline btn-sm">Gestionar</router-link></div>
          <div v-for="r in rutinas.slice(0, 4)" :key="r.id" class="rutina-mini"><strong>{{ r.nombre }}</strong><br><small>{{ r.descripcion }}</small></div>
        </div>
        <div class="section-panel">
          <div class="section-header"><h3>📋 Últimos Seguimientos</h3></div>
          <div v-for="s in seguimientos.slice(0, 4)" :key="s.id" class="rutina-mini"><strong>{{ s.objetivo }}</strong><br><small>{{ s.fecha }} — {{ s.observaciones.substring(0, 60) }}...</small></div>
        </div>
      </div>
    </template>

    <!-- ═══════════ NUTRICIONISTA DASHBOARD ═══════════ -->
    <template v-if="role === 'nutricionista'">
      <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-icon green">🩺</div><div class="kpi-data"><span class="kpi-value">{{ antecedentes.length }}</span><span class="kpi-label">Consultas Registradas</span></div></div>
        <div class="kpi-card"><div class="kpi-icon blue">👥</div><div class="kpi-data"><span class="kpi-value">{{ stats.totalClientes }}</span><span class="kpi-label">Pacientes</span></div></div>
      </div>
      <div class="section-panel">
        <div class="section-header"><h3>🩺 Últimas Consultas</h3><router-link to="/nutricionista/antecedentes" class="btn btn-outline btn-sm">Registrar Nueva</router-link></div>
        <table class="data-table">
          <thead><tr><th>Fecha</th><th>Peso</th><th>IMC</th><th>Diagnóstico</th></tr></thead>
          <tbody>
            <tr v-for="a in antecedentes.slice(0, 5)" :key="a.id">
              <td>{{ a.fecha }}</td><td>{{ a.peso }}kg</td><td>{{ a.imc }}</td><td>{{ a.diagnostico.substring(0, 50) }}...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
  <div v-else class="loading-state"><p>Cargando perfil...</p></div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
import API from '../api'

const authStore = useAuthStore()
const config = computed(() => ({ headers: { Authorization: `Bearer ${authStore.accessToken}` } }))

const role = computed(() => authStore.userRole)
const isAdmin = computed(() => role.value === 'admin' || role.value === 'superadmin')
const roleName = computed(() => {
  if (role.value === 'superadmin') return '⭐ SuperAdmin'
  if (role.value === 'admin') return 'Administración'
  if (role.value === 'instructor') return 'Instructor'
  if (role.value === 'nutricionista') return 'Nutrición'
  return 'Cliente'
})
const todayStr = new Date().toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' })

const stats = ref({ totalUsers: 0, totalClientes: 0, ingresos: 0, totalHorarios: 0, totalRutinas: 0, totalAntecedentes: 0 })
const ultimosPagos = ref([])
const horarios = ref([])
const disciplinas = ref([])
const rutinas = ref([])
const seguimientos = ref([])
const antecedentes = ref([])
const misReservas = ref([])
const misRutinas = ref([])
const misAntecedentes = ref([])

const formatTime = (t) => t ? t.substring(0, 5) : ''
const getDisciplinaNombre = (id) => { const d = disciplinas.value.find(x => x.id === id); return d ? d.nombre : `#${id}` }

onMounted(async () => {
  try {
    const c = config.value
    const [resU, resP, resH, resD, resR, resA, resSeg, resC] = await Promise.all([
      axios.get(`${API}/users/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/pagos/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/horarios/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/disciplinas/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/rutinas/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/antecedentes/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/seguimientos/`, c).catch(() => ({ data: [] })),
      axios.get(`${API}/clientes/`, c).catch(() => ({ data: [] }))
    ])
    
    disciplinas.value = resD.data
    horarios.value = resH.data
    rutinas.value = resR.data
    antecedentes.value = resA.data
    seguimientos.value = resSeg.data
    
    stats.value = {
      totalUsers: resU.data.length,
      totalClientes: resU.data.filter(u => u.is_cliente).length,
      ingresos: resP.data.reduce((s, p) => s + parseFloat(p.monto_total || 0), 0),
      totalHorarios: resH.data.length,
      totalRutinas: resR.data.length,
      totalAntecedentes: resA.data.length
    }
    ultimosPagos.value = resP.data.slice().reverse().slice(0, 6)

    // Client-specific
    if (role.value === 'cliente') {
      const me = resC.data.find(c => c.user?.id === authStore.user.id)
      if (me) {
        const resRes = await axios.get(`${API}/reservas/`, c).catch(() => ({ data: [] }))
        misReservas.value = resRes.data.filter(r => r.cliente === me.user.id)
        misRutinas.value = resR.data // All rutinas visible
        misAntecedentes.value = resA.data.filter(a => a.cliente === me.user.id)
      }
    }
  } catch (e) { console.error(e) }
})
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.25rem; text-transform: capitalize; }
.font-mono { font-family: 'SF Mono', monospace; }
.loading-state { display: flex; justify-content: center; align-items: center; min-height: 50vh; color: var(--text-secondary); }

.today-classes { display: flex; flex-direction: column; gap: 0.5rem; }
.class-pill {
  display: flex; align-items: center; gap: 1rem; padding: 0.65rem 0.9rem;
  background: rgba(0,0,0,0.2); border-radius: var(--radius-sm); border: 1px solid var(--border-color);
}
.pill-time { font-weight: 700; color: var(--accent-hover); font-size: 0.85rem; min-width: 45px; }
.pill-name { flex: 1; font-weight: 500; }
.pill-day { font-size: 0.75rem; color: var(--text-secondary); }

.rutina-mini { padding: 0.75rem; background: rgba(0,0,0,0.15); border-radius: var(--radius-sm); margin-bottom: 0.5rem; border: 1px solid var(--border-color); }
.rutina-mini strong { color: var(--accent-hover); font-size: 0.9rem; }
.rutina-mini small { color: var(--text-secondary); font-size: 0.8rem; }
</style>

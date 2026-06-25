<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Mi Rutina de Entrenamiento</h1><p class="page-subtitle">Sigue tu progreso y alcanza tus metas.</p></div>
    </header>

    <!-- Rutinas con ejercicios reales -->
    <div v-for="r in rutinas" :key="r.id" class="section-panel" style="margin-bottom:1.5rem;">
      <div class="section-header">
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <h3>{{ r.nombre }}</h3>
          <span class="badge badge-success">Activa</span>
        </div>
      </div>
      <p style="color:var(--text-secondary); font-size:0.85rem; margin-bottom:1rem;">{{ r.descripcion }}</p>

      <div class="exercise-grid" v-if="getDetalles(r.id).length > 0">
        <div v-for="det in getDetalles(r.id)" :key="det.id" class="exercise-card">
          <div class="ex-icon">🏋️</div>
          <div class="ex-body">
            <h4>{{ getEjercicioNombre(det.ejercicio) }}</h4>
            <div class="ex-stats">
              <div class="ex-stat"><span class="stat-val">{{ det.serie }}</span><span class="stat-label">Series</span></div>
              <div class="ex-stat"><span class="stat-val">{{ det.repeticiones }}</span><span class="stat-label">Reps</span></div>
              <div class="ex-stat"><span class="stat-val">{{ det.peso }}kg</span><span class="stat-label">Peso</span></div>
            </div>
          </div>
          <div class="ex-day"><span class="badge badge-info">{{ det.dia }}</span></div>
        </div>
      </div>
      <div v-else class="empty-state">Ejercicios pendientes de asignación por tu instructor.</div>
    </div>

    <div v-if="rutinas.length === 0" class="section-panel">
      <div class="empty-state">No tienes rutinas asignadas. Habla con tu instructor.</div>
    </div>

    <!-- Seguimientos -->
    <div class="section-panel" v-if="seguimientos.length > 0">
      <div class="section-header"><h3>📋 Historial de Seguimiento</h3></div>
      <table class="data-table">
        <thead><tr><th>Fecha</th><th>Objetivo</th><th>Observaciones</th><th>Próx. Consulta</th></tr></thead>
        <tbody>
          <tr v-for="s in seguimientos" :key="s.id">
            <td>{{ s.fecha }}</td><td>{{ s.objetivo }}</td><td style="max-width:300px;">{{ s.observaciones }}</td><td>{{ s.fecha_prox_consulta }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import API from '../api'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
const cfg = () => ({ headers: { Authorization: `Bearer ${authStore.accessToken}` } })

const rutinas = ref([]); const detalles = ref([]); const ejercicios = ref([]); const seguimientos = ref([])

const getDetalles = (rutinaId) => detalles.value.filter(d => d.rutina === rutinaId)
const getEjercicioNombre = (id) => { const e = ejercicios.value.find(x => x.id === id); return e ? e.nombre : `Ejercicio #${id}` }

onMounted(async () => {
  const [resR, resDet, resEj, resSeg, resC] = await Promise.all([
    axios.get(`${API}/rutinas/`, cfg()), axios.get(`${API}/detalles-rutina/`, cfg()),
    axios.get(`${API}/ejercicios/`, cfg()), axios.get(`${API}/seguimientos/`, cfg()),
    axios.get(`${API}/clientes/`, cfg())
  ])
  rutinas.value = resR.data; detalles.value = resDet.data; ejercicios.value = resEj.data
  const me = resC.data.find(c => c.user?.id === authStore.user.id)
  if (me) seguimientos.value = resSeg.data.filter(s => s.cliente === me.user.id)
})
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }

.exercise-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; }
.exercise-card { display: flex; align-items: center; gap: 0.75rem; padding: 1rem; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: var(--radius-md); transition: border-color 0.2s; }
.exercise-card:hover { border-color: var(--border-active); }
.ex-icon { font-size: 1.5rem; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: rgba(99,102,241,0.1); border-radius: var(--radius-sm); flex-shrink: 0; }
.ex-body { flex: 1; }
.ex-body h4 { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
.ex-stats { display: flex; gap: 0.75rem; }
.ex-stat { display: flex; flex-direction: column; align-items: center; }
.stat-val { font-size: 0.95rem; font-weight: 700; color: var(--accent-hover); }
.stat-label { font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; }
.ex-day { flex-shrink: 0; }
</style>

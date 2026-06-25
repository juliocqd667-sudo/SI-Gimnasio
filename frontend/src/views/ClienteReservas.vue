<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Mis Reservas</h1><p class="page-subtitle">Explora clases disponibles y reserva tu cupo.</p></div>
    </header>

    <div class="grid-2">
      <!-- Clases Disponibles -->
      <div class="section-panel">
        <div class="section-header"><h3>📅 Clases Disponibles</h3></div>
        <div class="booking-grid">
          <div v-for="h in horarios" :key="h.id" class="booking-card">
            <div class="booking-color" :style="{ background: getColor(h.disciplina) }"></div>
            <div class="booking-body">
              <h4>{{ getDisciplinaNombre(h.disciplina) }}</h4>
              <div class="booking-meta">
                <span>📅 {{ h.dia }}</span>
                <span>⏰ {{ formatTime(h.hora_inicial) }} - {{ formatTime(h.hora_final) }}</span>
              </div>
              <div class="booking-cupo">
                <div class="cupo-bar"><div class="cupo-fill" :style="{ width: getCupoPercent(h.disciplina) + '%' }"></div></div>
                <span class="cupo-text">{{ getCupoDisp(h.disciplina) }} cupos disp.</span>
              </div>
            </div>
            <button class="btn btn-sm" :class="yaReservado(h.disciplina) ? 'btn-success' : 'btn-primary'" @click="reservar(h)" :disabled="yaReservado(h.disciplina)">
              {{ yaReservado(h.disciplina) ? '✓' : 'Reservar' }}
            </button>
          </div>
          <div v-if="horarios.length === 0" class="empty-state">No hay clases programadas.</div>
        </div>
      </div>

      <!-- Mis Reservas -->
      <div class="section-panel">
        <div class="section-header"><h3>🎟️ Mis Reservas ({{ misReservas.length }})</h3></div>
        <div v-for="r in misReservas" :key="r.id" class="reserva-item">
          <div>
            <strong>{{ getDisciplinaNombre(r.disciplina) }}</strong>
            <div class="reserva-meta">
              <span class="badge badge-success">{{ r.estado === 'A' ? 'Activa' : r.estado }}</span>
              <span>{{ r.fecha }}</span>
            </div>
          </div>
          <button class="btn btn-danger btn-sm" @click="cancelar(r.id)">Cancelar</button>
        </div>
        <div v-if="misReservas.length === 0" class="empty-state">No tienes reservas activas.</div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast" class="toast" :class="toast.type">{{ toast.msg }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import API from '../api'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
const cfg = () => ({ headers: { Authorization: `Bearer ${authStore.accessToken}` } })

const horarios = ref([]); const disciplinas = ref([]); const reservas = ref([]); const myClientId = ref(null)
const toast = ref(null)
const colors = ['#6366f1','#10b981','#f59e0b','#ef4444','#3b82f6','#a855f7','#06b6d4','#ec4899']
const getColor = (id) => colors[(id-1) % colors.length]
const formatTime = (t) => t ? t.substring(0,5) : ''
const getDisciplinaNombre = (id) => { const d = disciplinas.value.find(x => x.id === id); return d ? d.nombre : `#${id}` }
const getCupoDisp = (dId) => { const d = disciplinas.value.find(x => x.id === dId); return d ? d.cupo : 0 }
const getCupoPercent = (dId) => { const d = disciplinas.value.find(x => x.id === dId); return d ? Math.min(100, (reservas.value.filter(r => r.disciplina === dId).length / d.cupo) * 100) : 0 }

const misReservas = computed(() => myClientId.value ? reservas.value.filter(r => r.cliente === myClientId.value) : [])
const yaReservado = (dId) => misReservas.value.some(r => r.disciplina === dId)

const showToast = (msg, type = 'toast-success') => { toast.value = { msg, type }; setTimeout(() => toast.value = null, 3000) }

const fetchData = async () => {
  const [resH, resD, resR, resC] = await Promise.all([
    axios.get(`${API}/horarios/`, cfg()), axios.get(`${API}/disciplinas/`, cfg()),
    axios.get(`${API}/reservas/`, cfg()), axios.get(`${API}/clientes/`, cfg())
  ])
  horarios.value = resH.data; disciplinas.value = resD.data; reservas.value = resR.data
  const me = resC.data.find(c => c.user?.id === authStore.user.id)
  if (me) myClientId.value = me.id
}

const reservar = async (horario) => {
  if (!myClientId.value) return showToast('Sin perfil de cliente', 'toast-error')
  try {
    const resComp = await axios.get(`${API}/comprobantes/`, cfg())
    const comp = resComp.data.find(c => c.cliente === myClientId.value)
    if (!comp) return showToast('Necesitas un pago activo para reservar', 'toast-error')
    await axios.post(`${API}/reservas/`, { fecha: new Date().toISOString().split('T')[0], estado: 'A', cliente: myClientId.value, disciplina: horario.disciplina, comprobante: comp.id }, cfg())
    showToast('¡Reserva creada exitosamente!'); fetchData()
  } catch(e) { showToast('Error al reservar', 'toast-error') }
}

const cancelar = async (id) => {
  if (!confirm('¿Cancelar esta reserva?')) return
  await axios.delete(`${API}/reservas/${id}/`, cfg()); showToast('Reserva cancelada'); fetchData()
}
onMounted(fetchData)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }

.booking-grid { display: flex; flex-direction: column; gap: 0.75rem; }
.booking-card { display: flex; align-items: center; gap: 0.75rem; padding: 0.9rem; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: var(--radius-md); transition: border-color 0.2s; }
.booking-card:hover { border-color: var(--border-active); }
.booking-color { width: 4px; height: 50px; border-radius: 2px; flex-shrink: 0; }
.booking-body { flex: 1; }
.booking-body h4 { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.25rem; }
.booking-meta { display: flex; gap: 1rem; font-size: 0.78rem; color: var(--text-secondary); }
.booking-cupo { margin-top: 0.4rem; }
.cupo-bar { width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.cupo-fill { height: 100%; background: var(--accent-gradient); border-radius: 2px; transition: width 0.3s; }
.cupo-text { font-size: 0.7rem; color: var(--text-muted); }

.reserva-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; border-bottom: 1px solid var(--border-color); }
.reserva-meta { display: flex; gap: 0.5rem; align-items: center; margin-top: 0.25rem; font-size: 0.78rem; color: var(--text-secondary); }
</style>

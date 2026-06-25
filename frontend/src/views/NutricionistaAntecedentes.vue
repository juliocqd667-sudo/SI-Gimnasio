<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Antecedentes Clínicos</h1><p class="page-subtitle">Registra mediciones y diagnósticos nutricionales.</p></div>
    </header>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-icon green">🩺</div><div class="kpi-data"><span class="kpi-value">{{ antecedentes.length }}</span><span class="kpi-label">Consultas</span></div></div>
      <div class="kpi-card"><div class="kpi-icon blue">👥</div><div class="kpi-data"><span class="kpi-value">{{ clientes.length }}</span><span class="kpi-label">Pacientes</span></div></div>
    </div>

    <!-- Formulario -->
    <div class="section-panel" style="margin-bottom:1.5rem;">
      <div class="section-header"><h3>📝 Registrar Nuevo Antecedente</h3></div>
      <form @submit.prevent="guardar" style="display:flex; flex-direction:column; gap:0.75rem;">
        <div class="grid-2">
          <div class="input-group"><label>Cliente</label><select v-model="form.cliente" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.user.first_name }} {{ c.user.last_name }}</option></select></div>
          <div class="input-group"><label>Fecha</label><input type="date" v-model="form.fecha" class="input-field" required></div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem;">
          <div class="input-group"><label>Peso (kg)</label><input type="number" step="0.1" v-model="form.peso" class="input-field" @input="calcIMC" required></div>
          <div class="input-group"><label>Altura (cm)</label><input type="number" v-model="form.altura" class="input-field" @input="calcIMC" required></div>
          <div class="input-group">
            <label>IMC</label>
            <div class="imc-display">
              <span class="imc-value" :style="{ color: imcColor }">{{ form.imc || '—' }}</span>
              <span class="imc-label" :style="{ color: imcColor }">{{ imcLabel }}</span>
            </div>
            <!-- IMC Gauge -->
            <div class="imc-gauge">
              <div class="gauge-track">
                <div class="gauge-fill" :style="{ width: imcPercent + '%', background: imcColor }"></div>
              </div>
              <div class="gauge-labels"><span>15</span><span>18.5</span><span>25</span><span>30</span><span>40</span></div>
            </div>
          </div>
        </div>
        <div class="grid-2">
          <div class="input-group"><label>Diagnóstico</label><textarea v-model="form.diagnostico" class="input-field" rows="2" required></textarea></div>
          <div class="input-group"><label>Recomendaciones</label><textarea v-model="form.recomendaciones" class="input-field" rows="2" required></textarea></div>
        </div>
        <div class="grid-2">
          <div class="input-group"><label>Objetivo</label><input v-model="form.objetivo" class="input-field" required></div>
          <div class="input-group"><label>Próxima Consulta</label><input type="date" v-model="form.proxima" class="input-field" required></div>
        </div>
        <div style="text-align:right;"><button type="submit" class="btn btn-primary">Guardar Registro</button></div>
      </form>
    </div>

    <!-- Historial -->
    <div class="section-panel">
      <div class="section-header"><h3>📋 Historial de Consultas</h3></div>
      <table class="data-table">
        <thead><tr><th>Fecha</th><th>Paciente</th><th>Peso</th><th>IMC</th><th>Clasificación</th><th>Diagnóstico</th><th>Próx. Cita</th><th>Acción</th></tr></thead>
        <tbody>
          <tr v-for="a in antecedentes.slice().reverse()" :key="a.id">
            <td>{{ a.fecha }}</td>
            <td>{{ getClienteNombre(a.cliente) }}</td>
            <td>{{ a.peso }}kg</td>
            <td><strong>{{ a.imc }}</strong></td>
            <td><span class="badge" :class="imcBadge(a.imc)">{{ imcClassify(a.imc) }}</span></td>
            <td style="max-width:200px;">{{ a.diagnostico }}</td>
            <td>{{ a.fecha_prox_consulta }}</td>
            <td><button class="btn btn-danger btn-sm" @click="eliminar(a.id)">×</button></td>
          </tr>
          <tr v-if="antecedentes.length === 0"><td colspan="8" class="empty-state">Sin antecedentes registrados.</td></tr>
        </tbody>
      </table>
    </div>

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

const clientes = ref([]); const antecedentes = ref([]); const myNutriId = ref(null)
const toast = ref(null)
const showToast = (msg, type='toast-success') => { toast.value = { msg, type }; setTimeout(() => toast.value = null, 3000) }

const form = ref({ cliente:'', fecha: new Date().toISOString().split('T')[0], peso:'', altura:'', imc:'', diagnostico:'', recomendaciones:'', objetivo:'', proxima:'' })

const calcIMC = () => { if(form.value.peso && form.value.altura) { const h = form.value.altura/100; form.value.imc = (form.value.peso/(h*h)).toFixed(1) } }
const imcLabel = computed(() => imcClassify(parseFloat(form.value.imc)))
const imcColor = computed(() => { const v=parseFloat(form.value.imc); if(!v) return '#64748b'; if(v<18.5) return '#3b82f6'; if(v<25) return '#10b981'; if(v<30) return '#f59e0b'; return '#ef4444' })
const imcPercent = computed(() => { const v=parseFloat(form.value.imc); if(!v) return 0; return Math.min(100, ((v-15)/(40-15))*100) })

const imcClassify = (v) => { v = parseFloat(v); if(!v) return '—'; if(v<18.5) return 'Bajo Peso'; if(v<25) return 'Normal'; if(v<30) return 'Sobrepeso'; return 'Obesidad' }
const imcBadge = (v) => { v = parseFloat(v); if(v<18.5) return 'badge-info'; if(v<25) return 'badge-success'; if(v<30) return 'badge-warning'; return 'badge-danger' }
const getClienteNombre = (id) => { const c = clientes.value.find(x => x.id === id); return c ? `${c.user.first_name} ${c.user.last_name}` : `#${id}` }

const fetchData = async () => {
  const [resC, resA, resN] = await Promise.all([
    axios.get(`${API}/clientes/`, cfg()), axios.get(`${API}/antecedentes/`, cfg()), axios.get(`${API}/nutricionistas/`, cfg())
  ])
  clientes.value = resC.data; antecedentes.value = resA.data
  const me = resN.data.find(n => n.user?.id === authStore.user.id)
  if (me) myNutriId.value = me.id
}

const guardar = async () => {
  const nutriId = myNutriId.value || 1 // Fallback para superadmin u otros
  if (!myNutriId.value && authStore.userRole !== 'superadmin') return showToast('Sin perfil de nutricionista', 'toast-error')
  try {
    await axios.post(`${API}/antecedentes/`, {
      fecha: form.value.fecha, diagnostico: form.value.diagnostico, recomendaciones: form.value.recomendaciones,
      objetivo: form.value.objetivo, peso: parseFloat(form.value.peso), altura: parseFloat(form.value.altura),
      imc: parseFloat(form.value.imc), gc: 0, mm: 0, fecha_prox_consulta: form.value.proxima,
      cliente: form.value.cliente, nutricionista: nutriId
    }, cfg())
    showToast('Antecedente registrado'); form.value = { cliente:'', fecha: new Date().toISOString().split('T')[0], peso:'', altura:'', imc:'', diagnostico:'', recomendaciones:'', objetivo:'', proxima:'' }
    fetchData()
  } catch(e) { showToast('Error al guardar', 'toast-error') }
}

const eliminar = async (id) => {
  if (!confirm('¿Eliminar este antecedente?')) return
  await axios.delete(`${API}/antecedentes/${id}/`, cfg()); showToast('Antecedente eliminado'); fetchData()
}
onMounted(fetchData)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }

.imc-display { display: flex; align-items: baseline; gap: 0.5rem; padding: 0.5rem 0; }
.imc-value { font-size: 1.75rem; font-weight: 800; }
.imc-label { font-size: 0.8rem; font-weight: 600; }

.imc-gauge { margin-top: 0.25rem; }
.gauge-track { width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
.gauge-fill { height: 100%; border-radius: 3px; transition: all 0.4s ease; }
.gauge-labels { display: flex; justify-content: space-between; font-size: 0.6rem; color: var(--text-muted); margin-top: 0.15rem; }
</style>

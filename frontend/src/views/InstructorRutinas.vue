<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Gestión de Rutinas</h1><p class="page-subtitle">Crea rutinas, asigna ejercicios y monitorea alumnos.</p></div>
    </header>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-icon blue">🏋️</div><div class="kpi-data"><span class="kpi-value">{{ rutinas.length }}</span><span class="kpi-label">Rutinas</span></div></div>
      <div class="kpi-card"><div class="kpi-icon green">👥</div><div class="kpi-data"><span class="kpi-value">{{ clientes.length }}</span><span class="kpi-label">Clientes</span></div></div>
      <div class="kpi-card"><div class="kpi-icon orange">📋</div><div class="kpi-data"><span class="kpi-value">{{ seguimientos.length }}</span><span class="kpi-label">Seguimientos</span></div></div>
    </div>

    <div class="grid-2">
      <!-- Banco de Rutinas -->
      <div class="section-panel">
        <div class="section-header"><h3>🏋️ Banco de Rutinas</h3><button class="btn btn-primary btn-sm" @click="showModal = true">+ Nueva</button></div>
        <div v-for="r in rutinas" :key="r.id" class="rutina-item">
          <div><strong>{{ r.nombre }}</strong><br><small style="color:var(--text-secondary)">{{ r.descripcion }}</small></div>
          <div style="display:flex; gap:0.25rem;">
            <button class="btn btn-outline btn-sm" @click="openAddExercise(r)">+ Ejercicio</button>
            <button class="btn btn-danger btn-sm" @click="deleteRutina(r.id)">×</button>
          </div>
        </div>
        <div v-if="rutinas.length === 0" class="empty-state">Sin rutinas creadas.</div>
      </div>

      <!-- Seguimiento -->
      <div class="section-panel">
        <div class="section-header"><h3>📋 Asignar Seguimiento</h3></div>
        <form @submit.prevent="asignarRutina" style="display:flex; flex-direction:column; gap:0.75rem;">
          <div class="input-group"><label>Cliente</label><select v-model="asig.cliente" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.user.first_name }} {{ c.user.last_name }}</option></select></div>
          <div class="input-group"><label>Rutina</label><select v-model="asig.rutina" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="r in rutinas" :key="r.id" :value="r.id">{{ r.nombre }}</option></select></div>
          <div class="input-group"><label>Objetivo</label><input v-model="asig.objetivo" class="input-field" required></div>
          <div class="input-group"><label>Observaciones</label><textarea v-model="asig.observaciones" class="input-field" rows="2" required></textarea></div>
          <button type="submit" class="btn btn-primary" style="width:100%">Registrar Seguimiento</button>
        </form>

        <div v-if="seguimientos.length > 0" style="margin-top:1.5rem;">
          <h4 style="font-size:0.9rem; margin-bottom:0.75rem;">Últimos Seguimientos</h4>
          <div v-for="s in seguimientos.slice().reverse().slice(0,4)" :key="s.id" class="rutina-item">
            <div><strong>{{ getClienteNombre(s.cliente) }}</strong><br><small style="color:var(--text-secondary)">{{ s.objetivo }} — {{ s.fecha }}</small></div>
            <button class="btn btn-danger btn-sm" @click="deleteSeguimiento(s.id)">×</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Nueva Rutina -->
    <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
      <div class="modal-box">
        <h3>Crear Rutina</h3>
        <form @submit.prevent="crearRutina">
          <div class="input-group"><label>Nombre</label><input v-model="newRutina.nombre" class="input-field" required></div>
          <div class="input-group"><label>Descripción</label><textarea v-model="newRutina.descripcion" class="input-field" rows="2" required></textarea></div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showModal = false">Cancelar</button><button type="submit" class="btn btn-primary">Guardar</button></div>
        </form>
      </div>
    </div>

    <!-- Modal: Agregar Ejercicio a Rutina -->
    <div class="modal-overlay" v-if="showAddEx" @click.self="showAddEx = false">
      <div class="modal-box">
        <h3>Agregar Ejercicio a "{{ selectedRutina?.nombre }}"</h3>
        <form @submit.prevent="addExercise">
          <div class="input-group"><label>Ejercicio</label><select v-model="exForm.ejercicio" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="e in ejercicios" :key="e.id" :value="e.id">{{ e.nombre }}</option></select></div>
          <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Series</label><input v-model="exForm.serie" class="input-field" required></div>
            <div class="input-group"><label>Reps</label><input v-model="exForm.repeticiones" class="input-field" required></div>
            <div class="input-group"><label>Peso (kg)</label><input v-model="exForm.peso" class="input-field" required></div>
          </div>
          <div class="input-group"><label>Día</label><select v-model="exForm.dia" class="input-field" required><option v-for="d in ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']" :key="d" :value="d">{{ d }}</option></select></div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showAddEx = false">Cancelar</button><button type="submit" class="btn btn-primary">Agregar</button></div>
        </form>
      </div>
    </div>

    <div v-if="toast" class="toast" :class="toast.type">{{ toast.msg }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import API from '../api'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
const cfg = () => ({ headers: { Authorization: `Bearer ${authStore.accessToken}` } })

const rutinas = ref([]); const clientes = ref([]); const seguimientos = ref([]); const ejercicios = ref([])
const showModal = ref(false); const showAddEx = ref(false); const selectedRutina = ref(null)
const newRutina = ref({ nombre:'', descripcion:'' })
const asig = ref({ cliente:'', rutina:'', objetivo:'', observaciones:'' })
const exForm = ref({ ejercicio:'', serie:'4', repeticiones:'10', peso:'20', dia:'Lunes' })
const toast = ref(null)
const showToast = (msg, type='toast-success') => { toast.value = { msg, type }; setTimeout(() => toast.value = null, 3000) }

const getClienteNombre = (id) => { const c = clientes.value.find(x => x.id === id); return c ? `${c.user.first_name} ${c.user.last_name}` : `#${id}` }

const fetchData = async () => {
  const [resR, resC, resS, resE] = await Promise.all([
    axios.get(`${API}/rutinas/`, cfg()), axios.get(`${API}/clientes/`, cfg()),
    axios.get(`${API}/seguimientos/`, cfg()), axios.get(`${API}/ejercicios/`, cfg())
  ])
  rutinas.value = resR.data; clientes.value = resC.data; seguimientos.value = resS.data; ejercicios.value = resE.data
}

const crearRutina = async () => {
  await axios.post(`${API}/rutinas/`, newRutina.value, cfg()); showModal.value = false
  newRutina.value = { nombre:'', descripcion:'' }; showToast('Rutina creada'); fetchData()
}
const deleteRutina = async (id) => {
  if (!confirm('¿Eliminar esta rutina permanentemente?')) return
  await axios.delete(`${API}/rutinas/${id}/`, cfg()); showToast('Rutina eliminada'); fetchData()
}

const openAddExercise = (r) => { selectedRutina.value = r; showAddEx.value = true }
const addExercise = async () => {
  await axios.post(`${API}/detalles-rutina/`, { rutina: selectedRutina.value.id, ...exForm.value }, cfg())
  showAddEx.value = false; exForm.value = { ejercicio:'', serie:'4', repeticiones:'10', peso:'20', dia:'Lunes' }
  showToast('Ejercicio agregado')
}

const asignarRutina = async () => {
  const resI = await axios.get(`${API}/instructores/`, cfg())
  const me = resI.data.find(i => i.user?.id === authStore.user.id)
  const instructorId = me ? me.id : 1 // Fallback para superadmin u otros
  if (!me && authStore.userRole !== 'superadmin') return showToast('Sin perfil de instructor', 'toast-error')
  await axios.post(`${API}/seguimientos/`, {
    fecha: new Date().toISOString().split('T')[0], observaciones: asig.value.observaciones,
    objetivo: asig.value.objetivo, fecha_prox_consulta: new Date(Date.now() + 15*86400000).toISOString().split('T')[0],
    cliente: asig.value.cliente, instructor: instructorId, rutina: asig.value.rutina
  }, cfg())
  asig.value = { cliente:'', rutina:'', objetivo:'', observaciones:'' }; showToast('Seguimiento registrado'); fetchData()
}
const deleteSeguimiento = async (id) => {
  if (!confirm('¿Eliminar este seguimiento?')) return
  await axios.delete(`${API}/seguimientos/${id}/`, cfg()); showToast('Seguimiento eliminado'); fetchData()
}
onMounted(fetchData)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }
.rutina-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; border-bottom: 1px solid var(--border-color); }
.rutina-item strong { color: var(--accent-hover); font-size: 0.9rem; }
</style>

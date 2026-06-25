<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Gestión de Clases y Horarios</h1><p class="page-subtitle">Programa disciplinas y horarios del gimnasio.</p></div>
    </header>

    <!-- Calendario Visual Semanal -->
    <div class="section-panel" style="margin-bottom:1.5rem;">
      <div class="section-header"><h3>📅 Vista Semanal</h3></div>
      <div class="calendar-grid">
        <div v-for="day in weekDays" :key="day" class="calendar-col">
          <div class="cal-day-header">{{ day }}</div>
          <div v-for="h in getHorariosByDay(day)" :key="h.id" class="cal-block" :style="{ borderLeftColor: getColor(h.disciplina) }">
            <span class="cal-time">{{ formatTime(h.hora_inicial) }} - {{ formatTime(h.hora_final) }}</span>
            <span class="cal-name">{{ getDisciplinaNombre(h.disciplina) }}</span>
          </div>
          <div v-if="getHorariosByDay(day).length === 0" class="cal-empty">—</div>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <!-- Disciplinas -->
      <div class="section-panel">
        <div class="section-header"><h3>🏅 Disciplinas</h3><button class="btn btn-primary btn-sm" @click="showModalD = true">+ Añadir</button></div>
        <table class="data-table">
          <thead><tr><th>Nombre</th><th>Grupo</th><th>Cupo</th><th>Sala</th><th>Acción</th></tr></thead>
          <tbody>
            <tr v-for="d in disciplinas" :key="d.id">
              <td><strong>{{ d.nombre }}</strong></td><td>{{ d.grupo }}</td><td>{{ d.cupo }}</td><td>{{ getSalaNombre(d.sala) }}</td>
              <td style="display:flex; gap:0.25rem;">
                <button class="btn btn-outline btn-sm" @click="editDisciplina(d)">✎</button>
                <button class="btn btn-danger btn-sm" @click="deleteDisciplina(d.id)">×</button>
              </td>
            </tr>
            <tr v-if="disciplinas.length === 0"><td colspan="5" class="empty-state">Sin disciplinas</td></tr>
          </tbody>
        </table>
      </div>

      <!-- Horarios -->
      <div class="section-panel">
        <div class="section-header"><h3>⏰ Horarios</h3><button class="btn btn-primary btn-sm" @click="showModalH = true">+ Programar</button></div>
        <table class="data-table">
          <thead><tr><th>Día</th><th>Inicio</th><th>Fin</th><th>Disciplina</th><th>Instructor</th><th>Acción</th></tr></thead>
          <tbody>
            <tr v-for="h in horarios" :key="h.id">
              <td>{{ h.dia }}</td><td>{{ formatTime(h.hora_inicial) }}</td><td>{{ formatTime(h.hora_final) }}</td><td>{{ getDisciplinaNombre(h.disciplina) }}</td><td>{{ getInstructorNombre(h.instructor) }}</td>
              <td style="display:flex; gap:0.25rem;">
                <button class="btn btn-outline btn-sm" @click="editHorario(h)">✎</button>
                <button class="btn btn-danger btn-sm" @click="deleteHorario(h.id)">×</button>
              </td>
            </tr>
            <tr v-if="horarios.length === 0"><td colspan="5" class="empty-state">Sin horarios</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal: Nueva Disciplina -->
    <div class="modal-overlay" v-if="showModalD" @click.self="showModalD = false">
      <div class="modal-box">
        <h3>Nueva Disciplina</h3>
        <form @submit.prevent="saveDisciplina">
          <div class="input-group"><label>Nombre</label><input v-model="formD.nombre" class="input-field" required></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Grupo</label><input type="number" v-model="formD.grupo" class="input-field" required></div>
            <div class="input-group"><label>Cupo</label><input type="number" v-model="formD.cupo" class="input-field" required></div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Hora Inicio</label><input v-model="formD.hora_inicial" class="input-field" placeholder="08:00" required></div>
            <div class="input-group"><label>Hora Fin</label><input v-model="formD.hora_final" class="input-field" placeholder="22:00" required></div>
          </div>
          <div class="input-group"><label>Sala</label><select v-model="formD.sala" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="s in salas" :key="s.id" :value="s.id">{{ s.descripcion }}</option></select></div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showModalD = false">Cancelar</button><button type="submit" class="btn btn-primary">Guardar</button></div>
        </form>
      </div>
    </div>

    <!-- Modal: Nuevo Horario -->
    <div class="modal-overlay" v-if="showModalH" @click.self="showModalH = false">
      <div class="modal-box">
        <h3>Programar Horario</h3>
        <form @submit.prevent="saveHorario">
          <div class="input-group"><label>Día</label><select v-model="formH.dia" class="input-field" required><option v-for="d in weekDays" :key="d" :value="d">{{ d }}</option></select></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Hora Inicio</label><input type="time" v-model="formH.hora_inicial" class="input-field" required></div>
            <div class="input-group"><label>Hora Fin</label><input type="time" v-model="formH.hora_final" class="input-field" required></div>
          </div>
          <div class="input-group"><label>Disciplina</label><select v-model="formH.disciplina" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="d in disciplinas" :key="d.id" :value="d.id">{{ d.nombre }}</option></select></div>
          <div class="input-group">
            <label>Instructor</label>
            <select v-model="formH.instructor" class="input-field">
              <option value="">(Sin asignar)</option>
              <option v-for="i in instructores" :key="i.user.id" :value="i.user.id">{{ i.user.first_name }} {{ i.user.last_name }}</option>
            </select>
          </div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showModalH = false">Cancelar</button><button type="submit" class="btn btn-primary">Guardar</button></div>
        </form>
      </div>
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

const disciplinas = ref([]); const horarios = ref([]); const salas = ref([]); const instructores = ref([])
const showModalD = ref(false); const showModalH = ref(false)
const formD = ref({ id:null, nombre:'', grupo:'', cupo:'', hora_inicial:'', hora_final:'', sala:'' })
const formH = ref({ id:null, dia:'', hora_inicial:'', hora_final:'', disciplina:'', instructor:'' })
const weekDays = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
const colors = ['#6366f1','#10b981','#f59e0b','#ef4444','#3b82f6','#a855f7','#06b6d4','#ec4899']

const formatTime = (t) => t ? t.substring(0,5) : ''
const getDisciplinaNombre = (id) => { const d = disciplinas.value.find(x => x.id === id); return d ? d.nombre : `#${id}` }
const getSalaNombre = (id) => { const s = salas.value.find(x => x.id === id); return s ? s.descripcion : `#${id}` }
const getInstructorNombre = (id) => { const i = instructores.value.find(x => x.id === id); return i ? `${i.user.first_name} ${i.user.last_name}` : (id ? `#${id}` : '—') }
const getColor = (id) => colors[(id - 1) % colors.length]
const getHorariosByDay = (day) => horarios.value.filter(h => h.dia && h.dia.toLowerCase().includes(day.toLowerCase().substring(0,3)))

const fetchData = async () => {
  const [resD, resH, resS, resI] = await Promise.all([
    axios.get(`${API}/disciplinas/`, cfg()), axios.get(`${API}/horarios/`, cfg()), axios.get(`${API}/salas/`, cfg()), axios.get(`${API}/instructores/`, cfg())
  ])
  disciplinas.value = resD.data; horarios.value = resH.data; salas.value = resS.data; instructores.value = resI.data
}

const editDisciplina = (d) => { formD.value = { ...d }; showModalD.value = true }
const saveDisciplina = async () => {
  if (formD.value.id) await axios.patch(`${API}/disciplinas/${formD.value.id}/`, formD.value, cfg())
  else await axios.post(`${API}/disciplinas/`, formD.value, cfg())
  showModalD.value = false
  formD.value = { id:null, nombre:'', grupo:'', cupo:'', hora_inicial:'', hora_final:'', sala:'' }; fetchAll()
}
const deleteDisciplina = async (id) => {
  if (!confirm('¿Eliminar disciplina?')) return
  await axios.delete(`${API}/disciplinas/${id}/`, cfg()); fetchAll()
}

const editHorario = (h) => { formH.value = { ...h, hora_inicial: formatTime(h.hora_inicial), hora_final: formatTime(h.hora_final) }; showModalH.value = true }
const saveHorario = async () => {
  const payload = { ...formH.value }
  if (!payload.instructor) payload.instructor = null // Ensure null instead of empty string
  if (formH.value.id) await axios.patch(`${API}/horarios/${formH.value.id}/`, payload, cfg())
  else await axios.post(`${API}/horarios/`, payload, cfg())
  showModalH.value = false
  formH.value = { id:null, dia:'', hora_inicial:'', hora_final:'', disciplina:'', instructor:'' }; fetchAll()
}
const deleteHorario = async (id) => {
  if (!confirm('¿Eliminar horario?')) return
  await axios.delete(`${API}/horarios/${id}/`, cfg()); fetchAll()
}
onMounted(fetchAll)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }

.calendar-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.5rem; min-height: 200px; }
.calendar-col { display: flex; flex-direction: column; gap: 0.4rem; }
.cal-day-header { text-align: center; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); padding: 0.5rem; background: rgba(0,0,0,0.2); border-radius: var(--radius-sm); }
.cal-block { padding: 0.5rem 0.6rem; background: rgba(0,0,0,0.2); border-radius: var(--radius-sm); border-left: 3px solid var(--accent-color); }
.cal-time { font-size: 0.7rem; color: var(--accent-hover); font-weight: 600; display: block; }
.cal-name { font-size: 0.8rem; font-weight: 500; }
.cal-empty { text-align: center; color: var(--text-muted); padding: 1rem; font-size: 0.8rem; }
@media (max-width: 768px) { .calendar-grid { grid-template-columns: repeat(3, 1fr); } }
</style>

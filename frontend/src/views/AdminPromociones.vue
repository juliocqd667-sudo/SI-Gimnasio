<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Gestión de Promociones</h1><p class="page-subtitle">Crea y administra ofertas especiales para tus clientes.</p></div>
      <button class="btn btn-primary" @click="openModal()">+ Nueva Promoción</button>
    </header>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-icon green">🎉</div><div class="kpi-data"><span class="kpi-value">{{ promociones.length }}</span><span class="kpi-label">Total</span></div></div>
      <div class="kpi-card"><div class="kpi-icon blue">✅</div><div class="kpi-data"><span class="kpi-value">{{ promociones.filter(p => p.estado === 'A').length }}</span><span class="kpi-label">Activas</span></div></div>
      <div class="kpi-card"><div class="kpi-icon red">⏸</div><div class="kpi-data"><span class="kpi-value">{{ promociones.filter(p => p.estado !== 'A').length }}</span><span class="kpi-label">Inactivas</span></div></div>
    </div>

    <div class="section-panel">
      <div class="section-header"><h3>📋 Todas las Promociones</h3></div>
      <table class="data-table">
        <thead>
          <tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Valor</th><th>Vigencia</th><th>Estado</th><th>Descripción</th><th>Acciones</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in promociones" :key="p.id">
            <td>#{{ p.id }}</td>
            <td><strong>{{ p.nombre }}</strong></td>
            <td><span class="badge badge-info">{{ p.tipo }}</span></td>
            <td class="font-mono">{{ p.tipo === 'Porcentaje' ? p.valor + '%' : '$' + p.valor }}</td>
            <td>{{ p.fecha_ini }} → {{ p.fecha_fin }}</td>
            <td><span class="badge" :class="p.estado === 'A' ? 'badge-success' : 'badge-neutral'">{{ p.estado === 'A' ? 'Activa' : 'Inactiva' }}</span></td>
            <td style="max-width:200px;">{{ p.descripcion }}</td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(p)">Editar</button>
              <button class="btn btn-danger btn-sm" @click="deletePromo(p.id)" style="margin-left:0.25rem;">×</button>
            </td>
          </tr>
          <tr v-if="promociones.length === 0"><td colspan="8" class="empty-state">No hay promociones registradas.</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Modal: Crear/Editar Promoción -->
    <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
      <div class="modal-box" style="max-width:550px;">
        <h3>{{ form.id ? 'Editar' : 'Nueva' }} Promoción</h3>
        <form @submit.prevent="savePromo">
          <div class="input-group"><label>Nombre</label><input v-model="form.nombre" class="input-field" placeholder="Ej. 2x1 Verano" required maxlength="20"></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Tipo</label><select v-model="form.tipo" class="input-field" required><option value="Porcentaje">Porcentaje (%)</option><option value="Monto">Monto Fijo ($)</option><option value="2x1">2x1</option><option value="Gratis">Gratis</option></select></div>
            <div class="input-group"><label>Valor</label><input type="number" step="0.01" v-model="form.valor" class="input-field" required></div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Fecha Inicio</label><input type="date" v-model="form.fecha_ini" class="input-field" required></div>
            <div class="input-group"><label>Fecha Fin</label><input type="date" v-model="form.fecha_fin" class="input-field" required></div>
          </div>
          <div class="input-group"><label>Estado</label><select v-model="form.estado" class="input-field" required><option value="A">Activa</option><option value="I">Inactiva</option></select></div>
          <div class="input-group"><label>Descripción</label><textarea v-model="form.descripcion" class="input-field" rows="2" required maxlength="100"></textarea></div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" @click="showModal = false">Cancelar</button>
            <button type="submit" class="btn btn-primary">{{ form.id ? 'Actualizar' : 'Guardar' }}</button>
          </div>
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

const promociones = ref([])
const showModal = ref(false)
const toast = ref(null)
const showToast = (msg, type='toast-success') => { toast.value = { msg, type }; setTimeout(() => toast.value = null, 3000) }

const emptyForm = () => ({ id: null, nombre:'', tipo:'Porcentaje', valor:'', fecha_ini:'', fecha_fin:'', estado:'A', descripcion:'' })
const form = ref(emptyForm())

const fetchData = async () => { promociones.value = (await axios.get(`${API}/promociones/`, cfg())).data }

const openModal = (p = null) => {
  form.value = p ? { ...p } : emptyForm()
  showModal.value = true
}

const savePromo = async () => {
  try {
    if (form.value.id) {
      await axios.put(`${API}/promociones/${form.value.id}/`, form.value, cfg())
      showToast('Promoción actualizada')
    } else {
      const payload = { ...form.value }; delete payload.id
      await axios.post(`${API}/promociones/`, payload, cfg())
      showToast('Promoción creada')
    }
    showModal.value = false; form.value = emptyForm(); fetchData()
  } catch(e) {
    console.error(e);
    let msg = 'Error al guardar';
    if (e.response && e.response.data) {
      const errs = Object.values(e.response.data).flat();
      if (errs.length) msg = errs[0];
    }
    showToast(msg, 'toast-error');
  }
}

const deletePromo = async (id) => {
  if (!confirm('¿Eliminar esta promoción?')) return
  try { await axios.delete(`${API}/promociones/${id}/`, cfg()); showToast('Promoción eliminada'); fetchData() }
  catch(e) { showToast('Error al eliminar', 'toast-error') }
}

onMounted(fetchData)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }
.font-mono { font-family: 'SF Mono', monospace; }
</style>

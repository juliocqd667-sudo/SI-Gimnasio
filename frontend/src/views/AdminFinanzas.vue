<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Gestión Financiera</h1><p class="page-subtitle">Suscripciones, pagos y comprobantes.</p></div>
    </header>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-icon purple">💰</div><div class="kpi-data"><span class="kpi-value">${{ totalIngresos.toFixed(0) }}</span><span class="kpi-label">Ingresos</span></div></div>
      <div class="kpi-card"><div class="kpi-icon green">📋</div><div class="kpi-data"><span class="kpi-value">{{ pagos.length }}</span><span class="kpi-label">Pagos</span></div></div>
      <div class="kpi-card"><div class="kpi-icon blue">🎫</div><div class="kpi-data"><span class="kpi-value">{{ suscripciones.length }}</span><span class="kpi-label">Planes</span></div></div>
    </div>

    <!-- CU7: Gestión de Suscripciones -->
    <div class="section-panel" style="margin-bottom:1.5rem;">
      <div class="section-header"><h3>🎫 Planes de Suscripción (CU7)</h3><button class="btn btn-primary btn-sm" @click="showSuscModal = true">+ Nuevo Plan</button></div>
      <table class="data-table">
        <thead><tr><th>ID</th><th>Membresía</th><th>Plan</th><th>Descripción</th><th>Precio</th><th>Acciones</th></tr></thead>
        <tbody>
          <tr v-for="s in suscripciones" :key="s.id">
            <td>#{{ s.id }}</td><td><strong>{{ s.membresia }}</strong></td><td>{{ s.plan }}</td><td>{{ s.descripcion }}</td>
            <td class="font-mono">${{ s.precio }}</td>
            <td>
              <button class="btn btn-outline btn-sm" @click="editSusc(s)">Editar</button>
              <button class="btn btn-danger btn-sm" @click="deleteSusc(s.id)" style="margin-left:0.25rem;">×</button>
            </td>
          </tr>
          <tr v-if="suscripciones.length === 0"><td colspan="6" class="empty-state">Sin planes</td></tr>
        </tbody>
      </table>
    </div>

    <div class="grid-2">
      <!-- Historial de Pagos -->
      <div class="section-panel">
        <div class="section-header"><h3>💳 Historial de Pagos</h3></div>
        <table class="data-table">
          <thead><tr><th>Fecha</th><th>Cliente</th><th>Monto</th><th>Estado</th></tr></thead>
          <tbody>
            <tr v-for="p in pagos.slice().reverse().slice(0, 15)" :key="p.id">
              <td>{{ p.fecha }}</td>
              <td>{{ getClienteNombre(p.cliente) }}</td>
              <td class="font-mono">${{ p.monto_total }}</td>
              <td><span class="badge badge-success">{{ p.estado_pago || 'Pagado' }}</span></td>
            </tr>
            <tr v-if="pagos.length === 0"><td colspan="4" class="empty-state">Sin pagos</td></tr>
          </tbody>
        </table>
      </div>

      <!-- Registrar Pago -->
      <div class="section-panel">
        <div class="section-header"><h3>📝 Registrar Pago</h3></div>
        <form @submit.prevent="registrarPago" style="display:flex; flex-direction:column; gap:0.75rem;">
          <div class="input-group"><label>Cliente</label><select v-model="pago.cliente" class="input-field" required><option value="" disabled>Seleccionar...</option><option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.user.first_name }} {{ c.user.last_name }}</option></select></div>
          <div class="input-group"><label>Membresía</label><select v-model="pago.membresia" class="input-field" required @change="autoMonto"><option value="" disabled>Seleccionar plan...</option><option v-for="s in suscripciones" :key="s.id" :value="s.id">{{ s.membresia }} — ${{ s.precio }}</option></select></div>
          <div class="grid-2">
            <div class="input-group"><label>Método</label><select v-model="pago.metodo" class="input-field"><option value="E">Efectivo</option><option value="T">Tarjeta</option><option value="Q">QR / Transferencia</option></select></div>
            <div class="input-group"><label>Monto ($)</label><input type="number" step="0.01" v-model="pago.monto" class="input-field" required></div>
          </div>
          <!-- Yape QR Display -->
          <div v-if="pago.metodo === 'Q'" class="qr-container">
            <img src="/qr_pago.png" alt="QR Yape" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%">Procesar Pago</button>
        </form>
      </div>
    </div>

    <!-- Modal: Crear/Editar Suscripción -->
    <div class="modal-overlay" v-if="showSuscModal" @click.self="showSuscModal = false">
      <div class="modal-box">
        <h3>{{ suscForm.id ? 'Editar' : 'Crear' }} Plan de Suscripción</h3>
        <form @submit.prevent="saveSusc">
          <div class="input-group"><label>Membresía</label><input v-model="suscForm.membresia" class="input-field" placeholder="Ej. Premium" required></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Plan</label><input v-model="suscForm.plan" class="input-field" placeholder="Ej. Mensual" required></div>
            <div class="input-group"><label>Precio ($)</label><input type="number" step="0.01" v-model="suscForm.precio" class="input-field" required></div>
          </div>
          <div class="input-group"><label>Descripción</label><input v-model="suscForm.descripcion" class="input-field" placeholder="Descripción del plan" required></div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showSuscModal = false">Cancelar</button><button type="submit" class="btn btn-primary">{{ suscForm.id ? 'Actualizar' : 'Guardar' }}</button></div>
        </form>
      </div>
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

const suscripciones = ref([]); const clientes = ref([]); const pagos = ref([])
const pago = ref({ cliente:'', membresia:'', metodo:'E', monto:0 })
const showSuscModal = ref(false)
const suscForm = ref({ id: null, membresia:'', plan:'', descripcion:'', precio:'' })
const toast = ref(null)
const showToast = (msg, type='toast-success') => { toast.value = { msg, type }; setTimeout(() => toast.value = null, 3000) }

const totalIngresos = computed(() => pagos.value.reduce((s, p) => s + parseFloat(p.monto_total || 0), 0))
const autoMonto = () => { const p = suscripciones.value.find(s => s.id === pago.value.membresia); if(p) pago.value.monto = parseFloat(p.precio) }
const getClienteNombre = (id) => { const c = clientes.value.find(x => x.id === id); return c ? `${c.user.first_name} ${c.user.last_name}` : `#${id}` }

const fetchData = async () => {
  const [resS, resC, resP] = await Promise.all([
    axios.get(`${API}/suscripciones/`, cfg()), axios.get(`${API}/clientes/`, cfg()), axios.get(`${API}/pagos/`, cfg())
  ])
  suscripciones.value = resS.data; clientes.value = resC.data; pagos.value = resP.data
}

// CU7: CRUD Suscripciones
const editSusc = (s) => { suscForm.value = { ...s }; showSuscModal.value = true }
const saveSusc = async () => {
  try {
    if (suscForm.value.id) {
      await axios.put(`${API}/suscripciones/${suscForm.value.id}/`, suscForm.value, cfg())
      showToast('Plan actualizado')
    } else {
      await axios.post(`${API}/suscripciones/`, suscForm.value, cfg())
      showToast('Plan creado')
    }
    showSuscModal.value = false; suscForm.value = { id: null, membresia:'', plan:'', descripcion:'', precio:'' }; fetchData()
  } catch(e) { showToast('Error al guardar plan', 'toast-error') }
}
const deleteSusc = async (id) => {
  if (!confirm('¿Eliminar este plan?')) return
  try { await axios.delete(`${API}/suscripciones/${id}/`, cfg()); showToast('Plan eliminado'); fetchData() } catch(e) { showToast('Error al eliminar', 'toast-error') }
}

const registrarPago = async () => {
  try {
    const res = await axios.post(`${API}/pagos/`, {
      metodo_pago: pago.value.metodo, monto_total: pago.value.monto, fecha: new Date().toISOString().split('T')[0],
      cliente: pago.value.cliente, suscripcion: pago.value.membresia, estado_pago: 'Completado'
    }, cfg())
    const hoy = new Date().toISOString().split('T')[0]
    const next = new Date(Date.now() + 30*86400000).toISOString().split('T')[0]
    await axios.post(`${API}/comprobantes/`, { monto: pago.value.monto, fecha_ini_mem: hoy, fecha_fin_mem: next, pago: res.data.id, cliente: pago.value.cliente }, cfg())
    pago.value = { cliente:'', membresia:'', metodo:'E', monto:0 }; showToast('Pago registrado y comprobante generado'); fetchData()
  } catch(e) {
    console.error(e);
    let msg = 'Error al registrar pago';
    if (e.response && e.response.data) {
      const errs = Object.values(e.response.data).flat();
      if (errs.length) msg = errs[0];
    }
    showToast(msg, 'toast-error');
  }
}
onMounted(fetchData)
</script>

<style scoped>
.page-header { margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }
.font-mono { font-family: 'SF Mono', monospace; }

/* QR Styles */
.qr-container { background: #fff; padding: 1.5rem; border-radius: var(--radius-md); text-align: center; color: #000; margin: 0.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.qr-header { margin-bottom: 1rem; }
.qr-yape { font-size: 1.5rem; font-weight: 800; color: #7b2cbf; display: inline-block; padding: 0.2rem 0.5rem; border: 2px solid #7b2cbf; border-radius: 4px; }
.qr-box { width: 180px; height: 180px; margin: 0 auto; background: repeating-linear-gradient(45deg, #000 0, #000 5px, #fff 5px, #fff 10px), repeating-linear-gradient(-45deg, #000 0, #000 5px, #fff 5px, #fff 10px); position: relative; border: 10px solid #fff; box-shadow: 0 0 0 2px #000; border-radius: 8px; }
.qr-inner { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; height: 50px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.qr-footer { margin-top: 1rem; }
.qr-footer p { font-size: 0.85rem; color: #666; margin-bottom: 0.25rem; }
.qr-footer h3 { font-size: 1.1rem; color: #333; margin-bottom: 0.25rem; }
</style>

<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div><h1>Gestión de Usuarios</h1><p class="page-subtitle">Administra miembros, instructores y personal.</p></div>
      <button class="btn btn-primary" @click="showForm = true">+ Nuevo Usuario</button>
    </header>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-icon blue">👥</div><div class="kpi-data"><span class="kpi-value">{{ users.length }}</span><span class="kpi-label">Total</span></div></div>
      <div class="kpi-card"><div class="kpi-icon green">✅</div><div class="kpi-data"><span class="kpi-value">{{ users.filter(u => u.is_cliente).length }}</span><span class="kpi-label">Clientes</span></div></div>
      <div class="kpi-card"><div class="kpi-icon orange">🏋️</div><div class="kpi-data"><span class="kpi-value">{{ users.filter(u => u.is_instructor).length }}</span><span class="kpi-label">Instructores</span></div></div>
      <div class="kpi-card"><div class="kpi-icon purple">🩺</div><div class="kpi-data"><span class="kpi-value">{{ users.filter(u => u.is_nutricionista).length }}</span><span class="kpi-label">Nutricionistas</span></div></div>
    </div>

    <div class="section-panel">
      <div class="section-header">
        <input type="text" v-model="search" placeholder="Buscar usuarios..." class="input-field" style="max-width:320px; margin-bottom:0;" />
      </div>
      <table class="data-table">
        <thead><tr><th>ID</th><th>Nombre</th><th>Usuario</th><th>Email</th><th>Rol</th><th>Acciones</th></tr></thead>
        <tbody>
          <tr v-for="u in filtered" :key="u.id" @click="selectUser(u)" style="cursor:pointer;">
            <td>#{{ u.id }}</td>
            <td><strong>{{ u.first_name }} {{ u.last_name }}</strong></td>
            <td style="color:var(--text-secondary)">@{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td><span class="badge" :class="badgeClass(u)">{{ roleName(u) }}</span></td>
            <td><button class="btn btn-outline btn-sm" @click.stop="selectUser(u)">Ver</button></td>
          </tr>
          <tr v-if="filtered.length === 0"><td colspan="6" class="empty-state">Sin resultados</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Modal: Perfil 360° -->
    <div class="modal-overlay" v-if="selectedUser" @click.self="selectedUser = null">
      <div class="modal-box" style="max-width:550px;">
        <div class="profile-header">
          <div class="profile-avatar">{{ (selectedUser.first_name || 'U')[0] }}</div>
          <div>
            <h3>Perfil de Usuario #{{ selectedUser.id }}</h3>
            <span class="badge" :class="badgeClass(selectedUser)">{{ roleName(selectedUser) }}</span>
          </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
          <div class="input-group"><label>Nombres</label><input v-model="selectedUser.first_name" class="input-field"></div>
          <div class="input-group"><label>Apellidos</label><input v-model="selectedUser.last_name" class="input-field"></div>
          <div class="input-group"><label>Email</label><input v-model="selectedUser.email" class="input-field"></div>
          <div class="input-group"><label>Username</label><input :value="selectedUser.username" class="input-field" disabled></div>
        </div>
        <div class="profile-details">
          <div class="detail-row"><span>CI:</span><span>{{ selectedUser.ci || '—' }}</span></div>
          <div class="detail-row"><span>Teléfono:</span><span>{{ selectedUser.telefono || '—' }}</span></div>
          <div class="detail-row" v-if="selectedUser.is_cliente"><span>Domicilio:</span><input v-model="selectedUser.domicilio" class="input-field-sm" placeholder="Sin dirección"></div>
          <div class="detail-row"><span>Nacimiento:</span><span>{{ selectedUser.fecha_nacimiento || '—' }}</span></div>
          <div class="detail-row"><span>Sexo:</span><span>{{ selectedUser.sexo === 'M' ? 'Masculino' : selectedUser.sexo === 'F' ? 'Femenino' : '—' }}</span></div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-danger btn-sm" @click="deleteUser(selectedUser.id)">Eliminar</button>
          <button class="btn btn-primary btn-sm" @click="editUser">Guardar Cambios</button>
          <button class="btn btn-outline btn-sm" @click="selectedUser = null">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- Modal: Crear Usuario -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal-box">
        <h3>Registrar Nuevo Usuario</h3>
        <form @submit.prevent="createUser">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
            <div class="input-group"><label>Username</label><input type="text" v-model="form.username" class="input-field" required></div>
            <div class="input-group"><label>Email</label><input type="email" v-model="form.email" class="input-field" required></div>
            <div class="input-group"><label>Nombres</label><input type="text" v-model="form.first_name" class="input-field" required></div>
            <div class="input-group"><label>Apellidos</label><input type="text" v-model="form.last_name" class="input-field" required></div>
            <div class="input-group"><label>Contraseña</label><input type="password" v-model="form.password" class="input-field" required></div>
            <div class="input-group"><label>Rol</label><select v-model="form.role" class="input-field"><option value="cliente">Cliente</option><option value="instructor">Instructor</option><option value="nutricionista">Nutricionista</option><option value="administrativo">Administrativo</option></select></div>
          </div>
          <div class="modal-footer"><button type="button" class="btn btn-outline" @click="showForm = false">Cancelar</button><button type="submit" class="btn btn-primary">Guardar</button></div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import API from '../api'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
const cfg = () => ({ headers: { Authorization: `Bearer ${authStore.accessToken}` } })

const users = ref([])
const search = ref('')
const showForm = ref(false)
const selectedUser = ref(null)
const form = ref({ username:'', email:'', first_name:'', last_name:'', password:'', role:'cliente' })

const filtered = computed(() => {
  if (!search.value) return users.value
  const q = search.value.toLowerCase()
  return users.value.filter(u => `${u.first_name} ${u.last_name} ${u.username} ${u.email}`.toLowerCase().includes(q))
})

const roleName = (u) => { if(u.is_administrativo) return 'Admin'; if(u.is_instructor) return 'Instructor'; if(u.is_nutricionista) return 'Nutricionista'; if(u.is_cliente) return 'Cliente'; return 'User' }
const badgeClass = (u) => { if(u.is_administrativo) return 'badge-danger'; if(u.is_instructor) return 'badge-warning'; if(u.is_nutricionista) return 'badge-info'; if(u.is_cliente) return 'badge-success'; return 'badge-neutral' }

const fetchUsers = async () => { users.value = (await axios.get(`${API}/users/`, cfg())).data }
const selectUser = (u) => { selectedUser.value = u }

const createUser = async () => {
  try {
    const payload = { username: form.value.username, email: form.value.email, first_name: form.value.first_name, last_name: form.value.last_name, password: form.value.password, [`is_${form.value.role}`]: true }
    const res = await axios.post(`${API}/users/`, payload, cfg())
    const userId = res.data.id
    // CU6: Crear perfil asociado al rol
    const roleEndpoints = { cliente: 'clientes', instructor: 'instructores', nutricionista: 'nutricionistas', administrativo: 'administrativos' }
    const endpoint = roleEndpoints[form.value.role]
    if (endpoint) {
      await axios.post(`${API}/${endpoint}/`, { user: userId }, cfg()).catch(() => {})
    }
    showForm.value = false; form.value = { username:'', email:'', first_name:'', last_name:'', password:'', role:'cliente' }; fetchUsers()
  } catch(e) { alert('Error al crear usuario') }
}

const editUser = async () => {
  try {
    const u = selectedUser.value
    await axios.patch(`${API}/users/${u.id}/`, { first_name: u.first_name, last_name: u.last_name, email: u.email, ci: u.ci, telefono: u.telefono, fecha_nacimiento: u.fecha_nacimiento }, cfg())
    
    // Si es cliente, guardar domicilio en su perfil
    if (u.is_cliente) {
      const resC = await axios.get(`${API}/clientes/`, cfg())
      const cliente = resC.data.find(c => c.user.id === u.id)
      if (cliente) {
        await axios.patch(`${API}/clientes/${cliente.user.id}/`, { domicilio: u.domicilio }, cfg())
      }
    }
    
    selectedUser.value = null; fetchUsers()
  } catch(e) { alert('Error al editar') }
}

const deleteUser = async (id) => {
  if(!confirm('¿Eliminar este usuario permanentemente?')) return
  try { await axios.delete(`${API}/users/${id}/`, cfg()); selectedUser.value = null; fetchUsers() } catch(e) { alert('Error al eliminar') }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.page-header h1 { font-size: 1.5rem; }
.page-subtitle { color: var(--text-secondary); font-size: 0.875rem; }
.profile-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.profile-avatar { width: 56px; height: 56px; border-radius: 50%; background: var(--accent-gradient); display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.25rem; flex-shrink: 0; }
.profile-details { display: flex; flex-direction: column; gap: 0.5rem; }
.detail-row { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 0.875rem; }
.detail-row span:first-child { color: var(--text-secondary); }
</style>

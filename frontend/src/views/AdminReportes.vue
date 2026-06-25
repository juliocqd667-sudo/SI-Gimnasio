<!-- src/views/AdminReportes.vue -->
<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div>
        <h1>Reportes del Sistema</h1>
        <p class="page-subtitle">Genera reportes en Excel y PDF de toda la información.</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-outline" @click="startVoiceCommand" :class="{ listening: isListening }">
          🎤 {{ isListening ? 'Escuchando...' : 'Comando por voz' }}
        </button>
      </div>
    </header>

    <div class="reportes-grid">
      <div class="reporte-card" v-for="group in reportes" :key="group.titulo">
        <h3>{{ group.titulo }}</h3>
        <div class="reporte-buttons">
          <a v-for="re in group.reportes" :key="re.key" :href="`${API}/reportes/${re.key}/`" class="btn btn-primary btn-sm" target="_blank">
            {{ re.label }}
          </a>
        </div>
      </div>
    </div>

    <div class="status-bar" v-if="voiceStatus">{{ voiceStatus }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import API from '../api'

const isListening = ref(false)
const voiceStatus = ref('')
let recognition = null

const reportes = ref([
  {
    titulo: 'Usuarios',
    reportes: [
      { key: 'usuarios/excel/', label: '📗 Excel' },
      { key: 'usuarios/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Pagos',
    reportes: [
      { key: 'pagos/excel/', label: '📗 Excel' },
      { key: 'pagos/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Suscripciones',
    reportes: [
      { key: 'suscripciones/excel/', label: '📗 Excel' },
      { key: 'suscripciones/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Promociones',
    reportes: [
      { key: 'promociones/excel/', label: '📗 Excel' },
      { key: 'promociones/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Rutinas',
    reportes: [
      { key: 'rutinas/excel/', label: '📗 Excel' },
      { key: 'rutinas/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Horarios',
    reportes: [
      { key: 'horarios/excel/', label: '📗 Excel' },
      { key: 'horarios/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Antecedentes',
    reportes: [
      { key: 'antecedentes/excel/', label: '📗 Excel' },
      { key: 'antecedentes/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Seguimientos',
    reportes: [
      { key: 'seguimientos/excel/', label: '📗 Excel' },
      { key: 'seguimientos/pdf/', label: '📕 PDF' },
    ]
  },
])

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition = new SpeechRecognition()
  recognition.lang = 'es-ES'
  recognition.continuous = false
  recognition.interimResults = false

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase().trim()
    voiceStatus.value = `Comando recibido: "${transcript}"`
    processVoiceCommand(transcript)
  }

  recognition.onerror = (event) => {
    voiceStatus.value = `Error en reconocimiento de voz: ${event.error}`
    isListening.value = false
  }

  recognition.onend = () => {
    isListening.value = false
  }
}

const startVoiceCommand = () => {
  if (!recognition) {
    voiceStatus.value = 'Tu navegador no soporta reconocimiento de voz.'
    return
  }
  isListening.value = true
  voiceStatus.value = 'Escuchando... Di el nombre del reporte que deseas generar.'
  recognition.start()
}

const processVoiceCommand = (transcript) => {
  const reportes = {
    'usuarios excel': 'usuarios/excel/',
    'usuarios pdf': 'usuarios/pdf/',
    'pagos excel': 'pagos/excel/',
    'pagos pdf': 'pagos/pdf/',
    'suscripciones excel': 'suscripciones/excel/',
    'suscripciones pdf': 'suscripciones/pdf/',
    'promociones excel': 'promociones/excel/',
    'promociones pdf': 'promociones/pdf/',
    'rutinas excel': 'rutinas/excel/',
    'rutinas pdf': 'rutinas/pdf/',
    'horarios excel': 'horarios/excel/',
    'horarios pdf': 'horarios/pdf/',
    'antecedentes excel': 'antecedentes/excel/',
    'antecedentes pdf': 'antecedentes/pdf/',
    'seguimientos excel': 'seguimientos/excel/',
    'seguimientos pdf': 'seguimientos/pdf/',
  }

  const key = Object.keys(reportes).find(k => transcript.includes(k))
  if (key) {
    const url = `${API}/reportes/${reportes[key]}`
    window.open(url, '_blank')
    voiceStatus.value = `Generando reporte: ${key.replace(' ', ' ').toUpperCase()}`
  } else {
    voiceStatus.value = 'Comando no reconocido. Di: "usuarios excel", "pagos pdf", etc.'
  }
}
</script>

<style scoped>
.reportes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
.reporte-card { background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; }
.reporte-card h3 { font-size: 0.95rem; margin-bottom: 0.75rem; color: var(--text-primary); }
.reporte-buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.header-actions { display: flex; gap: 0.5rem; align-items: center; }
.status-bar { margin-top: 1rem; padding: 0.75rem; background: rgba(99,102,241,0.1); border: 1px solid var(--accent-color); border-radius: var(--radius-sm); font-size: 0.85rem; color: var(--accent-hover); }
.listening { border-color: #ef4444; color: #ef4444; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
</style>

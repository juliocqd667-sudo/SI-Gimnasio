<!-- src/views/AdminReportes.vue -->
<template>
  <div class="animate-fade-in">
    <header class="page-header">
      <div>
        <h1>Reportes del Sistema</h1>
        <p class="page-subtitle">Genera reportes en Excel y PDF de toda la información.</p>
      </div>
      <div class="voice-command-container">
        <button class="voice-btn" @click="startVoiceCommand" :class="{ listening: isListening }">
          <span class="voice-icon">🎤</span>
          <span class="voice-text">{{ isListening ? 'Escuchando orden...' : 'Control por Voz' }}</span>
          <span class="voice-pulse" v-if="isListening"></span>
        </button>
      </div>
    </header>

    <div class="reportes-grid">
      <div class="reporte-card" v-for="group in reportes" :key="group.titulo">
        <h3>{{ group.titulo }}</h3>
        <div class="reporte-buttons">
          <button v-for="re in group.reportes" :key="re.key" @click="downloadReport(re.key, group.titulo, re.label)" class="btn btn-primary btn-sm">
            {{ re.label }}
          </button>
        </div>
      </div>
    </div>

    <div class="status-bar" v-if="voiceStatus">{{ voiceStatus }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import API from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
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
    titulo: 'Ejercicios',
    reportes: [
      { key: 'ejercicios/excel/', label: '📗 Excel' },
      { key: 'ejercicios/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Salas',
    reportes: [
      { key: 'salas/excel/', label: '📗 Excel' },
      { key: 'salas/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Disciplinas',
    reportes: [
      { key: 'disciplinas/excel/', label: '📗 Excel' },
      { key: 'disciplinas/pdf/', label: '📕 PDF' },
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
    titulo: 'Reservas',
    reportes: [
      { key: 'reservas/excel/', label: '📗 Excel' },
      { key: 'reservas/pdf/', label: '📕 PDF' },
    ]
  },
  {
    titulo: 'Consultas',
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

const downloadReport = async (key, title, label) => {
  try {
    const isPdf = key.includes('pdf')
    const format = isPdf ? 'PDF' : 'Excel'
    voiceStatus.value = `Descargando reporte de ${title} en formato ${format}...`

    const response = await axios.get(`${API}/reportes/${key}`, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` },
      responseType: 'blob'
    })

    const blob = new Blob([response.data], {
      type: isPdf ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })

    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl

    const filename = `${title.toLowerCase().replace(/[^a-z0-9]/g, '_')}_reporte.${isPdf ? 'pdf' : 'xlsx'}`
    link.setAttribute('download', filename)

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)

    voiceStatus.value = `Reporte de ${title} (${format}) descargado con éxito.`
  } catch (error) {
    console.error(error)
    voiceStatus.value = `Error al descargar el reporte de ${title}.`
  }
}

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
  voiceStatus.value = 'Escuchando... Di el nombre del reporte que deseas generar (ej: "excel de pagos" o "pdf de consultas").'
  recognition.start()
}

const processVoiceCommand = (transcript) => {
  const text = transcript.toLowerCase().trim()

  // Detect format
  let format = null
  let formatLabel = ''
  if (text.includes('excel') || text.includes('xls') || text.includes('hoja de cálculo') || text.includes('hoja de calculo')) {
    format = 'excel'
    formatLabel = '📗 Excel'
  } else if (text.includes('pdf') || text.includes('documento') || text.includes('portable')) {
    format = 'pdf'
    formatLabel = '📕 PDF'
  }

  // Detect section
  let sectionKey = null
  let sectionName = ''

  if (text.includes('usuario')) {
    sectionKey = 'usuarios'
    sectionName = 'Usuarios'
  } else if (text.includes('pago')) {
    sectionKey = 'pagos'
    sectionName = 'Pagos'
  } else if (text.includes('suscripcion') || text.includes('suscripción')) {
    sectionKey = 'suscripciones'
    sectionName = 'Suscripciones'
  } else if (text.includes('promocion') || text.includes('promoción')) {
    sectionKey = 'promociones'
    sectionName = 'Promociones'
  } else if (text.includes('rutina')) {
    sectionKey = 'rutinas'
    sectionName = 'Rutinas'
  } else if (text.includes('ejercicio')) {
    sectionKey = 'ejercicios'
    sectionName = 'Ejercicios'
  } else if (text.includes('sala')) {
    sectionKey = 'salas'
    sectionName = 'Salas'
  } else if (text.includes('disciplina') || text.includes('clase')) {
    sectionKey = 'disciplinas'
    sectionName = 'Disciplinas'
  } else if (text.includes('horario')) {
    sectionKey = 'horarios'
    sectionName = 'Horarios'
  } else if (text.includes('reserva')) {
    sectionKey = 'reservas'
    sectionName = 'Reservas'
  } else if (text.includes('consulta') || text.includes('antecedente')) {
    sectionKey = 'antecedentes'
    sectionName = 'Consultas'
  } else if (text.includes('seguimiento')) {
    sectionKey = 'seguimientos'
    sectionName = 'Seguimientos'
  }

  if (format && sectionKey) {
    const key = `${sectionKey}/${format}/`
    downloadReport(key, sectionName, formatLabel)
  } else {
    if (!format && !sectionKey) {
      voiceStatus.value = `Comando no reconocido: "${transcript}". Intenta decir: "excel de pagos" o "pdf de consultas".`
    } else if (!format) {
      voiceStatus.value = `Se detectó la sección "${sectionName}", pero no el formato. Di: "excel" o "pdf".`
    } else {
      voiceStatus.value = `Se detectó el formato "${format === 'excel' ? 'Excel' : 'PDF'}", pero no el reporte. Di: "pagos", "consultas", "usuarios", etc.`
    }
  }
}
</script>

<style scoped>
.reportes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
.reporte-card { background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; }
.reporte-card h3 { font-size: 0.95rem; margin-bottom: 0.75rem; color: var(--text-primary); }
.reporte-buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; }

/* Voice Command Button Premium Style */
.voice-command-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.voice-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 1.6rem;
  font-size: 1rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.voice-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
  background: linear-gradient(135deg, #4f46e5, #9333ea);
}
.voice-btn:active {
  transform: translateY(1px);
}
.voice-icon {
  font-size: 1.2rem;
}
.voice-text {
  letter-spacing: 0.02em;
}
.voice-btn.listening {
  background: linear-gradient(135deg, #ef4444, #f43f5e);
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.5);
  animation: pulse-glow 1.5s infinite;
}
.voice-pulse {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 50px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  animation: ripple 1.5s infinite;
  opacity: 0;
}
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.5);
  }
  50% {
    box-shadow: 0 4px 30px rgba(239, 68, 68, 0.85);
  }
}
@keyframes ripple {
  0% {
    transform: scale(0.95);
    opacity: 0.6;
  }
  100% {
    transform: scale(1.35);
    opacity: 0;
  }
}

.status-bar { margin-top: 1rem; padding: 0.75rem; background: rgba(99,102,241,0.1); border: 1px solid var(--accent-color); border-radius: var(--radius-sm); font-size: 0.85rem; color: var(--accent-hover); }
</style>

<template>
  <div class="home animate-fade-in">
    <div class="hero">
      <div class="hero-badge">SISTEMA DE GESTIÓN</div>
      <h1 class="hero-title"><span class="text-gradient">NovaFit</span> Gym</h1>
      <p class="hero-subtitle">Plataforma integral de entrenamiento, nutrición y gestión para tu gimnasio.</p>
      <div class="hero-actions">
        <button class="btn btn-primary" @click="$router.push('/login')">Comenzar</button>
        <button class="btn btn-outline" @click="$router.push('/login')">Ver Demo</button>
      </div>
    </div>

    <div class="features-grid">
      <div class="feature-card" v-for="(f, i) in features" :key="i">
        <div class="feature-icon" :class="f.color">{{ f.icon }}</div>
        <h3>{{ f.title }}</h3>
        <p>{{ f.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  { icon: '💪', title: 'Rutinas Personalizadas', desc: 'Ejercicios con series, repeticiones y peso asignados por tu instructor.', color: 'blue' },
  { icon: '🥗', title: 'Control Nutricional', desc: 'Seguimiento de IMC, peso y diagnósticos con gauge visual.', color: 'green' },
  { icon: '📅', title: 'Reservas Online', desc: 'Reserva cupo en clases con barra de disponibilidad en tiempo real.', color: 'purple' },
  { icon: '📊', title: 'Dashboard Inteligente', desc: 'KPIs de ingresos, usuarios y actividades al instante.', color: 'orange' },
  { icon: '🏋️', title: 'Gestión de Clases', desc: 'Calendario visual semanal con disciplinas y horarios.', color: 'cyan' },
  { icon: '👥', title: 'Perfiles 360°', desc: 'Vista completa de cada miembro: datos, membresía y actividad.', color: 'red' },
]
</script>

<style scoped>
.home { display: flex; flex-direction: column; gap: 3rem; align-items: center; padding: 2rem 0; }
.hero { text-align: center; padding: 3rem 2rem; max-width: 700px; }
.hero-badge { display: inline-block; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: var(--accent-hover); background: rgba(99,102,241,0.1); padding: 0.3rem 0.8rem; border-radius: 50px; margin-bottom: 1rem; }
.hero-title { font-size: 3rem; margin-bottom: 1rem; line-height: 1.1; }
.hero-subtitle { font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2rem; max-width: 500px; margin-left: auto; margin-right: auto; }
.hero-actions { display: flex; gap: 1rem; justify-content: center; }

.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.25rem; width: 100%; }
.feature-card { padding: 1.75rem; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: var(--radius-lg); transition: all 0.2s; }
.feature-card:hover { transform: translateY(-3px); border-color: var(--border-active); }
.feature-icon { font-size: 2rem; margin-bottom: 0.75rem; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-sm); }
.feature-icon.blue { background: rgba(99,102,241,0.1); }
.feature-icon.green { background: rgba(16,185,129,0.1); }
.feature-icon.purple { background: rgba(168,85,247,0.1); }
.feature-icon.orange { background: rgba(245,158,11,0.1); }
.feature-icon.cyan { background: rgba(6,182,212,0.1); }
.feature-icon.red { background: rgba(239,68,68,0.1); }
.feature-card h3 { margin-bottom: 0.5rem; font-size: 1rem; }
.feature-card p { color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5; }
</style>

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Apply saved theme immediately before mount
const savedTheme = localStorage.getItem('novafit_theme') || 'dark'
document.documentElement.setAttribute('data-theme', savedTheme)

app.mount('#app')


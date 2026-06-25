import { defineStore } from 'pinia'
import axios from 'axios'
import API_URL from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    loading: false,
    theme: localStorage.getItem('novafit_theme') || 'dark',
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    userRole: (state) => {
      if (!state.user) return null
      if (state.user.is_superuser) return 'superadmin'
      if (state.user.is_administrativo) return 'admin'
      if (state.user.is_instructor) return 'instructor'
      if (state.user.is_nutricionista) return 'nutricionista'
      if (state.user.is_cliente) return 'cliente'
      return 'user'
    },
    // SuperAdmin puede hacer TODO
    isSuperAdmin: (state) => state.user?.is_superuser === true,
    isAdmin: (state) => {
      if (!state.user) return false
      return state.user.is_superuser || state.user.is_administrativo
    }
  },
  actions: {
    async fetchUser() {
      if (!this.accessToken) return null
      try {
        const response = await axios.get(`${API_URL}/users/me/`, {
          headers: { Authorization: `Bearer ${this.accessToken}` }
        })
        this.user = response.data
        return this.user
      } catch (error) {
        console.error('Error fetching user', error)
        this.logout()
        return null
      }
    },
    async login(username, password) {
      this.loading = true
      try {
        const response = await axios.post(`${API_URL}/token/`, {
          username, password
        })
        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh
        localStorage.setItem('access_token', this.accessToken)
        localStorage.setItem('refresh_token', this.refreshToken)
        
        await this.fetchUser()
        return true
      } catch (error) {
        console.error('Login error', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('novafit_theme', this.theme)
      document.documentElement.setAttribute('data-theme', this.theme)
    },
    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.theme)
    }
  }
})

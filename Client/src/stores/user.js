import { defineStore } from 'pinia'
// Import the persistedstate plugin

export const user = defineStore('user', {
  // Using the setup function approach to define state, getters, and actions
  state: () => ({
    username: '',
    token: '',
    refreshDate: null,
    loginAttempts: 0,
    lastLoginAttempt: null,
  }),
  getters: {
    expired: (state) => state.refreshDate.setMinutes(state.refreshDate.getMinutes() + 10) > new Date(),
    getLoginAttempts: (state) => state.loginAttempts,
    getLastLoginAttemptTime: (state) => state.lastLoginAttempt,
  },
  actions: {
    setDate() {
      this.refreshDate = new Date()
    },
    setLogin(username, token) {
      this.username = username
      this.token = token
      this.lastLoginAttempt = new Date()
      this.refreshDate = new Date()
    },
    setLogout() {
      this.username = ''
      this.token = ''
      this.refreshDate = null
    },
    setLoginAttempt() {
      this.loginAttempts++
      this.lastLoginAttempt = new Date()
    },
    resetLoginAttempts() {
      this.loginAttempts = 0
    },
  },
  // Configure persisted state
  persist: {
    enabled: true
  }
})

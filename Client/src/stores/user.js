import { defineStore } from 'pinia'
// Import the persistedstate plugin

export const useCounterStore = defineStore('user', {
  // Using the setup function approach to define state, getters, and actions
  state: () => ({
    username: '',
    token: '',
    refreshDate: null,
    loginAttempts: 0,
    lastLoginAttempt: null
  }),
  getters: {
    expired: (state) =>
      state.refreshDate.setMinutes(state.refreshDate.getMinutes() + 10) > new Date()
  },
  actions: {
    setDate() {
      this.refreshDate = new Date()
    },
    setLogin(username, token) {
      this.username = username
      this.token = token
    },
    setLogout() {
      this.username = ''
      this.token = ''
      this.refreshDate = null
    }
  },
  // Configure persisted state
  persist: {
    enabled: true
  }
})

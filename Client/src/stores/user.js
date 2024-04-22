import { defineStore } from 'pinia'

export const user = defineStore('user', {
  persist: {
    enabled: true,
  },
  state: () => ({
    username: '',
    token: '',
    refreshDate: null,
    loginAttempts: 0,
    lastLoginAttempt: null
  }),
  getters: {
    expired: (state) =>
      state.refreshDate.setMinutes(state.refreshDate.getMinutes() + 10) > new Date(),
    getLoginAttempts: (state) => state.loginAttempts,
    getLastLoginAttemptTime: (state) => state.lastLoginAttempt,
    getToken: (state) => state.token.toString()
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
    clearUser() {
      this.username = ''
      this.token = ''
      this.refreshDate = null
      this.loginAttempts = 0
      this.lastLoginAttempt = null
    },
    initializeDefaultState() {
      this.$reset();
    }
  },
})

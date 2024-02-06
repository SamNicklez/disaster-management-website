import { defineStore } from 'pinia'
// Import the persistedstate plugin

export const useCounterStore = defineStore('counter', {
  // Using the setup function approach to define state, getters, and actions
  state: () => ({
    username: '',
    token: '',
    refreshDate: new Date(),
  }),
  getters: {
    expired: (state) => state.refreshDate.setMinutes(state.refreshDate.getMinutes() + 10) > new Date(),
    
  },
  actions: {
    setDate() {
      this.refreshDate = new Date();
    }
  },
  // Configure persisted state
  persist: {
    enabled: true,
  },
})

import { defineStore } from 'pinia'
// Import the persistedstate plugin

export const useCounterStore = defineStore('counter', {
  // Using the setup function approach to define state, getters, and actions
  state: () => ({
    count: 0,
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
  // Configure persisted state
  persist: {
    enabled: true,
    // Optionally, you can customize the storage and paths
    // For example, to persist only specific parts of the state
    // paths: ['count'],
  },
})

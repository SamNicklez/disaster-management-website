import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const userData = defineStore('counter', () => {
  const username = ref('')
  const password = ref('')
  const email = ref('')
  return (username,password,email)
})

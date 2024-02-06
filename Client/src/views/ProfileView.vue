<template>
  <div>
    <h1>Profile page, this is a page to test state</h1>
    <p>Count: {{ count }}</p>
    <p>Double Count: {{ doubleCount }}</p>
    <v-btn @click="increment">Increment</v-btn>
  </div>
</template>

<script setup>
import { useCounterStore } from '../stores/user.js' // Adjust the path as necessary

// Use the store
const counterStore = useCounterStore()

// Extract state and actions from the store
const { count, doubleCount, increment } = counterStore
</script>

<script setup>
import Navbar from '@/components/NavComponent.vue'
</script>

<template>
  <div id="app">
    <Navbar />
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<style>
body, html, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  min-width: 100%;
  min-height: 100%;
}

.main {
  flex: 1;
  overflow: auto;
}
</style>


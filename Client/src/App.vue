<script setup>
import Navbar from '@/components/NavComponent.vue'
</script>

<script>
import { loadingBar } from './stores/loading.js';
import { alertStore } from './stores/alert';

export default {
  computed: {
    loading() {
      return loadingBar.loading;
    },
    alertText() {
      return alertStore.text;
    },
    isAlert() {
      return alertStore.display;
    },
    alertType() {
      return alertStore.type;
    },
    alertTitle() {
      return alertStore.title;
    },
  },
};
</script>

<template>
  <v-app>
    <v-main>
      <v-progress-linear
      :active="loading"
      indeterminate
      color="orange"
      height="10"
      top
    ></v-progress-linear>
      <Navbar />
      <v-alert :text="alertText" :title="alertTitle" v-if="isAlert" :type="alertType" style="margin:auto; max-width: 90%; min-height: 5vh; margin-bottom: 2.5vh;"></v-alert>
      <router-view />
    </v-main>
  </v-app>
</template>

<style>
body,
html,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #E8E9EB;
}

#template {
  background-color: #E8E9EB;
}

#app {
  display: flex;
  flex-direction: column;
  min-width: 100%;
  min-height: 100%;
  background-color: #E8E9EB;
}

.main {
  flex: 1;
  overflow: auto;
  background-color: #E8E9EB;
}

@font-face {
  font-style: normal;
  font-display: auto;
  font-family: "Poppins";
  src: url('/public/Poppins-Regular.ttf');
}

.v-application__wrap {
  background-color: #E8E9EB;
}
</style>


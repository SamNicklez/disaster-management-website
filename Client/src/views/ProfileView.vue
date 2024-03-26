<script setup>
import UserInfoComponent from '@/components/UserInfoComponent.vue'
</script>

<script></script>

<template>
  <div>
    <v-card
      class="mx-auto pa-12 pb-8"
      id="card"
      elevation="8"
      rounded="lg"
      style="margin-bottom: 10vh;"
    >
      <UserInfoComponent />
    </v-card>
  </div>
</template>

<style scoped>
#card {
  width: 65%;
}
</style>

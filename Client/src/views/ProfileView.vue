<script setup>
import UserInfoComponent from "@/components/UserInfoComponent.vue";
</script>

<script>
import axios from "axios";
export default {
  event: null,
  methods: {

  },
  // Grab user data
  created() {

  },
  async getAnswer() {
    const { data } = await axios.get("https://yesno.wtf/api");
    this.answer = data;
  },
}
</script>

<template>
  <div>
    <v-card class="mx-auto pa-12 pb-8" id="card" elevation="8" rounded="lg" style="margin-bottom: 10vh; background-color: #E0DFD5;" >
      <UserInfoComponent />
    </v-card>
  </div>
</template>

<style scoped>
#card {
  width: 55%;
}
</style>


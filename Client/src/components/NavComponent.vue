<script>
import '@mdi/font/css/materialdesignicons.css'
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    performSearch() {
      // Implement your search logic here
      console.log('Searching for:', this.searchQuery);
    },
    openProfile() {
      // Implement profile opening logic here
      console.log('Profile icon clicked');
    },
  },
};
</script>

<template>
  <v-container>
    <v-app-bar scroll-off-screen title="Disaster Donation">
      <v-spacer></v-spacer>
      <div class="nav-textfield">
        <v-text-field v-model="searchQuery" dense flat hide-details prepend-icon="mdi-magnify"
          @click:append="performSearch" @keyup.enter="performSearch" variant="outlined" label="Search for an Event"
          class="mx-auto" density="compact"></v-text-field>
      </div>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-btn icon @click="openProfile">
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </v-app-bar>
  </v-container>
</template>

<style scoped>
.nav-textfield {
  width: 35%;
  margin: 0 auto;
}
</style>

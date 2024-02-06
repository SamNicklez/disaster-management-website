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
      console.log('Searching for:', this.searchQuery);
    },
    openProfile() {
      this.$router.push('/profile');
    },
    openLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<template>
  <v-container>
    <v-app-bar scroll-behavior="hide">
        <v-toolbar-title>
          <v-btn text to="/" variant="plain" class="button">Disaster Donation</v-btn>
        </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="nav-textfield">
        <v-text-field v-model="searchQuery" dense flat hide-details prepend-icon="mdi-magnify"
          @click:append="performSearch" @keyup.enter="performSearch" variant="outlined" label="Search for an Event"
          class="mx-auto" density="compact"></v-text-field>
      </div>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-btn @click="openLogin">Login</v-btn>
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
  color:black;
}
.button{
  color: black;
  font-size: 0.75em;
  margin-left: 0.5vw;
}
.button:hover{
  color: black;
}
</style>

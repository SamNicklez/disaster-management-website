<script>
import { events } from '../stores/events.js'
const eventData = events()
  export default {
    event: null,
    methods: {
      /**
       * Routes to the home page
       */
      goHome() {
        this.$router.push('/');
      }
    },
    mounted() {
      this.event = eventData.getEvent(this.$route.params.id)
    }
  }
</script>

<template>
  <div class="card" v-if="this.event == null">
    Event page
    <br>
    
    <br>
    <v-btn to="/">Home</v-btn>
    <br>
    <v-btn to="/login">Login</v-btn>
  </div>
  <div class ="card" v-else>
    <h1>{{this.event.name}}</h1>
    <h2>{{this.event.location}}</h2>
    <h3>{{this.event.date}} at {{this.event.time}}</h3>
    <p>{{this.event.description}}</p>
    <v-btn to="/">Home</v-btn>
  </div>
</template>

<style scoped>
.card{
  background-color: #990000;
  width: 100%;
  height: 50%;
  text-align: center;
  color: white;
  font-size: 2em;
}
</style>
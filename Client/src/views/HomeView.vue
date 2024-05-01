<script setup>
import EventList from '../components/EventsListComponent.vue'
</script>

<template>
  <!-- <div class="card">
    <h1>Our Mission</h1>
    <br />
    <p>
      Our mission is to provide a platform for people to donate to the less fortunate. We believe
      that everyone should have access to the basic necessities of life. We are dedicated to helping
      those in need and we are committed to making a difference in the world.
    </p>
  </div> -->
  <EventList />
</template>

<style scoped>
.card {
  background-color: #f06543;
  width: auto;
  height: auto;
  text-align: center;
  font-size: 2em;
  border-radius: 10px;
  padding-left: 10vw;
  padding-right: 10vw;
  padding-bottom: 10vh;
  padding-top: 2.5vh;
  margin-left: 1vw;
  margin-right: 1vw;
  margin-bottom: 5vh;
  color: white;
}
</style>

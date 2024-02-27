<script>
export default {
  event: null,
  methods: {
  },
  created() {
    this.event = this.$route.params.event
  }
}
</script>

<template>
  <div class="card">
    <h1>{{ this.event.name }}</h1>
    <h2>{{ this.event.location }}</h2>
    <h3>{{ this.event.date }} at {{ this.event.time }}</h3>
    <p>{{ this.event.description }}</p>
  </div>
</template>

<style scoped>
.card {
  background-color: #F06543;
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
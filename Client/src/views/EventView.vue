<script>
export default {
  event_id: null,
  methods: {},
  created() {
    this.event_id = this.$route.params.id
  }
}
</script>

<template>
  <div class="card">
    Test
    <br>
    EVENT ID {{ event_id }}
  </div>
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

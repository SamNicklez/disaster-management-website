<script>
export default {
  data() {
    return {
      Events: [
        {name: 'Earthquake', location: 'Iowa City, IA', date: '10/10/2021', time: '10:00 AM', description: 'A 7.0 magnitude earthquake has struck Iowa City, IA. The city is in need of food, water, and medical supplies.', route_id: 3},
        {name: 'Hurricane', location: 'New Orleans, LA', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 5},
        {name: 'Tornado', location: 'Oklahoma City, OK', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 6},
        {name: 'Flood', location: 'Houston, TX', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 7},
        {name: 'Wildfire', location: 'Los Angeles, CA', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 8}
      ],
    };
  },
  methods: {
    goToEvent(id) {
      this.$router.push({ name: 'event', params: { id: id } });
    },
  },
};
</script>

<template>
    <v-container>
      <div>
        <h1>Active Disasters</h1>
        <v-row>
          <v-col cols="12" sm="6" v-for="event in Events" :key="event.route_id">
            <v-card @click="goToEvent(event.route_id)" class="ma-1" hoverable id="card">
              <v-card-title style="font-size: 2em;">{{ event.name }}</v-card-title>
              <v-card-text style="font-size: 1.1em;">
                <div><b>{{ event.location }}</b></div>
                <div>{{ event.date }} at {{ event.time }}</div>
                <div>{{ event.description }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </template>

<style scoped>
#card{
    padding: 1vh;
}


</style>

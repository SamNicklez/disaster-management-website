<template>
  <v-container>
    <div>
      <h1>Active Disasters</h1>
      <v-row>
        <v-col cols="12" sm="6" v-for="event in this.events" :key="event.route_id">
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

<script>
import { events } from '../stores/events.js'

export default {
  data() {
    return {
      eventData: null,
    };
  },
  computed: {
    /**
     * Get the list of events.
     * @returns {Array} The list of events.
     */
    events() {
      return this.eventData ? this.eventData.getEvents : [];
    }
  },
  mounted() {
    this.eventData = events();
  },
  methods: {
    /**
     * Navigate to the event details page.
     * @param {string} id - The ID of the event.
     */
    goToEvent(id) {
      this.$router.push({ name: 'event', params: { id: id } });
    },
  },
};
</script>

<style scoped>
#card {
  padding: 1vh;
}
</style>

<template>
  <v-container>
    <h1>Search Results:</h1>
    <v-row v-for="event in events" :key="event.event_id">
      <v-col cols="12">
        <v-card @click="goToEvent(event.event_id)" class="ma-1" hoverable>
          <v-card-title class="title">{{
            truncateName(event.event_name, 100) || 'Title Not Found'
          }}</v-card-title>
          <v-card-text>
            <div class="location-text">
              <b>{{ truncateName(event.location, 500) || 'Location Not Found' }}</b>
            </div>
            <div class="date-text">{{ formatDate(event.start_date) || 'Date Not Found' }}</div>
            <div class="description-text">
              {{ truncateName(event.description, 1000) || 'No Description' }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { alertStore } from '../stores/alert.js'
export default {
  data() {
    return {
      eventData: [],
      query: '',
    }
  },
  computed: {
    events() {
      return this.eventData
    }
  },
  mounted() {
    this.fetchEvents()
  },
  methods: {
    fetchEvents() {
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/event/search?query=' + this.$route.params.query,
      }

      axios
        .request(config)
        .then((response) => {
          this.eventData = response.data
        })
        .catch(() => {
          alertStore.showError('Failed to fetch events')
        })
    },
    goToEvent(id) {
      this.$router.push({ name: 'event', params: { id } })
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' })
    },
    truncateName(name, maxLength) {
      return name?.length > maxLength ? `${name.substring(0, maxLength)}...` : name
    }
  }
}
</script>

<style scoped>
.title {
  font-size: 2em;
}

.location-text,
.date-text,
.description-text {
  font-size: 1.5em;
  margin-bottom: 0.5vh;
}

#card {
  padding: 1vh;
}
</style>

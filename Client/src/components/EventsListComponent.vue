<template>
  <v-container>
    <div>
      <h1>Active Disasters</h1>
      <v-row>
        <v-col cols="12" sm="6" v-for="event in this.events" :key="event.event_id">
          <v-card @click="goToEvent(event.event_id)" class="ma-1" hoverable id="card">
            <v-card-title style="font-size: 2em">{{
              this.truncateName(event.event_name, 40) || 'Title Not Found'
            }}</v-card-title>
            <v-card-text style="font-size: 1.1em">
              <div>
                <b>{{ this.truncateName(event.location, 60) || 'Location Not Found' }}</b>
              </div>
              <br />
              <div>{{ this.formatDate(event.start_date) || 'Date Not Found' }}</div>
              <div>{{ this.truncateName(event.description, 60) || 'No Description' }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      eventData: null
    }
  },
  computed: {
    /**
     * Get the list of events.
     * @returns {Array} The list of events.
     */
    events() {
      return this.eventData
    }
  },
  mounted() {
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/event/GetAllEvents'
    }

    axios
      .request(config)
      .then((response) => {
        this.eventData = response.data.events.slice(0, 10)
        console.log(this.eventData)
      })
      .catch((error) => {
        console.log(error)
      })
  },
  methods: {
    /**
     * Navigate to the event details page.
     * @param {string} id - The ID of the event.
     */
    goToEvent(id) {
      this.$router.push({ name: 'event', params: { id: id } })
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const year = date.getFullYear()
      return `${month.toString().padStart(2, '0')}/${day.toString().padStart(2, '0')}/${year}`
    },
    truncateName(name, maxLength) {
      if (!name) return name
      if (name.length > maxLength) {
        return name.substring(0, maxLength) + '...'
      }
      return name
    }
  }
}
</script>

<style scoped>
#card {
  padding: 1vh;
}
</style>

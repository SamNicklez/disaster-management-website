<template>
  <v-container style="max-width: 60%">
    <div>
      <h3>Event Details</h3>
      <div class="request">
        <h4>Disaster Type: {{ eventDetails.name }}</h4>
        <h4>Location: {{ eventDetails.location }}</h4>
        <h4>Started on: {{ eventDetails.date }}</h4>
        <div v-if="role == 'Recipiant' || role == 'Admin'">
          <v-btn color="primary" variant="outlined" style="margin-top: 1.5vh" @click="requestItems()">Request Items</v-btn>
        </div>
      </div>
    </div>
    <div v-if="requests.length > 0">
      <v-card-title class="text-h5 py-3">Current Items Needed</v-card-title>
      <v-row>
        <v-col
          cols="12"
          md="6"
          v-for="(request, request_id) in requests"
          :key="request_id"
          class="my-2"
        >
          <v-card class="pa-3" elevation="2" style="background-color: #f5f5f5">
            <v-card-title class="headline mb-1">Item Needed: {{ request.item_name }}</v-card-title>
            <v-card-subtitle class="grey--text font-weight-light mb-2"
              >Requested On: {{ request.date_requested }}</v-card-subtitle
            >
            <v-card-text class="body-1">
              <div>Quantity Required: {{ request.quantity }}</div>
            </v-card-text>
            <v-card-actions>
              <v-btn
                v-if="role == 'Donor' || role == 'Admin'"
                @click="pledgeItem(request)"
                color="primary"
                variant="outlined"
                >Fill Request</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <v-card-title>No items needed at this time, please check back later.</v-card-title>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'
export default {
  data() {
    return {
      event_id: null,
      role: null,
      eventDetails: {},
      requests: []
    }
  },
  methods: {
    fetchEventDetails() {
      let userData = user()
      let token = userData.getToken
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/event/GetAllItemRequestsByEventId?event_id=' + this.event_id,
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
      axios
        .request(config)
        .then((response) => {
          this.eventDetails = {
            id: response.data.event_id,
            name: response.data.event_name,
            location: response.data.location,
            date: this.formatDate(response.data.start_date)
          }
          this.requests = response.data.requests
          let list = []
          for (let i = 0; i < this.requests.length; i++) {
            let json = {
              id: this.requests[i].request_id,
              item_name: this.requests[i].item_name,
              quantity: this.requests[i].quantity_remaining,
              date_requested: this.formatDate(this.requests[i].created_date)
            }
            list.push(json)
          }
          this.requests = list
        })
        .catch(() => {
          alertStore.showError('Error', 'An error occurred while fetching event details.')
        })
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
    }
  },
  created() {
    this.event_id = this.$route.params.id
  },
  mounted() {
    let userData = user()
    let token = userData.getToken
    if (token && token != null && token != undefined && token != '') {
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/getRole',
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
      axios
        .request(config)
        .then((response) => {
          this.role = response.data.role
        })
        .catch(() => {
          alertStore.showError('Error', 'An error occurred while fetching your user role.')
        })
    } else {
      this.role = 'None'
    }
    this.fetchEventDetails()
  }
}
</script>

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

.request {
  background-color: #f7f7f7;
  color: #333;
  padding: 20px;
  margin-top: 10px;
  border-radius: 5px;
}

h3,
h4 {
  color: #333;
}

.v-card {
  transition: box-shadow 0.3s ease;
  cursor: pointer;
}

.v-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.v-btn {
  margin-top: auto; /* Aligns button to bottom if card content varies in height */
}
</style>

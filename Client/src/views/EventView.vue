<template>
  <div>
    <h3>Event Details</h3>
    <div class="request">
      <h4>Event ID: {{ event_id }}</h4>
      <h4>Role: {{ role }}</h4>
    </div>
  </div>
  <div v-if="requests.length > 0">
      <v-card-title>Current Items Needed</v-card-title>
      <v-row>
      <v-col cols="12" md="6" lg="3" v-for="(request, request_id) in requests" :key="request_id" class="my-2">
        <v-card style="background-color: #f5f5f5;">
          <v-card-title>Item Needed: {{ request.item_name }}</v-card-title>
          <v-card-subtitle>Requested On: {{ request.date_requested }}</v-card-subtitle>
          <v-card-text>
            <div>Quantity Required: {{ request.quantity }}</div>
          </v-card-text>
          <div v-if="role == 'Donor' || role == 'Admin'">
            <v-btn @click="pledgeItem(request.request_id, request.item_id, request.quantity)" color="primary">Pledge Item</v-btn>
          </div>
        </v-card>
      </v-col>
      </v-row>
    </div>
    <div v-else>
      <v-card-title>No items needed at this time.</v-card-title>
    </div>
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
              request_id: this.requests[i].request_id,
              item_name: this.requests[i].items[0].item_name,
              item_id: this.requests[i].items[0].item_id,
              quantity: this.requests[i].items[0].quantity,
              request_item_id: this.requests[i].items[0].item_id,
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
    },
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
</style>

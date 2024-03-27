<template>
  <div class="card">
    <h2>{{ eventDetails.event_name }}</h2>
    <p>Location: {{ eventDetails.location }}</p>
    <p>Description: {{ eventDetails.description }}</p>
  </div>
  <div class="request-button" v-if="isRecipient">
    <v-btn color="secondary" @click="handleRequest">Request</v-btn>
  </div>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4" lg="3" v-for="request in eventDetails.requests" :key="request.request_id">
        <v-card class="ma-2">
          <v-card-text>
            <p><b>Created:</b> {{ formatDate(request.created_date) }}</p>
            <p><b>Fulfilled:</b> {{ request.is_fulfilled ? 'Yes' : 'No' }}</p>
            <div v-if="request.items && request.items.length">
              <v-list dense>
                <v-subheader><b>Items Requested</b></v-subheader>
                <v-list-item v-for="item in request.items" :key="item.requestitem_id">
                  <v-list-item-content>
                    {{ item.item_name }} : {{ item.quantity }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </div>
            <div v-else>
              No items requested.
            </div>
            <v-btn color="primary" class="mt-3" v-if="isDonor" @click="respondToRequest(request.request_id)">Respond to Request</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { user } from '../stores/user.js'

export default {
  data() {
    return {
      event_id: null,
      eventDetails: {},
      isDonor: false,
      isRecipient: false,
    };
  },
  methods: {
    fetchEventDetails() {
      const config = {
        method: 'get',
        url: `http://127.0.0.1:5000/event/GetAllItemRequestsByEventId?event_id=${this.event_id}`
      };
      
      axios.request(config)
        .then(response => {
          this.eventDetails = response.data; 
        })
        .catch(error => {
          console.error('Error fetching event details:', error);
        });
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString(undefined, {year: 'numeric', month: 'long', day: 'numeric'});
    },

    verifyUserRole() {
      let userData = user();
      const token = userData.getToken;
      const headers = {
        'Authorization': `Bearer ${token}`
      };
      axios.post('http://127.0.0.1:5000/users_bp/verifyDonor', {}, { headers: headers })
      .then(response => {
        this.isDonor = true; 
      })
      .catch(error => {
        console.error('Error verifying user role:', error);
        this.isDonor = false; 
      });
    },
    verifyRecipientRole() {
      let userData = user();
      const token = userData.getToken;
      const headers = {
        'Authorization': `Bearer ${token}`
      };
      axios.post('http://127.0.0.1:5000/users_bp/verifyDonor', {}, { headers: headers })
      .then(response => {
        this.isRecipient = true;
      })
      .catch(error => {
        console.error('Error verifying recipient role:', error);
        this.isRecipient = false;
      });
    },
  },
  created() {
    this.event_id = this.$route.params.id;
    this.fetchEventDetails();
    this.verifyUserRole();
    this.verifyRecipientRole();
  },
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

h3, h4 {
  color: #333;
}

</style>

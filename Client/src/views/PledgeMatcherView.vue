<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <v-card>
          <v-card-title>Active Requests</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="requests"
              :items-per-page="5"
              class="elevation-1"
              @click:row="handleRequestClick"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card>
          <v-card-title>Match Actions</v-card-title>
          <v-card-text>
            <v-btn color="primary" @click="autoMatch">Auto Match</v-btn>
            <v-card>
              <v-card-title>Request Details</v-card-title>
              <v-card-text>
                {{ selectedRequest }}
              </v-card-text>
            </v-card>
            <v-card>
              <v-card-title>Donor Details</v-card-title>
              <v-card-text>
                {{ selectedDonor }}
              </v-card-text>
            </v-card>
            <v-btn color="primary" @click="confirmMatch">Confirm Match</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card>
          <v-card-title>Matching Pledges</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="donorHeaders"
              :items="pledges"
              :items-per-page="5"
              class="elevation-1"
              @click:row="handleDonorClick"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
export default {
  name: 'ActiveRequestsTable',
  data() {
    return {
      requests: [],
      pledges: [],
      headers: [
        { title: 'Item Name', key: 'item.ItemName', align: 'start' },
        { title: 'Created Date', key: 'created_date', align: 'start' },
        { title: 'Location', key: 'event.location', align: 'start' },
        { title: 'Quantity Needed', key: 'quantity_remaining', align: 'start' }
      ],
      donorHeaders: [
        { title: 'Location', key: 'location.State', align: 'start' },
        { title: 'Quantity Available to Give', key: 'quantity_remaining', align: 'start' }
      ],
      selectedRequest: null,
      selectedDonor: null
    }
  },
  mounted() {
    this.fetchActiveRequests()
  },
  methods: {
    fetchActiveRequests() {
      let userData = user()
      let config = {
        method: 'get',
        url: 'http://127.0.0.1:5000/match/grabAllActiveRequests',
        headers: {
          Authorization:
            'Bearer ' + userData.token
        }
      }

      axios
        .request(config)
        .then((response) => {
          this.requests = response.data
        })
        .catch((error) => {
          console.error('Error fetching active requests:', error)
        })
    },
    handleRequestClick(event, row) {
      let userData = user()
      this.selectedRequest = row.item
      let data = JSON.stringify({
        item_id: row.item.item.ItemID
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/match/grabPotentialMatches',
        headers: {
          'Content-Type': 'application/json',
          Authorization:
            'Bearer ' + userData.token
        },
        data: data
      }

      axios
        .request(config)
        .then((response) => {
          if(response.data.length === 0){
            this.pledges = [{
              location: {
                State: 'No matches found'
              },
              quantity_remaining: 'No matches found'
            
            }]
          }
          else{
            this.pledges = response.data
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const options = {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric'
      }
      return date.toLocaleDateString('en-US', options)
    },
    handleDonorClick(event, row) {
      this.selectedDonor = row.item
    },
    autoMatch() {
      if (!this.selectedRequest){
        return
      }
      
    },
    confirmMatch() {
      if (!this.selectedRequest || !this.selectedDonor) {
        return
      } 
      // Confirm the match between selectedRequest and selectedDonor
      console.log('Match confirmed between:', this.selectedRequest, this.selectedDonor)
    }
  }
}
</script>

<style scoped>
.v-card {
  margin-bottom: 5vh;
}

.v-card-text {
  padding: 1vh;
}

.v-btn {
  margin-bottom: 1vh;
}

/* This can help visually separate the buttons from the rest of the content */
.v-card-title,
.v-card-text {
  margin-bottom: 1vh;
}
</style>

<template>
    <v-container>
      <v-row>
        <v-col cols="6">
          <v-card>
            <v-card-title>
              Active Requests
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="requests"
                :items-per-page="5"
                class="elevation-1"
                @click:row="handleRowClick"
              ></v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6">
          
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ActiveRequestsTable',
    data() {
      return {
        requests: [],
        headers: [
          {
            text: 'Created Date',
            align: 'start',
            sortable: false,
            value: 'created_date',
          },
          { text: 'Item Name', value: 'item.ItemName' },
          { text: 'Location', value: 'event.location' },
          { text: 'Quantity Remaining', value: 'quantity_remaining' },
        ],
      };
    },
    mounted() {
      this.fetchActiveRequests();
    },
    methods: {
      fetchActiveRequests() {
        let config = {
          method: 'get',
          url: 'http://127.0.0.1:5000/match/grabAllActiveRequests',
          headers: {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiUm9sZUlEIjoxLCJEYXRlQ3JlYXRlZCI6IjIwMjQtMDMtMjBUMTA6MzY6MzQuMzIwMzk0In0.If6UserOfiFYv31G8hVm-b8cAVEJBvg-rsYZlGk4i2A'
          }
        };
  
        axios.request(config)
          .then((response) => {
            this.requests = response.data;
          })
          .catch((error) => {
            console.error('Error fetching active requests:', error);
          });
      },
      handleRowClick(row) {
        console.log('Row clicked:', row);
        // You can expand this method to perform other actions
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  
<template>
    <v-card class="mx-auto" max-width="800">
      <v-card-title>
        Your Notifications
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text>
        <v-list dense> <!-- Added 'dense' for a more compact list -->
            <v-list-item v-for="notification in notifications" :key="notification.id" class="notification-item">
            <v-row align="center"> <!-- This will vertically center the content -->
                <v-col cols="9">
                <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
                </v-col>
                <v-col cols="3" class="text-end">
                <span class="caption">{{ notification.created_date }}</span>
                </v-col>
            </v-row>
            </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </template>
  
  <style scoped>
  .notification-item {
    border-bottom: 1px solid #eee; /* Add a subtle separator */
  }
  </style>
  
  
  <script>
import axios from 'axios';
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'
  export default {
    data() {
      return {
        notifications: [],
      };
    },
    created() {
      this.fetchNotifications();
    },
    methods: {
      fetchNotifications() {
        let userData = user();
        axios.get('http://127.0.0.1:5000/notification/get', {
            headers: {
                Authorization: 'Bearer ' + userData.getToken
            }
        })
          .then(response => {
            this.notifications = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the notifications:', error);
          });
      },
    },
  };
  </script>
  
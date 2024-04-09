<template>
    <v-card class="mx-auto" max-width="800">
      <v-card-title>
        Your Notifications
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="notification in notifications"
            :key="notification.id"
          >
            <v-list-item-content>
              <v-list-item-title>{{ notification.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ notification.message }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </template>
  
  <script>
  import axios from 'axios';
  
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
        axios.get('http://127.0.0.1:5000/users_bp/getAllUsers', {
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
  
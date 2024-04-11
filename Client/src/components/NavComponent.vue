<template>
  <v-container>
    <v-app-bar scroll-behavior="hide">
      <v-toolbar-title>
        <v-btn text to="/" variant="plain" class="button">Disaster Donation</v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field
        id="search"
        v-model="searchQuery"
        dense
        flat
        hide-details
        prepend-icon="mdi-magnify"
        @click:append="performSearch"
        @keyup.enter="performSearch"
        variant="outlined"
        label="Search for an Event"
        class="mx-auto"
        density="compact"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <v-btn @click="openLogin">Login</v-btn>
      <v-btn icon @click="openProfile">
        <v-icon size="large">mdi-account-circle</v-icon>
      </v-btn>
      <v-menu transition="scale-transition" :close-on-content-click="false">
        <template v-slot:activator="{ props }">
          <v-btn icon @click="populateNotifications" v-bind="props">
            <v-icon size="large">mdi-bell</v-icon>
          </v-btn>
        </template>
        <v-list lines="three" style="min-width: 25vw" v-if="this.notifications.length != 0">
          <v-list-item
            v-for="(item, i) in notifications"
            :key="i"
            append-icon="mdi-close"
            @click="closeNoti(i)"
          >
            <v-list-item-title>{{ item.message }}</v-list-item-title>
            <!-- <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle> -->
          </v-list-item>
        </v-list>
        <v-list lines="three" style="min-width: 25vw" v-else>
          <v-list-item>
            <v-list-item-title>No New Notifications</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </v-container>
</template>

<script>
import '@mdi/font/css/materialdesignicons.css'
import { user } from '../stores/user.js'
import axios from 'axios'
export default {
  data() {
    return {
      searchQuery: '',
      notifications: []
    }
  },
  methods: {
    /**
     * Perform a search
     */
    performSearch() {
      let route_name = this.$route.name
      this.$router.push({ name: 'search', params: { query: this.searchQuery } }).then(() => {
        if (route_name === 'search') {
          this.$router.go()
        }
        this.searchQuery = ''
      })
    },
    /**
     * Open the profile page
     */
    openProfile() {
      this.$router.push('/profile')
    },
    /**
     * Open the login page
     */
    openLogin() {
      this.$router.push('/login')
    },
    /**
     * Populates the notifications
     */
    populateNotifications() {
      let userData = user()
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/notification/viewUnread',
        headers: {
          Authorization: 'Bearer ' + userData.getToken
        }
      }
      axios
       .request(config)
       .then(response => {
          this.notifications = response.data
        })
    },
    /**
     * Closes a notification
     * @param {int} index
     */
     closeNoti(index) {
      let userData = user()
        const notificationId = this.notifications[index].notification_id;
          axios.post(`http://127.0.0.1:5000/notification/markRead/${notificationId}`, {}, {
            headers: {
              'Authorization': `Bearer ` + userData.getToken, 
            }
          })
          .then(response => {
            console.log(response.data.message); // "Notification marked as read"
            // Remove the notification from the list after successfully marking it as read
            this.notifications.splice(index, 1);
          })
          .catch(error => {
            console.error("Error marking notification as read:", error);
          });
    }
  }
}
</script>

<style scoped>
.nav-textfield {
  width: 35em;
  margin: 0 auto;
  color: black;
}

.button {
  color: black;
  font-size: 0.75em;
  margin-left: 0.5vw;
}

.button:hover {
  color: black;
}
</style>

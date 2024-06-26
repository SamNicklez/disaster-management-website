<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-h5">Notification Management</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-autocomplete
                v-model="selectedUserId"
                :items="users"
                item-title="displayText"
                item-value="id"
                label="Select User"
                return-object
                single-line
                clearable
              >
              </v-autocomplete>
              <v-text-field
                v-model="notificationTitle"
                label="Notification Title"
                required
                :rules="messageRules"
              ></v-text-field>
              <v-text-field
                v-model="notificationMessage"
                label="Notification Message"
                required
                :rules="messageRules"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="success" :disabled="!valid" @click="createNotification">Send</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'
export default {
  data: () => ({
    valid: false,
    users: [],
    selectedUserId: null,
    notificationTitle: '',
    notificationMessage: '',
    messageRules: [(v) => !!v || 'Notification message is required']
  }),
  created() {
    this.fetchAllUsers()
  },

  methods: {
    async createNotification() {
      const userData = user()
      if (!this.selectedUserId || !this.notificationMessage || !this.notificationTitle) {
        alertStore.showError('Please select a user and enter a message.')
        return
      }

      const payload = {
        user_id: this.selectedUserId.id,
        title: this.notificationTitle,
        message: this.notificationMessage
      }

      try {
        await axios.post('http://127.0.0.1:5000/notification/create', payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        })

        this.notificationMessage = ''
        this.notificationTitle = ''
        this.selectedUserId = null
        alertStore.showSuccess('Notification created successfully.')
      } catch (error) {
        console.error('Failed to create notification:', error)
        alertStore.showError('Failed to send notification. Please try again.')
      }
    },
    fetchAllUsers() {
      let userData = user()
      axios
        .get('http://127.0.0.1:5000/users_bp/getAllUsers', {
          headers: {
            Authorization: 'Bearer ' + userData.getToken
          }
        })
        .then((response) => {
          this.users = response.data.map((user) => {
            return {
              displayText: `ID: ${user.id} | EMAIL: ${user.email}`,
              email: user.email,
              id: user.id
            }
          })
        })
        .catch((error) => {
          console.error('Failed to fetch users:', error)
          alertStore.showError('Error fetching users')
        })
    }
  }
}
</script>

<style scoped></style>

<template>
  <v-dialog v-model="dialog" width="auto" persistent>
    <v-card>
      <v-alert
        v-model="alert"
        class="alert"
        density="compact"
        type="warning"
        :title="alertText"
        variant="tonal"
      ></v-alert>
      <v-card-text v-if="isLogin">
        Account not verified! An email has been sent to your email address, please enter the code to
        verify your account.
      </v-card-text>
      <v-card-text v-else>
        Account created! An email has been sent to your email address, please enter the code to
        verify your account.
      </v-card-text>
      <v-text-field
        variant="outlined"
        label="Verification Code"
        v-model="verifyCode"
        required
        dense
        outlined
        placeholder="Enter verification code"
        maxLength="6"
        style="min-width: 50%; margin: auto; margin-top: 2.5vh"
      >
      </v-text-field>
      <v-card-actions>
        <v-btn color="primary" block @click="verify()">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'
import { alertStore } from '../stores/alert.js'
export default {
  props: ['email', 'login'],
  data() {
    return {
      dialog: true,
      alert: false,
      alertText: '',
      verifyCode: '',
      username: this.email,
      isLogin: this.login
    }
  },
  methods: {
    verify() {
      let data = JSON.stringify({
        email: this.username.toLowerCase(),
        verification: parseInt(this.verifyCode)
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/verify',
        headers: {
          'Content-Type': 'application/json'
        },
        data: data
      }

      axios
        .request(config)
        .then(() => {
          alertStore.title = 'Signup Successful'
          alertStore.text = `You have successfully signed up, please login to continue.`
          alertStore.type = 'success'
          alertStore.overRide = true
          alertStore.display = true
          this.$router.push({ name: 'login' })
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.alertText = 'Invalid verification code'
          } else if (error.response.status === 500) {
            this.alertText = 'Internal server error'
          } else {
            this.alertText = 'An error occurred'
          }
          this.alert = true
        })
    }
  }
}
</script>

<style></style>

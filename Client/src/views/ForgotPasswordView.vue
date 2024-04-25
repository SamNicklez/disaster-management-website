<template>
  <div class="login-card">
    <v-card
      class="mx-auto pa-12 pb-8"
      id="card"
      elevation="8"
      rounded="lg"
      style="margin-bottom: 10vh"
    >
      <div class="text-h5 text-center mb-8">Forgot Password</div>
      <div class="text-subtitle-1 text-medium-emphasis">Enter Email</div>
      <v-text-field
        density="compact"
        v-model="username"
        maxLength="100"
        placeholder="Email"
        prepend-inner-icon="mdi-account-circle"
        variant="outlined"
      ></v-text-field>
      <div class="text-subtitle-1 text-medium-emphasis">Confirm Email</div>
      <v-text-field
        density="compact"
        v-model="confirm_username"
        maxLength="100"
        placeholder="Confirm Email"
        prepend-inner-icon="mdi-account-circle"
        variant="outlined"
      ></v-text-field>
      <v-btn
        block
        class="mb-8"
        color="#F06543"
        size="large"
        variant="tonal"
        id="verifyEmail"
        @click="verifyEmail"
      >
        Reset Password
      </v-btn>
      <v-card-text class="text-center">
        <a class="text-decoration-none" style="color: #313638; cursor: pointer" @click="goToLogin">
          Head back to login <v-icon icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
    </v-card>
  </div>
  <v-dialog v-model="dialog" width="auto">
    <v-card>
      <v-alert
        v-model="alert"
        class="alert"
        density="compact"
        type="warning"
        :title="alertText"
        variant="tonal"
      ></v-alert>
      <v-card-text>
        Please verfiy your email! If a account with the provided email address exists, a code was
        sent to your email.
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
  data() {
    return {
      dialog: false,
      alert: false,
      alertText: '',
      verifyCode: '',
      username: '',
      confirm_username: ''
    }
  },
  methods: {
    verify() {
      let data = JSON.stringify({
        email: this.username.toLowerCase(),
        code: parseInt(this.verifyCode)
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/verifyforgotpassword',
        headers: {
          'Content-Type': 'application/json'
        },
        data: data
      }

      axios
        .request(config)
        .then((response) => {
          alertStore.showSuccess(response.data.message)
          this.dialog = false
        })
        .catch(() => {
          this.alertText = 'Invalid verification code'
          this.alert = true
        })
    },
    goToLogin() {
      this.$router.push({ name: 'login' })
    },
    verifyEmail() {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
      if (!emailRegex.test(this.username)) {
        alertStore.showWarning('Invalid email format', 'Error')
        return
      }
      if (this.username !== this.confirm_username) {
        alertStore.showWarning('Emails do not match', 'Error')
        return
      }

      let data = JSON.stringify({
        email: this.username.toLowerCase()
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/sendforgotpasswordemail',
        headers: {
          'Content-Type': 'application/json'
        },
        data: data
      }

      axios
        .request(config)
        .then(() => {
          this.dialog = true
        })
        .catch((error) => {
          alertStore.showError(error.message)
        })
    }
  }
}
</script>

<style scoped>
#card {
  width: 35em;
}
</style>

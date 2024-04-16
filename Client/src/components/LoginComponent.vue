<template>
  <VerifyComponentVue v-if="dialog" :email="username" :login="true" />
  <div class="login-card">
    <v-card
      class="mx-auto pa-12 pb-8"
      id="card"
      elevation="8"
      rounded="lg"
      style="margin-bottom: 10vh"
    >
      <div class="text-h5 text-center mb-8">Login</div>
      <div class="text-subtitle-1 text-medium-emphasis">Email</div>
      <v-text-field
        density="compact"
        v-model="username"
        maxLength="100"
        placeholder="Email"
        prepend-inner-icon="mdi-account-circle"
        variant="outlined"
      ></v-text-field>
      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password
        <a
          class="text-caption text-decoration-none"
          style="color: #313638; cursor: pointer"
          @click="forgotPass"
        >
          Forgot login password?</a
        >
      </div>
      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        v-model="password"
        placeholder="Enter your password"
        maxLength="15"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
      ></v-text-field>
      <v-card class="mb-12" color="#313638" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          Warning: After 3 consecutive failed login attempts, you account will be temporarily locked
          for 10 minutes. If you must login now, you can also click "Forgot login password?" above
          to reset the login password.
        </v-card-text>
      </v-card>
      <v-btn
        block
        class="mb-8"
        color="#F06543"
        size="large"
        variant="tonal"
        id="loginButton"
        @click="login"
      >
        Log In
      </v-btn>
      <v-card-text class="text-center">
        <a class="text-decoration-none" style="color: #313638; cursor: pointer" @click="goToSignUp">
          Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import VerifyComponentVue from './VerifyComponent.vue'
</script>

<script>
import '@mdi/font/css/materialdesignicons.css'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'
import axios from 'axios'
export default {
  data: () => ({
    visible: false,
    username: '',
    password: '',
    dialog: false
  }),
  methods: {
    /**
     * Routes to the signup page
     */
    goToSignUp() {
      this.$router.push({ name: 'signup' })
    },
    /**
     * Logs the user in
     */
    login() {
      let userData = user()
      console.log(userData)
      if (this.username != '' && this.password != '') {
        if (
          userData.getLoginAttempts >= 3 &&
          this.minutesBetweenDatesVal(userData.getLastLoginAttemptTime) >= 1
        ) {
          if (userData.getLoginAttempts == 3) {
            userData.setLoginAttempt()
            alertStore.showWarning(
              `You have exceeded the maximum number of login attempts. Please try again in 10 minutes.`,
              'Account Locked'
            )
            return
          } else {
            alertStore.showWarning(
              `You have exceeded the maximum number of login attempts. Please try again in ${this.minutesBetweenDates(this.userData.getLastLoginAttemptTime)}`,
              'Account Locked'
            )
            return
          }
        } else {
          if (userData.getLoginAttempts >= 3) {
            userData.resetLoginAttempts()
          }
          userData.setLoginAttempt()
          let data = JSON.stringify({
            email: this.username.toLowerCase(),
            password: this.password
          })

          let config = {
            method: 'post',
            maxBodyLength: Infinity,
            url: 'http://127.0.0.1:5000/users_bp/signin',
            headers: {
              'Content-Type': 'application/json'
            },
            data: data
          }

          axios
            .request(config)
            .then((response) => {
              console.log(JSON.stringify(response.data))
              userData.setLogin(this.username.toLowerCase(), response.data.token)
              alertStore.showSuccess(`You have successfully logged in.`, 'Login Successful', true)
              this.$router.push({ name: 'home' })
            })
            .catch((error) => {
              try {
                if (error.response.status === 401) {
                  alertStore.showWarning(`Invalid username or password.`, 'Invalid Credentials')
                } else if (error.response.status === 405) {
                  this.dialog = true
                } else {
                  alertStore.showError(`An error occurred.`)
                }
              } catch (error) {
                alertStore.showError('an error occurred')
              }
            })
        }
      }
    },
    /**
     * Routes to the forgot password page
     */
    forgotPass() {
      console.log('Forgot password')
      //Router push to somewhere to reset password
    },
    /**
     * Calculates the minutes between the current time and the input date and returns a stringified version of the minutes or seconds
     * @param {Date} inputDateString
     */
    minutesBetweenDates(inputDateString) {
      try {
        const inputDate = new Date(inputDateString)
        const tenMinutesLater = new Date(inputDate.getTime() + 10 * 60000)
        const now = new Date()
        const diffInMilliseconds = tenMinutesLater.getTime() - now.getTime()
        if (diffInMilliseconds < 60000) {
          return Math.floor(diffInMilliseconds / 1000) + ' seconds.'
        } else {
          return Math.floor(diffInMilliseconds / 60000) + ' minutes.'
        }
      } catch (error) {
        return '10 minutes.'
      }
    },
    /**
     * Calculates the minutes between the current time and the input date
     * @param {Date} inputDateString
     */
    minutesBetweenDatesVal(inputDateString) {
      const inputDate = new Date(inputDateString)
      const tenMinutesLater = new Date(inputDate.getTime() + 10 * 60000)
      const now = new Date()
      const diffInMilliseconds = tenMinutesLater.getTime() - now.getTime()
      return diffInMilliseconds
    }
  }
}
</script>

<style scoped>
#card {
  width: 35em;
}
</style>

<template>
  <v-card-title>User Profile</v-card-title>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field label="Email" v-model="email" :readonly="!edit" outlined dense></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field label="Role" v-model="role" :readonly="!edit" outlined dense></v-text-field>
      </v-col>
    </v-row>
    <v-btn variant="outlined" @click="this.dialog = true">Reset Password</v-btn>
  </v-container>
  <v-card-title>Address Information</v-card-title>
  <v-container>
    <v-text-field
      v-if="edit"
      class="mb-3"
      :loading="loading"
      outlined
      clearable
      label="Add Address"
      v-model="searchQuery"
      @keyup="debouncedFetchAddresses"
      append-inner-icon="mdi-magnify"
      @click:clear="checkClear"
    ></v-text-field>
    <v-list v-if="addresses.length" dense>
      <v-list-item
        v-for="address in addresses"
        :key="address.properties.place_id"
        @click="selectAddress(address)"
      >
        <v-list-item-title>{{ address.properties.formatted }}</v-list-item-title>
      </v-list-item>
    </v-list>
    <v-text-field
      readonly
      outlined
      label="Address"
      v-model="addressDetails.address"
      dense
    ></v-text-field>
    <v-text-field
      v-if="edit"
      outlined
      label="Address Line 2"
      v-model="addressDetails.addressLine2"
      dense
    ></v-text-field>
    <v-text-field readonly outlined label="City" v-model="addressDetails.city" dense></v-text-field>
    <v-text-field
      readonly
      outlined
      label="State"
      v-model="addressDetails.state"
      dense
    ></v-text-field>
    <v-text-field
      readonly
      outlined
      label="Zipcode"
      v-model="addressDetails.zipcode"
      dense
    ></v-text-field>
    <v-btn :color="edit ? 'success' : 'primary'" @click="toggleEdit">
      <v-icon left>{{ edit ? 'mdi-content-save' : 'mdi-pencil' }}</v-icon>
      {{ edit ? 'Save' : 'Edit' }}
    </v-btn>
  </v-container>
  <div v-if="role == 'Donor' || 'Admin'">
    <v-card-title>Pledges</v-card-title>
    <v-btn @click="routePledge" color="primary">Create a Pledge</v-btn>
    <div v-if="activePledges.length != 0">
      <v-card-title>Your Active Pledges</v-card-title>
      <v-row>
        <v-col
          cols="12"
          md="6"
          lg="4"
          v-for="(pledge, pledge_id) in activePledges"
          :key="pledge_id"
          class="my-2"
        >
          <v-card style="background-color: #f5f5f5">
            <v-card-title>{{ pledge.item_name }}</v-card-title>
            <v-card-text>
              <div>Quantity Donated: {{ pledge.quantity_given }}</div>
              <div>Quantity Remaining: {{ pledge.quantity_remaining }}</div>
            </v-card-text>
            <v-btn color="primary" @click="cancelpledge(pledge_id)">Cancel Pledge</v-btn>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-if="pastPledges.length != 0">
      <v-card-title>Your Past Pledges</v-card-title>
      <v-row>
        <v-col
          cols="12"
          md="6"
          lg="3"
          v-for="(pledge, pledge_id) in pastPledges"
          :key="pledge_id"
          class="my-2"
        >
          <v-card style="background-color: #f5f5f5">
            <v-card-title>{{ pledge.item_name }}</v-card-title>
            <v-card-text>
              <div>Quantity Given: {{ pledge.quantity_given }}</div>
              <div>Quantity Remaining: {{ pledge.quantity_remaining }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
  <div v-if="role == 'Recipient' || 'Admin'">
    <div v-if="activeRequests != 0">
      <v-card-title>Your Requests</v-card-title>
    </div>
    <div v-if="pastRequests != 0">
      <v-card-title>Your Past Requests</v-card-title>
    </div>
  </div>
  <v-card-title v-if="role == 'Admin'">Admin Settings</v-card-title>
  <v-container v-if="role == 'Admin'">
    <v-btn @click="createItem" color="primary" style="margin-right: 5vh"
      >Items and Category Management</v-btn
    >
    <v-btn @click="routeEvent" color="primary" style="margin-right: 5vh">Event Management</v-btn>
    <v-btn @click="routePledgeMatcher" color="primary">Pledge Matcher</v-btn>
  </v-container>
  <v-dialog v-model="dialog" style="max-width: 40vw" @click:outside="resetForm">
    <v-card>
      <v-alert
        v-if="showAlert"
        class="alert"
        density="compact"
        type="warning"
        :title="alertText"
        variant="tonal"
      ></v-alert>
      <v-card-title>Reset Password</v-card-title>
      <v-text-field
        label="Old Password"
        v-model="oldPassword"
        type="password"
        :rules="[rules.required]"
        style="margin-bottom: 1vh"
      ></v-text-field>
      <v-text-field
        label="Re-enter Old Password"
        v-model="oldPasswordConfirm"
        type="password"
        :rules="[rules.required, rules.matchPasswords(oldPassword)]"
        style="margin-bottom: 1vh"
      ></v-text-field>
      <v-text-field
        label="New Password"
        v-model="newPassword"
        type="password"
        hint="8-15 characters, includes a capital letter and a special character like .,?!"
        persistent-hint
        :rules="[rules.required, rules.passwordComplexity]"
        style="margin-bottom: 1vh"
      ></v-text-field>
      <v-text-field
        label="Confirm New Password"
        v-model="newPasswordConfirm"
        type="password"
        :rules="[rules.required, rules.matchPasswords(newPassword)]"
      ></v-text-field>
      <v-card-actions>
        <v-btn :disabled="!canSubmit" color="primary" block @click="changePassword">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert'
export default {
  name: 'AddressAutocomplete',
  data() {
    return {
      searchQuery: '',
      addresses: [],
      addressDetails: {
        address: '',
        addressLine2: '',
        city: '',
        state: '',
        zipcode: ''
      },
      loading: false,
      location: {
        longitude: '',
        latitude: ''
      },
      email: '',
      role: '',
      edit: false,
      activePledges: [],
      activeRequests: [],
      pastRequests: [],
      pastPledges: [],
      dialog: false,
      oldPassword: '',
      oldPasswordConfirm: '',
      newPassword: '',
      newPasswordConfirm: '',
      alertText: 'Please check your input.',
      showAlert: false,
      rules: {
        required: (value) => !!value || 'This field is required.',
        matchPasswords: (reference) => (value) => value === reference || 'Passwords do not match.',
        passwordComplexity: (value) => {
          if (value.length < 8 || value.length > 15) {
            return 'Password must be 8-15 characters long.'
          }
          if (!/[A-Z]/.test(value)) {
            return 'Password must contain at least one capital letter.'
          }
          if (!/[.,?!]/.test(value)) {
            return 'Password must contain at least one special character (.,?!).'
          }
          return true
        }
      }
    }
  },
  computed: {
    canSubmit() {
      // Simply checks all rules by invoking them; useful if you want to show alert or disable submit based on general validity
      return (
        this.rules.required(this.oldPassword) === true &&
        this.rules.required(this.oldPasswordConfirm) === true &&
        this.rules.matchPasswords(this.oldPassword)(this.oldPasswordConfirm) === true &&
        this.rules.required(this.newPassword) === true &&
        this.rules.passwordComplexity(this.newPassword) === true &&
        this.rules.required(this.newPasswordConfirm) === true &&
        this.rules.matchPasswords(this.newPassword)(this.newPasswordConfirm) === true
      )
    }
  },
  created() {
    this.debouncedFetchAddresses = this.debounce(this.fetchAddresses, 250)
    this.fetchUserProfile()
  },

  methods: {
    editProfile() {
      let userData = user()
      let data = JSON.stringify({
        phone_number: this.phone_number,
        address: this.addressDetails.address,
        addressLine2: this.addressDetails.addressLine2,
        city: this.addressDetails.city,
        state: this.addressDetails.state,
        zipcode: this.addressDetails.zipcode,
        longitude: this.location.longitude,
        latitude: this.location.latitude
      })
      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/editProfile',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ` + userData.getToken
        },
        data: data
      }

      axios
        .request(config)
        .then(() => {
          window.scrollTo(0, 0)
          alertStore.showSuccess('Profile updated successfully')
        })
        .catch(() => {
          alertStore.showError('Failed to edit profile')
        })
    },

    /**
     * Fetches addresses based on the search query.
     */
    fetchAddresses() {
      if (this.searchQuery.length < 3) return
      this.loading = true
      const apiKey = 'b82eb2aaf0654b3f9517b92e38c28146'
      const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${this.searchQuery}&apiKey=${apiKey}`

      axios
        .get(url)
        .then((response) => {
          this.addresses = response.data.features
          this.loading = false
        })
        .catch((error) => console.error(error))
    },
    /**
     * Debounces a function to limit the number of times it is called.
     * @param {Function} func - The function to be debounced.
     * @param {number} wait - The debounce wait time in milliseconds.
     * @returns {Function} - The debounced function.
     */
    debounce(func, wait) {
      let timeout
      return function (...args) {
        const later = () => {
          clearTimeout(timeout)
          func.apply(this, args)
        }
        clearTimeout(timeout)
        timeout = setTimeout(later, wait)
      }
    },
    /**
     * Selects an address from the autocomplete suggestions.
     * @param {Object} address - The selected address object.
     */
    selectAddress(address) {
      this.searchQuery = address.properties.formatted
      this.addresses = [] // Clear suggestions
      if (address.properties.street != null && address.properties.housenumber != null) {
        this.addressDetails.address =
          address.properties.housenumber + ' ' + address.properties.street
      } else if (address.properties.name != null) {
        this.addressDetails.address = address.properties.name
      } else {
        this.addressDetails.address = 'FILL IN'
      }
      this.addressDetails.city = address.properties.city
      this.addressDetails.state = address.properties.state
      this.addressDetails.zipcode = address.properties.postcode
      this.location.longitude = address.geometry.coordinates[0]
      this.location.latitude = address.geometry.coordinates[1]
    },

    fetchUserProfile() {
      let userData = user()
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/users_bp/getProfile',
        headers: {
          Authorization: 'Bearer ' + userData.getToken
        }
      }
      axios
        .request(config)
        .then((response) => {
          this.username = response.data.username
          this.email = response.data.email
          this.role = response.data.role
          this.phone_number = response.data.phone_number
          this.addressDetails.address = response.data.address
          this.addressDetails.addressLine2 = response.data.addressLine2
          this.addressDetails.city = response.data.city
          this.addressDetails.state = response.data.state
          this.addressDetails.zipcode = response.data.zipcode
          if (response.data.role == 'Donor' || response.data.role == 'Admin') {
            this.fetchDonorPledges()
          }
          if (response.data.role == 'Recipient' || response.data.role == 'Admin') {
            this.fetchRecipientRequests()
          }
        })
        .catch(() => {
          alertStore.showError('Failed to fetch user profile')
        })
    },
    /**
     * Fetches the donor's pledges.
     */
    fetchDonorPledges() {
      let userData = user()
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/pledge/getUserPledges',
        headers: {
          Authorization: 'Bearer ' + userData.getToken
        }
      }

      axios
        .request(config)
        .then((response) => {
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].is_fulfilled == 0) {
              this.activePledges.push(response.data[i])
            } else {
              this.pastPledges.push(response.data[i])
            }
          }
        })
        .catch(() => {
          alertStore.showError('Failed to fetch user pledges')
        })
    },
    /**
     * Fetches the recipient's requests.
     */
    fetchRecipientRequests() {
      // let userData = user()
    },
    cancelpledge(pledge_id) {
      console.log(pledge_id)
    },
    /**
     * Clears the address details and location.
     */
    checkClear() {
      this.addressDetails = {
        address: '',
        addressLine2: '',
        city: '',
        state: '',
        zipcode: ''
      }
      this.location = {
        longitude: '',
        latitude: ''
      }
    },
    /**
     * Toggles the edit mode.
     */
    async toggleEdit() {
      if (this.edit) {
        await this.editProfile()
      }
      this.edit = !this.edit
    },

    /**
     * Redirects to the create item page.
     */
    createItem() {
      this.$router.push({ name: 'createItem' })
    },
    /**
     * Redirects to the event management page.
     */
    routeEvent() {
      this.$router.push({ name: 'eventManagement' })
    },
    routePledge() {
      this.$router.push({ name: 'pledge' })
    },
    changePassword() {
      let userData = user()
      if (this.canSubmit) {
        let data = JSON.stringify({
          old_password: this.oldPassword,
          new_password: this.newPassword
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/passwordreset',
          headers: {
            'Content-Type': 'application/json',
            Authorization:
              'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            alertStore.showSuccess('Password reset successfully')
            this.dialog = false
          })
          .catch((error) => {
            alertStore.showError(error.message)
            this.dialog = false
          })
      } else {
        this.alertText = 'Please ensure that the passwords match and meet the requirements.'
        this.showAlert = true
      }
    },
    resetForm() {
      this.oldPassword = ''
      this.oldPasswordConfirm = ''
      this.newPassword = ''
      this.newPasswordConfirm = ''
    },
    routePledgeMatcher() {
      this.$router.push({ name: 'match' })
    }
  }
}
</script>

<style scoped>
.v-card {
  padding: 2em;
  margin-bottom: 2em;
}

.v-container {
  max-width: 80%;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>

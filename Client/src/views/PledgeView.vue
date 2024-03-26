<template>
  <v-container style="max-width: 60vw">
    <v-form v-model="isFormValid">
      <v-autocomplete
        v-model="selectedItem"
        :items="item_names"
        label="Select an item to donate"
        :rules = "[rules.text_required]"
        clearable
      ></v-autocomplete>
      <v-text-field v-model="itemDescription" label="Description" readonly></v-text-field>

      <v-text-field v-model="itemCategory" label="Category" readonly></v-text-field>

      <v-text-field
        v-model="quantity"
        label="Quantity"
        type="text"
        :rules="[rules.required, rules.integer, rules.positiveNumber]"
      ></v-text-field>

      <v-btn :disabled="!isFormValid" color="primary" @click="submitDonation">Donate</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '@/stores/alert.js'
export default {
  data: () => ({
    selectedItem: null,
    quantity: '',
    item_names: [],
    items: [],
    itemDescription: '',
    itemCategory: '',
    isFormValid: false,
    rules: {
      text_required: value => !!value || 'This field is required',
      required: (value) => !!value || 'Required.',
      integer: (value) => Number.isInteger(Number(value)) || 'Must be a whole number.',
      positiveNumber: (value) => value > 0 || 'Must be a positive number.'
    }
  }),
  watch: {
    selectedItem(newValue) {
      this.onItemSelect(newValue)
    }
  },
  mounted() {
    this.fetchItems()
  },

  methods: {
    fetchItems() {
      let userData = user()
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/item/GetAllItems',
        headers: {
          Authorization: 'Bearer ' + userData.getToken
        }
      }

      axios
        .request(config)
        .then((response) => {
          this.items = response.data
          this.item_names = this.items.map((item) => item.name)
        })
        .catch(() => {
          alertStore.showError('Failed to fetch items')
        })
    },

    submitDonation() {
      // let userData = user()
      // let data = JSON.stringify({
      //   item_name: this.selectedItem,
      //   quantity: this.quantity
      // })
      // let config = {
      //   method: 'post',
      //   maxBodyLength: Infinity,
      //   url: 'http://127.0.0.1:5000/pledge/createPledge',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     Authorization: 'Bearer ' + userData.getToken
      //   },
      //   data: data
      // }

      // axios
      //   .request(config)
      //   .then(() => {
      //     this.$router.push({ name: 'profile' })
      //     alertStore.showSuccess('Thank you for your donation! You will get a notification when and where you need to ship your supplies!', 'Thanks!', true)
      //   })
      //   .catch(() => {
      //     alertStore.showError('Failed to submit donation')
      //   })
    },
    onItemSelect(itemName) {
      let item = this.items.find((item) => item.name === itemName)
      if (!item) {
        this.itemDescription = ''
        this.itemCategory = ''
        return
      } else {
        this.itemDescription = item.description || 'No description available'
        this.itemCategory = item.category || 'No category available'
        this.selectedItem = itemName
      }
    }
  }
}
</script>

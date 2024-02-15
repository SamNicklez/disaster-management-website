<template>
  <v-card variant="outlined" title="User Information">

  </v-card>
  <v-card variant="outlined" title="Address Information" style="margin-top: 10vh">
    <v-text-field v-if="edit" class="text-enter" :loading="loading" variant="solo" label="Search Address" clearable
      v-model="searchQuery" @keyup="debouncedFetchAddresses" append-inner-icon="mdi-magnify"
      @click:clear="checkClear"></v-text-field>
    <v-list v-if="addresses.length" dense>
      <v-list-item v-for="address in addresses" :key="address.properties.place_id" @click="selectAddress(address)">
        <v-list-item-content>
          <v-list-item-title>{{ address.properties.formatted }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-text-field class="address" readonly variant="outlined" label="Address" v-model="addressDetails.address" outlined
      dense></v-text-field>
    <v-text-field class="address" variant="outlined" label="Address Line 2" v-model="addressDetails.addressLine2" outlined
      dense></v-text-field>
    <v-text-field class="address" readonly variant="outlined" label="City" v-model="addressDetails.city" outlined
      dense></v-text-field>
    <v-text-field class="address" readonly variant="outlined" label="State" v-model="addressDetails.state" outlined
      dense></v-text-field>
    <v-text-field class="address" readonly variant="outlined" label="Zipcode" v-model="addressDetails.zipcode" outlined
      dense></v-text-field>
    <v-btn v-if="edit" style="background-color: #F06543;" @click="addressEdit">Save</v-btn>
    <v-btn v-if="!edit" style="background-color: #F06543;" @click="addressEdit">Edit</v-btn>
  </v-card>
</template>

<script>
import axios from 'axios';

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
        zipcode: '',
      },
      loading: false,
      location: {
        longitude: '',
        latitude: ''
      },
      username: 'temp',
      email: 'snicklaus@uiowa.edu',
      role: 'ADMIN',
      phone_number: '319-555-5555', 
      edit: false,
    };
  },
  created() {
    //Create FETCH call here for user data

    //If address data is not available, set edit to true
    //this.edit = true
    // Create a debounced version of fetchAddresses
    this.debouncedFetchAddresses = this.debounce(this.fetchAddresses, 500);
  },
  methods: {
    fetchAddresses() {
      if (this.searchQuery.length < 3) return;
      this.loading = true
      const apiKey = 'b82eb2aaf0654b3f9517b92e38c28146';
      const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${this.searchQuery}&apiKey=${apiKey}`;

      axios.get(url)
        .then(response => {
          this.addresses = response.data.features;
          this.loading = false;
        })
        .catch(error => console.error(error));
    },
    debounce(func, wait) {
      let timeout;
      return function (...args) {
        const later = () => {
          clearTimeout(timeout);
          func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },
    selectAddress(address) {
      console.log("Selected Address");
      this.searchQuery = address.properties.formatted;
      this.addresses = []; // Clear suggestions
      // Example of parsing, adjust based on the actual API response and needs
      if (address.properties.street != null && address.properties.housenumber != null) {
        this.addressDetails.address = address.properties.housenumber + " " + address.properties.street;
      }
      else if (address.properties.name != null) {
        this.addressDetails.address = address.properties.name;
      }
      else {
        this.addressDetails.address = "FILL IN";
      }
      this.addressDetails.city = address.properties.city;
      this.addressDetails.state = address.properties.state;
      this.addressDetails.zipcode = address.properties.postcode;
    },
    checkClear() {
      this.addressDetails = {
        address: '',
        addressLine2: '',
        city: '',
        state: '',
        zipcode: '',
      }
      this.location = {
        longitude: '',
        latitude: ''
      }
    },
    addressEdit() {
      this.edit = !this.edit

    }
  }
};
</script>

<style scoped>
.address {
  width: 50%;
  margin-left: 5vh;
}

.text-enter {
  margin-bottom: 1vh;
  width: 50%;
  margin-left: 5vh;

}

.v-card {
  padding: 3em;
  background-color: #E0DFD5;
}</style>
```

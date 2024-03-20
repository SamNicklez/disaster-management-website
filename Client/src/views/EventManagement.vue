<template>
  <v-dialog v-model="showDeleteDialog" persistent max-width="300px">
    <v-card>
      <v-card-title class="text-h5">Confirm Delete</v-card-title>
      <v-card-text>Are you sure you want to delete this event?</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="showDeleteDialog = false">Cancel</v-btn>
        <v-btn color="red darken-1" text @click="confirmDelete()">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-card style="margin: auto; max-width: 70vw">
    <v-card-title>
      Events
      <v-spacer></v-spacer>
      <v-btn color="primary" dark @click="showEventDialog = true">Add Event</v-btn>
    </v-card-title>

    <v-card-text>
      <v-text-field v-model="search" label="Search Events" outlined clearable></v-text-field>
      <v-data-table :headers="eventHeaders" :items="filteredEvents" :search="search">
        <template v-slot:[`item.action`]="{ item }">
          <v-btn text @click="confirmDeleteEvent(item)" class="mx-2">
            <v-icon small color="red">mdi-delete</v-icon>
          </v-btn>
        </template>
        <template v-slot:[`item.edit`]="{ item }">
          <v-btn text @click="editEvent(item)" class="mx-2">
            <v-icon small color="blue">mdi-pencil</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card-text>

    <v-dialog v-model="showEventDialog" max-width="800px">
      <v-card>
        <v-card-title>Event Management</v-card-title>
        <v-card-text>
          <v-text-field v-model="newEvent.event_name" label="Event Name" outlined></v-text-field>
          <v-textarea v-model="newEvent.description" label="Description" outlined></v-textarea>
          <v-text-field
            class="mb-3"
            :loading="loading"
            outlined
            clearable
            label="Location"
            v-model="searchQuery"
            @keyup="debouncedFetchAddresses"
            append-inner-icon="mdi-magnify"
            @click:clear="checkClear"
          ></v-text-field>
          <v-list v-if="addresses.length" dense class="mx-auto">
            <v-list-item
              v-for="address in addresses"
              :key="address.properties.place_id"
              @click="selectAddress(address)"
            >
              <v-list-item-title>{{ address.properties.formatted }}</v-list-item-title>
            </v-list-item>
          </v-list>
          <v-autocomplete
            v-model="chips"
            :items="items"
            label="Your favorite hobbies"
            prepend-icon="mdi-filter-variant"
            variant="solo"
            chips
            clearable
            multiple
          >
            <template v-slot:selection="{ attrs, item, select, selected }">
              <v-chip
                v-bind="attrs"
                :model-value="selected"
                closable
                @click="select"
                @click:close="remove(item)"
              >
                <strong>{{ item }}</strong
                >&nbsp;
                <span>(interest)</span>
              </v-chip>
            </template>
          </v-autocomplete>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="resetEventDialog()">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="addEditEvent()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'

export default {
  data: () => ({
    search: '',
    events: [],
    showEventDialog: false,
    showDeleteDialog: false,
    deleteEventIndex: null,
    loading: false,
    newEvent: {
      event_name: '',
      description: '',
      start_date: '',
      location: '',
      longitude: '',
      lattiude: '',
      item_names: []
    },
    eventHeaders: [
      { title: 'Event Name', key: 'event_name' },
      { title: 'Event Location', key: 'location' },
      { title: 'Event Date', key: 'start_date', sortable: true },
      { title: 'Event Description', key: 'description', sortable: false },
      { title: 'Actions', key: 'action', sortable: false },
      { title: 'Edit', key: 'edit', sortable: false }
    ],
    searchQuery: '',
    addresses: [],
    chips: ['Programming', 'Playing video games', 'Watching movies', 'Sleeping'],
    items: ['Streaming', 'Eating'],
  }),
  computed: {
    filteredEvents() {
      return this.search
        ? this.events.filter((event) =>
            Object.values(event).some((value) =>
              String(value).toLowerCase().includes(this.search.toLowerCase())
            )
          )
        : this.events
    }
  },
  created() {
    this.fetchEvents()
    this.debouncedFetchAddresses = this.debounce(this.fetchAddresses, 500)
  },
  methods: {
    fetchEvents() {
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/event/GetAllEvents'
      }

      axios
        .request(config)
        .then((response) => {
          for (let event of response.data.events) {
            event.start_date = this.formatDate(event.start_date)
            event.description = event.description || 'No Description'
            event.event_name = event.event_name || 'No Name'
          }
          this.events = response.data.events
        })
        .catch((error) => {
          console.log(error)
        })
    },
    confirmDeleteEvent(event) {
      this.deleteEventIndex = this.events.indexOf(event)
      this.showDeleteDialog = true
    },
    confirmDelete() {
      console.log('Deleting event')
    },
    addEditEvent() {
      console.log('Adding or editing event')
    },
    editEvent(event) {
      this.newEvent = { ...event }
      this.showEventDialog = true
    },
    resetEventDialog() {
      this.newEvent = { name: '', date: '', description: '' }
      this.showEventDialog = false
      this.editIndex = -1
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
        .catch((error) => alertStore.showError(error.message))
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
      this.newEvent.longitude = address.properties.lon
      this.newEvent.lattiude = address.properties.lat
      this.newEvent.location = address.properties.city + ', ' + address.properties.state
    },
    /**
     * Clears the address details and location.
     */
    checkClear() {
      ;(this.newEvent.location = ''), (this.newEvent.longitude = ''), (this.newEvent.lattiude = '')
      this.addresses = []
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const year = date.getFullYear()
      return `${month.toString().padStart(2, '0')}/${day.toString().padStart(2, '0')}/${year}`
    },
    remove (item) {
        this.chips.splice(this.chips.indexOf(item), 1)
    },
  }
}
</script>

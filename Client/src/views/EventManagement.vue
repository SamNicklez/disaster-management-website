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

    <v-dialog v-model="showEventDialog" max-width="600px">
      <v-card>
        <v-card-title>Add/Edit Event</v-card-title>
        <v-card-text>
          <v-text-field v-model="newEvent.name" label="Event Name" outlined></v-text-field>
          <v-text-field v-model="newEvent.date" label="Event Date" outlined></v-text-field>
          <v-textarea v-model="newEvent.description" label="Event Description" outlined></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showEventDialog = false">Cancel</v-btn>
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
    deleteType: null,
    deleteEventIndex: null,
    newEvent: {
      name: '',
      date: '',
      description: ''
    },
    eventHeaders: [
      { title: 'Event Name', key: 'name' },
      { title: 'Event Date', key: 'date', sortable: true },
      { title: 'Event Description', key: 'description', sortable: false },
      { title: 'Actions', key: 'action', sortable: false },
      { title: 'Edit', key: 'edit', sortable: false }
    ]
  }),
  computed: {
    filteredEvents() {
      return this.search
        ? this.events.filter((e) =>
            Object.values(e).some((v) => v.toLowerCase().includes(this.search.toLowerCase()))
          )
        : this.events
    }
  },
  created() {
    // Fetch events from the backend on component creation
    this.fetchEvents();
  },
  methods: {
    fetchEvents() {
      // Implement fetching of events from your backend here
    },
    confirmDeleteEvent(event) {
      this.deleteType = 'event'
      this.deleteEventIndex = this.events.indexOf(event)
      this.showDeleteDialog = true
    },
    confirmDelete() {
      
    },
    addEditEvent() {
      
    },
    editEvent(event) {
      this.newEvent = { ...event }
      this.showEventDialog = true
    },
    resetEventDialog() {
      this.newEvent = { name: '', date: '', description: '' }
      this.showEventDialog = false
      this.editIndex = -1
    }
  }
}
</script>

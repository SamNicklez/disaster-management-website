<template>
    <v-container>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="event.name"
          :rules="nameRules"
          label="Item Name"
          required
        ></v-text-field>
  
        <v-select
          v-model="event.category"
          :items="categories"
          :rules="[v => !!v || 'Item category is required']"
          label="Item Category"
          required
        ></v-select>
  
        <v-textarea
          v-model="event.description"
          :rules="[v => !!v || 'Item description is required']"
          label="Item Description"
          required
        ></v-textarea>
  
        <v-btn :disabled="!valid" color="success" @click="submitEvent">
          <v-icon left>mdi-check</v-icon>
          Submit
        </v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  export default {
    data: () => ({
      valid: true,
      event: {
        name: '',
        category: '',
        description: '',
      },
      nameRules: [
        v => !!v || 'Item name is required',
        v => (v && v.length <= 20) || 'Name must be less than 20 characters',
      ],
      categories: ['Music', 'Workshop', 'Festival', 'Meetup'], // Example categories
    }),
    methods: {
      submitEvent() {
        // Here you would usually send the event data to your backend or store it
        console.log('Submitting:', this.event);
        this.$refs.form.reset();
      },
    },
  };
  </script>  
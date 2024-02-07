import { defineStore } from 'pinia'

export const events = defineStore('events', {
    state: () => ({
      events: [
        {name: 'Earthquake', location: 'Iowa City, IA', date: '10/10/2021', time: '10:00 AM', description: 'A 7.0 magnitude earthquake has struck Iowa City, IA. The city is in need of food, water, and medical supplies.', route_id: 3},
        {name: 'Hurricane', location: 'New Orleans, LA', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 5},
        {name: 'Tornado', location: 'Oklahoma City, OK', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 6},
        {name: 'Flood', location: 'Houston, TX', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 7},
        {name: 'Wildfire', location: 'Los Angeles, CA', date: '10/10/2021', time: '10:00 AM', description: 'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.', route_id: 8}
      ]
    }),
    getters: {
      getEvents: (state) => state.events,
    },
    actions: {
      setEvents(event){
        this.events = event
      },
      getEvent(id){
        return this.events.find(event => event.route_id == id)
      },
    },
  })
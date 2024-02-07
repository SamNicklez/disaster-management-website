import { defineStore } from 'pinia'

export const useCounterStore = defineStore('events', {
    state: () => ({
      events: [{event_name: 'event1', date: '2021-10-10', time: '10:00', location: 'location1', description: 'description1'}],
    }),
    getters: {
      events: (state) => state.events,
    },
    actions: {
      setEvents(event){
        this.events = event
      },
    },
  })
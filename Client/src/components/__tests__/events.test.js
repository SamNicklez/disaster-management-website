import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { events } from '../../stores/events.js'

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('Events Store', () => {
  it('initializes with default state', () => {
    const eventsStore = events()
    expect(eventsStore.events.length).toBe(5)
  })

  it('getter: getEvents returns all events', () => {
    const eventsStore = events()
    const allEvents = eventsStore.getEvents
    expect(allEvents.length).toBe(5)
    expect(allEvents).toEqual(eventsStore.events)
  })

  it('action: setEvents updates the events state', () => {
    const eventsStore = events()
    const newEvents = [
      {
        name: 'Test Event',
        location: 'Test Location',
        date: '01/01/2022',
        time: '12:00 PM',
        description: 'Test Description',
        route_id: 9
      }
    ]
    eventsStore.setEvents(newEvents)
    expect(eventsStore.events).toEqual(newEvents)
  })

  it('action: getEvent returns a specific event by id', () => {
    const eventsStore = events()
    const event = eventsStore.getEvent(3)
    expect(event).toBeDefined()
    expect(event.name).toBe('Earthquake')
  })
})

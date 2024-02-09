import { describe, it, expect, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import EventsListComponent from '../EventsListComponent.vue'
import { events } from '../../stores/events.js'

const routes = [{ path: '/event/:id', name: 'event' }]

describe('EventsListComponent', () => {
  let router
  let eventsStore
  beforeEach(async () => {
    // Reset Pinia and Vue Router before each test
    setActivePinia(createPinia())
    router = createRouter({
      history: createWebHistory(),
      routes
    })

    // Directly set the state of the events store before each test
    eventsStore = events()
    eventsStore.setEvents([
      {
        name: 'Mock Event',
        location: 'Mock City',
        date: '01/01/2022',
        time: '12:00 PM',
        description: 'Mock Description',
        route_id: 1
      }
    ])
  })

  it('renders event data from the store', async () => {
    // Mount the component with the mock store instance
    const wrapper = mount(EventsListComponent, {
      global: {
        plugins: [router, eventsStore] // Pass the mock store instance
      }
    })

    // Flush promises to wait for component rendering
    await flushPromises()
    expect(wrapper.text()).toContain('Mock Event')
    expect(wrapper.text()).toContain('Mock City')
    expect(wrapper.text()).toContain('01/01/2022 at 12:00 PM')
    expect(wrapper.text()).toContain('Mock Description')
    expect(wrapper.findAll('[id="card"]').length).toBe(1)
  })

  it('navigates to event detail page on card click', async () => {
    // Get the mock store instance created in beforeEach
    const eventsStore = events()

    // Mount the component with the mock store instance
    const wrapper = mount(EventsListComponent, {
      global: {
        plugins: [router, eventsStore] // Pass the mock store instance
      }
    })
    await router.isReady()

    // Simulate clicking on event card
    await wrapper.find('[id="card"]').trigger('click')

    // Wait for all navigation and promises to resolve
    await flushPromises()

    // Perform assertions
    expect(router.currentRoute.value.name).toBe('event')
    expect(router.currentRoute.value.params.id).toBe('1')
  })
})

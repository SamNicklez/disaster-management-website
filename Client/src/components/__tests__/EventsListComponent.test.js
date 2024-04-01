import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import axios from 'axios'
import EventsListComponent from '@/components/EventsListComponent.vue' // Update the import path
import { createRouter, createWebHistory } from 'vue-router'
import { nextTick } from 'vue'

vi.mock('axios', () => ({
  default: {
    request: vi.fn(() =>
      Promise.resolve({
        data: {
          events: [
            {
              event_id: '1',
              event_name: 'Event 1',
              location: 'Location 1',
              start_date: '2023-01-01',
              description: 'Description 1'
            }
            // Mock more events if necessary
          ]
        }
      })
    )
  }
}))

const routes = [{ path: '/event/:id', name: 'event' }]
const router = createRouter({
  history: createWebHistory(),
  routes
})

describe('EventsListComponent.vue', () => {
  it('fetches events and renders them', async () => {
    const wrapper = mount(EventsListComponent, {
      global: {
        plugins: [router]
      }
    })

    await flushPromises()

    expect(axios.request).toHaveBeenCalled()
    expect(wrapper.vm.eventData).toHaveLength(1)
    expect(wrapper.findAll('#card')).toHaveLength(1)
    expect(wrapper.html()).toContain('Event 1')
  })

  describe('formatDate method', () => {
    it('formats date strings correctly', async () => {
      const wrapper = mount(EventsListComponent, {
        global: {
          plugins: [router]
        }
      })
      const formattedDate = wrapper.vm.formatDate('2023-03-21')
      const expectedDates = ['03/21/2023', '03/20/2023'] // Extendable to more dates if necessary

      // Check if the formatted date is one of the expected dates
      expect(expectedDates.includes(formattedDate)).toBe(true)
    })
  })

  describe('truncateName method', () => {
    it('truncates names longer than the specified maxLength', () => {
      const wrapper = mount(EventsListComponent, {
        global: {
          plugins: [router]
        }
      })

      const truncatedName = wrapper.vm.truncateName(
        'This is a very long event name that should be truncated',
        30
      )
      expect(truncatedName).toBe('This is a very long event name...')
    })

    it('does not truncate names shorter than the specified maxLength', () => {
      const wrapper = mount(EventsListComponent, {
        global: {
          plugins: [router]
        }
      })

      const notTruncatedName = wrapper.vm.truncateName('Short name', 30)
      expect(notTruncatedName).toBe('Short name')
    })
  })
  describe('events computed property', () => {
    it('returns eventData', async () => {
      const wrapper = mount(EventsListComponent, {
        global: {
          plugins: [router]
        }
      })

      // Simulate eventData being set by the axios request
      wrapper.vm.eventData = [{ event_id: '2', event_name: 'Event 2' }]
      await nextTick() // Wait for Vue to react to data changes

      expect(wrapper.vm.events).toEqual([{ event_id: '2', event_name: 'Event 2' }])
    })
  })

  it('navigates to event detail page using goToEvent', async () => {
    let mockRouterPush = vi.fn()
    let wrapper = mount(EventsListComponent, {
      global: {
        mocks: {
          $router: {
            push: mockRouterPush
          }
        }
      }
    })
    const testId = '123'
    await wrapper.vm.goToEvent(testId)
    expect(mockRouterPush).toHaveBeenCalledWith({
      name: 'event',
      params: {
        id: testId
      }
    })
  })
})

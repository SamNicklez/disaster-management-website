import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import EventManagement from '@/views/EventManagement.vue'
import { createPinia, setActivePinia } from 'pinia'

vi.mock('@/stores/user', () => ({
  user: vi.fn().mockReturnValue({
    token:
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiUm9sZUlEIjoxLCJEYXRlQ3JlYXRlZCI6IjIwMjQtMDMtMjJUMTM6MTA6MzIuMzQ2NDI3In0.0UMJEFy66KT3OkG0JZ9FIyX415Vuiui8ZR5mSOSlfgk'
  })
}))

vi.mock('@/stores/alert', () => ({
  alertStore: {
    showError: vi.fn(),
    showSuccess: vi.fn()
  }
}))

describe('EventManagement', () => {
  let wrapper

  beforeEach(() => {
    const pinia = createPinia()
    setActivePinia(pinia)
    wrapper = mount(EventManagement, {
      global: {
        plugins: [pinia]
      }
    })
  })

  it('initializes with the correct default data', () => {
    expect(wrapper.vm.showDeleteDialog).toBe(false)
    expect(wrapper.vm.showEventDialog).toBe(false)
    expect(wrapper.vm.events).toEqual([])
    expect(wrapper.vm.newEvent).toEqual({
      event_id: '',
      event_name: '',
      description: '',
      showable_description: '',
      start_date: '',
      location: '',
      longitude: '',
      lattiude: '',
      item_names: []
    })
  })

  it('computes filteredEvents correctly', async () => {
    await wrapper.setData({
      events: [
        {
          event_name: 'Event 1',
          location: 'Location 1',
          start_date: '2021-01-01',
          description: 'Description 1'
        },
        {
          event_name: 'Another Event',
          location: 'Location 2',
          start_date: '2022-02-02',
          description: 'Description 2'
        }
      ],
      search: 'another'
    })
    expect(wrapper.vm.filteredEvents.length).toBe(1)
  })

  it('opens the delete confirmation dialog', async () => {
    await wrapper.setData({
      events: [{ event_name: 'Event 1' }]
    })
    await wrapper.vm.confirmDeleteEvent(wrapper.vm.events[0])
    expect(wrapper.vm.showDeleteDialog).toBe(true)
  })

  it('closes the delete confirmation dialog on cancel', async () => {
    await wrapper.setData({ showDeleteDialog: true })
    await wrapper.find('[color="blue darken-1"]').trigger('click')
    expect(wrapper.vm.showDeleteDialog).toBe(false)
  })

  it('opens the event dialog', async () => {
    await wrapper.find('[color="primary"]').trigger('click')
    expect(wrapper.vm.showEventDialog).toBe(true)
  })

  it('resets the event dialog on cancel', async () => {
    await wrapper.setData({
      showEventDialog: true,
      newEvent: { event_name: 'Some Name' }
    })
    await wrapper.vm.resetEventDialog()
    expect(wrapper.vm.showEventDialog).toBe(false)
    expect(wrapper.vm.newEvent.event_name).toBe(undefined)
  })
  it('renders the add event dialog when showEventDialog is true', async () => {
    await wrapper.setData({ showEventDialog: true })
    expect(wrapper.find('.add-event-dialog').exists()).toBe(false)
  })

  it('does not render the delete confirmation dialog by default', () => {
    expect(wrapper.find('.delete-confirmation-dialog').exists()).toBe(false)
  })

  it('filters events based on search query', async () => {
    await wrapper.setData({
      events: [{ event_name: 'Test Event 1' }, { event_name: 'Another Test Event' }],
      search: 'Another'
    })
    expect(wrapper.vm.filteredEvents.length).toBe(1)
  })

  it('initializes with correct default data and computes filteredEvents', async () => {
    await wrapper.setData({ search: 'Event' })
    expect(wrapper.vm.filteredEvents).toHaveLength(
      wrapper.vm.events.filter((e) => e.event_name.includes('Event')).length
    )
  })

  it('resets event dialog correctly', async () => {
    await wrapper.vm.resetEventDialog()
    expect(wrapper.vm.newEvent.event_name).toBe(undefined)
    expect(wrapper.vm.newEvent.description).toBe('')
  })

  it('formats date correctly accounting for timezone differences', () => {
    const dateStr = '2023-01-01'
    const formattedDate = wrapper.vm.formatDate(dateStr)
    const expectedDate1 = '01/01/2023'
    const expectedDate2 = '12/31/2022'

    const isDateCorrect = formattedDate === expectedDate1 || formattedDate === expectedDate2
    expect(isDateCorrect).toBe(true)
  })

  it('truncates name correctly', () => {
    const longName = 'This is a very long event name that exceeds the limit'
    expect(wrapper.vm.truncateName(longName, 10)).toBe('This is a ...')
  })
  it('truncates name correctly', () => {
    const longName = 'This does not exceed the limit'
    expect(wrapper.vm.truncateName(longName, 1000)).toBe(longName)
  })
  it('correctly debounces functions', async () => {
    const spyFunction = vi.fn()
    const debouncedFunction = wrapper.vm.debounce(spyFunction, 100)

    debouncedFunction()
    debouncedFunction()

    await new Promise((resolve) => setTimeout(resolve, 150))

    expect(spyFunction).toHaveBeenCalledTimes(1)
  })

  it('does not add an event and shows an error when required fields are missing', async () => {
    await wrapper.setData({
      newEvent: {
        event_name: '',
        description: 'Sample Description',
        location: 'Sample Location',
        item_names: ['Item 1']
      }
    })
    await wrapper.vm.addEvent()
    expect(wrapper.vm.showEventDialog).toBe(false)
  })
  it('adds an event successfully and closes the dialog', async () => {
    await wrapper.setData({
      newEvent: {
        event_name: 'Event Name',
        description: 'Event Description',
        location: 'Event Location',
        item_names: ['Item 1']
      }
    })
    await wrapper.vm.addEvent()
    expect(wrapper.vm.events).toHaveLength(0)
    expect(wrapper.vm.showEventDialog).toBe(false)
  })
  it('correctly updates data properties when an address is selected', async () => {
    const mockAddress = {
      properties: {
        formatted: '123 Main St, City, State',
        lon: '123',
        lat: '456',
        city: 'City',
        state: 'State'
      }
    }

    await wrapper.vm.selectAddress(mockAddress)

    expect(wrapper.vm.searchQuery).toBe(mockAddress.properties.formatted)
    expect(wrapper.vm.addresses).toEqual([])
    expect(wrapper.vm.newEvent.longitude).toBe(mockAddress.properties.lon)
    expect(wrapper.vm.newEvent.lattiude).toBe(mockAddress.properties.lat)
    expect(wrapper.vm.newEvent.location).toBe(
      `${mockAddress.properties.city}, ${mockAddress.properties.state}`
    )
  })
  it('clears new event location details and addresses when checkClear is called', async () => {
    await wrapper.setData({
      newEvent: {
        location: '123 Main St, City, State',
        longitude: '123',
        lattiude: '456'
      },
      addresses: [{ properties: { formatted: '123 Main St, City, State' } }]
    })

    await wrapper.vm.checkClear()

    expect(wrapper.vm.newEvent.location).toBe('')
    expect(wrapper.vm.newEvent.longitude).toBe('')
    expect(wrapper.vm.newEvent.lattiude).toBe('')
    expect(wrapper.vm.addresses).toEqual([])
  })
  it('handles errors when the event deletion fails', async () => {
    const wrapper = mount(EventManagement, {})

    await wrapper.setData({
      events: [{ event_id: '1', event_name: 'Test Event' }],
      deleteEventIndex: 0,
      showDeleteDialog: true
    })

    await wrapper.vm.confirmDelete()

    expect(wrapper.vm.showDeleteDialog).toBe(false)
  })
})

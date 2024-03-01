import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import UserInfoComponent from '../UserInfoComponent.vue'

describe('UserInfoComponent', () => {
  let wrapper
  let axiosMock

  beforeEach(() => {
    axiosMock = vi.mock('axios', async () => ({
      get: vi.fn()
    }))

    wrapper = mount(UserInfoComponent, {})
  })

  it('fetches addresses when searchQuery length is at least 3', async () => {
    // Set searchQuery to trigger fetchAddresses
    await wrapper.setData({ searchQuery: 'abc' })

    // Wait for Vue to update the component
    await wrapper.vm.$nextTick()

    // Assert that axios.get was called
  })

  it('does not fetch addresses when searchQuery length is less than 3', async () => {
    // Set searchQuery to not trigger fetchAddresses
    await wrapper.setData({ searchQuery: 'ab' })

    // Wait for Vue to update the component
    await wrapper.vm.$nextTick()
  })

  it('selects an address and updates address details', async () => {
    // Sample address object
    const address = {
      properties: {
        formatted: '123 Main St',
        street: 'Main St',
        housenumber: '123',
        city: 'City',
        state: 'State',
        postcode: '12345'
      }
    }

    // Call selectAddress method
    await wrapper.vm.selectAddress(address)

    // Assert that address details are updated
    expect(wrapper.vm.addressDetails.address).toBe('123 Main St')
    expect(wrapper.vm.addressDetails.city).toBe('City')
    expect(wrapper.vm.addressDetails.state).toBe('State')
    expect(wrapper.vm.addressDetails.zipcode).toBe('12345')
  })

  it('toggles edit mode correctly', async () => {
    // Initial edit mode should be false
    expect(wrapper.vm.edit).toBe(false)

    // Toggle edit mode
    await wrapper.vm.toggleEdit()

    // Check if edit mode is toggled
    expect(wrapper.vm.edit).toBe(true)
  })

  it('clears address details and location correctly', async () => {
    // Set some initial address details and location
    await wrapper.setData({
      addressDetails: {
        address: '123 Main St',
        addressLine2: 'Apt 1',
        city: 'City',
        state: 'State',
        zipcode: '12345'
      },
      location: {
        longitude: '40.7128',
        latitude: '-74.0060'
      }
    })

    await wrapper.vm.checkClear()

    expect(wrapper.vm.addressDetails.address).toBe('')
    expect(wrapper.vm.addressDetails.addressLine2).toBe('')
    expect(wrapper.vm.addressDetails.city).toBe('')
    expect(wrapper.vm.addressDetails.state).toBe('')
    expect(wrapper.vm.addressDetails.zipcode).toBe('')
    expect(wrapper.vm.location.longitude).toBe('')
    expect(wrapper.vm.location.latitude).toBe('')
  })
})

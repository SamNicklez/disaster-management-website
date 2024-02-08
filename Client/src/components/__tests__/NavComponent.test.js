import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import NavComponent from '../NavComponent.vue'

describe('NavComponent', () => {
  let wrapper
  let mockRouterPush

  beforeEach(() => {
    mockRouterPush = vi.fn()
    wrapper = mount(NavComponent, {
      global: {
        mocks: {
          $router: {
            push: mockRouterPush
          }
        }
      }
    })
  })

  it('performs a search and navigates', async () => {
    await wrapper.setData({ searchQuery: 'disaster' })
    await wrapper.vm.performSearch()
    expect(mockRouterPush).toHaveBeenCalledWith(`/search/disaster`)
  })

  it('opens the profile page', async () => {
    wrapper.vm.openProfile()
    expect(mockRouterPush).toHaveBeenCalledWith('/profile')
  })

  it('opens the login page', async () => {
    wrapper.vm.openLogin()
    expect(mockRouterPush).toHaveBeenCalledWith('/login')
  })

  // Assuming populateNotifications would fetch and set notifications
  // This test might need to be adjusted based on the actual implementation of populateNotifications
  it('populates notifications', async () => {
    // Placeholder for testing populateNotifications
    // Depending on its implementation, you might need to mock API calls or other asynchronous operations
    console.log('Test for populateNotifications needs to be implemented based on its logic')
  })

  it('closes a notification', async () => {
    const initialLength = wrapper.vm.notifications.length
    wrapper.vm.closeNoti(0) // Close the first notification
    expect(wrapper.vm.notifications.length).toBe(initialLength - 1)
  })
})

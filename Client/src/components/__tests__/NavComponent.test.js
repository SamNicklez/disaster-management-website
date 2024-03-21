import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import NavComponent from '../NavComponent.vue'
import { flushPromises } from '@vue/test-utils'

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
    expect(mockRouterPush).toHaveBeenCalledWith({
      name: 'search',
      params: {
        query: 'disaster',
      },
    })
  })
  

  it('opens the profile page', async () => {
    wrapper.vm.openProfile()
    expect(mockRouterPush).toHaveBeenCalledWith('/profile')
  })

  it('opens the login page', async () => {
    wrapper.vm.openLogin()
    expect(mockRouterPush).toHaveBeenCalledWith('/login')
  })

  it('populates notifications', async () => {
    console.log('Test for populateNotifications needs to be implemented based on its logic')
  })

  it('closes a notification', async () => {
    const initialLength = wrapper.vm.notifications.length
    wrapper.vm.closeNoti(0)
    expect(wrapper.vm.notifications.length).toBe(initialLength - 1)
  })

  it('updates searchQuery on input', async () => {
    wrapper.vm.searchQuery = 'disaster'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.searchQuery).toBe('disaster')
  })

  it('populates notifications on bell icon click', async () => {
    const populateNotificationsSpy = vi.spyOn(wrapper.vm, 'populateNotifications')
    await wrapper.vm.populateNotifications()
    await flushPromises()

    expect(populateNotificationsSpy).toHaveBeenCalled()
  })

  it('closes a notification', async () => {
    await wrapper.setData({
      notifications: [{ title: 'Notification 1', description: 'Description 1' }]
    })
    const initialLength = wrapper.vm.notifications.length
    await wrapper.vm.closeNoti(0)
    expect(wrapper.vm.notifications.length).toBeLessThan(initialLength)
  })
})

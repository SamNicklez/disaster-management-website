import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import LogoutView from '@/views/LogoutView.vue'

describe('LogoutView', () => {
  let wrapper
  let routerMock

  beforeEach(() => {
    routerMock = {
      push: vi.fn()
    }

    wrapper = mount(LogoutView, {
      global: {
        mocks: {
          $router: routerMock
        }
      }
    })
  })

  it('redirects to home page when "Return to Home" link is clicked', async () => {
    await wrapper.find('a').trigger('click')
    expect(routerMock.push).toHaveBeenCalledWith({ name: 'home' })
  })
  it('logs out the user when "Log Out" button is clicked', async () => {
    vi.mock('@/stores/user', () => ({
      user: () => ({
        clearUser: vi.fn()
      })
    }))
    await wrapper.find('v-btn').trigger('click')
    expect(routerMock.push).toHaveBeenCalledWith({ name: 'login' })
  })
})

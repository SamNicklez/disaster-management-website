import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest'
import { mount } from '@vue/test-utils'
import LoginComponent from '@/components/LoginComponent.vue'
vi.mock('axios', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    request: vi.fn(() =>
      Promise.reject({
        response: {
          status: 401,
          data: {
            message: 'Unauthorized'
          }
        }
      })
    )
  }
})

vi.mock('@/stores/user', () => ({
  user: () => ({
    getLoginAttempts: vi.fn().mockReturnValue(0),
    setLoginAttempt: vi.fn(),
    resetLoginAttempts: vi.fn(),
    setLogin: vi.fn()
  })
}))


vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

// Example test
describe('LoginComponent', () => {
  it('renders properly', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        stubs: {
          VerifyComponentVue: true
        }
      }
    })
    expect(wrapper.exists()).toBeTruthy()
    expect(wrapper.find('.login-card').exists()).toBe(true)
  })

  it('calls login method and handles success', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        mocks: {
          $router: {
            push: vi.fn()
          }
        },
        stubs: {
          VerifyComponentVue: true
        }
      }
    })

    await wrapper.setData({ username: 'test@example.com', password: 'password' })
    await wrapper.find('#loginButton').trigger('click')
  })

  it('calculates the minutes between dates correctly', async () => {
    const wrapper = mount(LoginComponent)
    const inputDate = new Date()
    const result = wrapper.vm.minutesBetweenDates(inputDate.toISOString())
    expect(result).toMatch(/^\d+ minutes\.$/)
  })

  it('returns the difference in milliseconds correctly for minutesBetweenDatesVal', async () => {
    const wrapper = mount(LoginComponent)
    const inputDate = new Date()
    const result = wrapper.vm.minutesBetweenDatesVal(inputDate.toISOString())
    expect(result).toBeGreaterThanOrEqual(590000)
    expect(result).toBeLessThanOrEqual(610000)
  })
})

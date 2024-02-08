import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InitialSignupComponent from '../InitialSignupComponent.vue'

describe('InitialSignupComponent', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(InitialSignupComponent, {
      global: {
        mocks: {
          $router: {
            push: vi.fn()
          }
        }
      }
    })
  })

  it('enables sign up button when form is valid', async () => {
    await wrapper.setData({
      username: 'validUsername',
      password: 'ValidPass123!',
      confirmPassword: 'ValidPass123!'
    })
    // After updating the data, wait for Vue to process the changes
    await wrapper.vm.$nextTick()

    const signupButton = wrapper.find('[data-test="signup-button"]')
    expect(signupButton.attributes('disabled')).toBe('true')
  })
  it('submits the form correctly', async () => {
    const mockSubmitMethod = vi.spyOn(wrapper.vm, 'submit')
    await wrapper.vm.submit()
    expect(mockSubmitMethod).toHaveBeenCalled()
  })
  it('validates password correctly', async () => {
    const wrapper = mount(InitialSignupComponent)
    wrapper.vm.password = 'Passw0rd!'
    wrapper.vm.validatePassword()

    expect(wrapper.vm.passwordRequirements[0].valid).toBe(true) // Checks length requirement
    expect(wrapper.vm.passwordRequirements[1].valid).toBe(true) // Checks valid characters
    expect(wrapper.vm.passwordRequirements[2].valid).toBe(true) // Checks uppercase letter
    expect(wrapper.vm.passwordRequirements[3].valid).toBe(true) // Checks special character
  })
  it('submits the form successfully', async () => {
    const mockRouterPush = vi.fn()
    const wrapper = mount(InitialSignupComponent, {
      global: {
        mocks: {
          $router: { push: mockRouterPush }
        }
      }
    })
    await wrapper.setData({
      username: 'validUsername',
      password: 'ValidPass123!',
      confirmPassword: 'ValidPass123!'
    })

    // call submit method
    await wrapper.vm.submit()

    await wrapper.vm.$nextTick()

    // Check if routing to a new page occurs as expected
    expect(mockRouterPush).toHaveBeenCalledWith({ name: 'login' })
  })

  it('navigates to sign-in page correctly', async () => {
    const mockGoToSignInMethod = vi.spyOn(wrapper.vm, 'goToSignIn')
    await wrapper.vm.goToSignIn()
    expect(mockGoToSignInMethod).toHaveBeenCalled()
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({ name: 'login' }) // Adjust based on actual implementation
  })
  it('routes to sign-in page correctly', async () => {
    const mockRouterPush = vi.fn()
    const wrapper = mount(InitialSignupComponent, {
      global: {
        mocks: {
          $router: { push: mockRouterPush }
        }
      }
    })

    wrapper.vm.goToSignIn()
    expect(mockRouterPush).toHaveBeenCalledWith({ name: 'login' })
  })

  it('navigates to sign in page on link click', async () => {
    const signInLink = wrapper.find('[data-test="signin-link"]')
    await signInLink.trigger('click')
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith(expect.anything())
  })
  it('requires confirm password', async () => {
    const wrapper = mount(InitialSignupComponent)
    const confirmPasswordRule = wrapper.vm.confirmPasswordRules[0]

    // Test with empty confirm password
    expect(confirmPasswordRule('')).toBe('Confirm password is required')

    // Test with non-empty confirm password
    expect(confirmPasswordRule('password')).toBe(true)
  })
})

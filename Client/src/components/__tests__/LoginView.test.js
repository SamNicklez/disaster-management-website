import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import LoginView from '@/views/LoginView.vue'
import LoginComponent from '@/components/LoginComponent.vue'

describe('LoginView', () => {
  it('renders LoginComponent without Pinia error', () => {
    // Create a new Pinia store
    const pinia = createPinia()

    // Mount the component with Pinia
    const wrapper = mount(LoginView, {
      global: {
        plugins: [pinia]
      }
    })

    const loginComponent = wrapper.findComponent(LoginComponent)
    expect(loginComponent.exists()).toBe(true)
  })
})

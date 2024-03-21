import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import EventView from '../../views/EventView.vue'

const routes = [
  { path: '/event/:id', component: EventView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

describe('EventView.vue', () => {
  it('sets event_id from route params on creation', async () => {
    router.push('/event/123')
    await router.isReady()

    const wrapper = mount(EventView, {
      global: {
        plugins: [router]
      }
    })

    // Check if event_id is set correctly
    expect(wrapper.vm.event_id).toBe('123')
  })
})

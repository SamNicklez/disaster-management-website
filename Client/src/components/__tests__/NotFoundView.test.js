import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import NotFoundView from '@/views/NotFoundView.vue';

// Setup global mocks
const globalMocks = {
  global: {
    mocks: {
      $router: {
        push: vi.fn()
      }
    }
  }
};

describe('NotFoundView', () => {
  it('renders correctly', () => {
    const wrapper = mount(NotFoundView, globalMocks);
    // Check for the presence of elements
    expect(wrapper.find('h1').text()).toContain('Ope! Page not found.');
    expect(wrapper.find('p').text()).toContain("The page you are looking for doesn't exist or has been moved.");
    expect(wrapper.find('v-btn').exists()).toBe(true);
    expect(wrapper.find('v-img').attributes('src')).toBe("https://cdn-icons-png.flaticon.com/512/2748/2748558.png");
  });

  it('navigates home when button is clicked', async () => {
    const wrapper = mount(NotFoundView, globalMocks);
    await wrapper.find('v-btn').trigger('click');
    expect(globalMocks.global.mocks.$router.push).toHaveBeenCalledWith('/');
  });
});

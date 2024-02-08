import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import AppView from '../../App.vue';
import Navbar from '@/components/NavComponent.vue';

const globalStubs = {
  Navbar: true
};

describe('AppView', () => {
  it('renders properly', async () => {
    const wrapper = mount(AppView, {
      global: {
        stubs: globalStubs,
      }
    });

    expect(wrapper.findComponent(Navbar).exists()).toBe(true);
    expect(wrapper.find('v-main').exists()).toBe(true);
    expect(wrapper.find('router-view').exists()).toBe(true);

  });
});

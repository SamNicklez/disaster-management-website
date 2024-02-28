import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import DonationView from '@/views/DonationView.vue';

const routes = [
  { path: '/', component: { template: 'Home page' } },
  { path: '/login', component: { template: 'Login page' } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe('DonationView.vue', () => {
  it('renders event page text', async () => {
    const wrapper = mount(DonationView, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.text()).toContain('Event page');
  });

  it('has a button to navigate to home', async () => {
    const wrapper = mount(DonationView, {
      global: {
        plugins: [router],
      },
    });

    await router.isReady();

    const homeButton = wrapper.find('v-btn[to="/"]');
    expect(homeButton.exists()).toBe(true);
  });

  it('has a button to navigate to login', async () => {
    const wrapper = mount(DonationView, {
      global: {
        plugins: [router],
      },
    });

    await router.isReady();

    const loginButton = wrapper.find('v-btn[to="/login"]');
    expect(loginButton.exists()).toBe(true);
  });
});

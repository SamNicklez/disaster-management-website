import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import LoginComponent from '@/components/LoginComponent.vue';
import { createPinia, setActivePinia } from 'pinia';
import { user } from '../../stores/user.js';

describe('LoginComponent Tests', () => {
  let mockRouter;
  let userStore;
  beforeEach(() => {
    // Reset Pinia for each test
    setActivePinia(createPinia());
    // Initialize the user store
    userStore = user();
    // Optionally reset the user store's state if required
    userStore.$reset = vi.fn(() => {
      userStore.username = '';
      userStore.token = '';
      userStore.refreshDate = null;
      userStore.loginAttempts = 0;
      userStore.lastLoginAttempt = null;
    });
    userStore.$reset();

    // Mock Vue Router
    mockRouter = {
      push: vi.fn(),
    };
  });

  it('navigates to signup page on goToSignUp', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        mocks: {
          $router: mockRouter,
        },
        plugins: [createPinia()],
      },
    });

    wrapper.vm.goToSignUp();
    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'signup' });
  });

  it('displays alert when username and password are empty', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        mocks: {
          $router: mockRouter,
        },
        plugins: [createPinia()],
      },
    });

    wrapper.vm.login();
    expect(wrapper.vm.alert).toBe(true);
    expect(wrapper.vm.alertText).toBe('Please enter a username and password');
  });

//   it('displays custom alert after exceeding login attempts', async () => {
//     const wrapper = mount(LoginComponent, {
//       global: {
//         mocks: {
//           $router: mockRouter,
//         },
//         plugins: [userStore],
//       },
//     });

//     wrapper.vm.login();
//     expect(wrapper.vm.alert).toBe(true);
//     // Assert based on your component's logic for handling exceeded login attempts
//     expect(wrapper.vm.alertText).toContain('You have exceeded the maximum number of login attempts');
//   });
});

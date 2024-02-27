import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ParentComponent from '@/views/SignupView.vue';
import InitialSignupComponent from '@/components/InitialSignupComponent.vue';

describe('ParentComponent', () => {
  it('renders InitialSignupComponent', () => {
    const wrapper = mount(ParentComponent, {
    });

    const signupComponent = wrapper.findComponent(InitialSignupComponent);
    expect(signupComponent.exists()).toBe(true);
  });
});
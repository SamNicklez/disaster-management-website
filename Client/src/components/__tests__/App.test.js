import { mount } from '@vue/test-utils'
import AppView from '../../App.vue'
import { describe, it, expect, vi } from 'vitest';
import { loadingBar } from '../../stores/loading.js';
import { alertStore } from '../../stores/alert.js';

// Mock the external modules
vi.mock('../../stores/loading.js', () => ({
  loadingBar: {
    loading: false
  }
}));

vi.mock('../../stores/alert.js', () => ({
  alertStore: {
    text: '',
    display: false,
    type: '',
    title: ''
  }
}));

describe('AppView', () => {
  it('shows the loading bar when loading is true', async () => {
    // Mock loading state
    loadingBar.loading = true;
    const wrapper = mount(AppView);
    expect(wrapper.find('v-progress-linear').exists()).toBe(true);
    expect(wrapper.find('v-progress-linear').attributes('active')).toBe('true');
  });

  it('shows an alert when isAlert is true', async () => {
    // Mock alert state
    alertStore.display = true;
    alertStore.text = 'Test Alert';
    alertStore.title = 'Alert Title';
    alertStore.type = 'error';
    
    const wrapper = mount(AppView);
    
    expect(wrapper.find('v-alert').exists()).toBe(true);
    expect(wrapper.find('v-alert').attributes('text')).toBe('Test Alert');
    expect(wrapper.find('v-alert').attributes('type')).toBe('error');
    expect(wrapper.find('v-alert').attributes('title')).toBe('Alert Title');
  });

  it('hides the alert when isAlert is false', async () => {
    alertStore.display = false;
    const wrapper = mount(AppView);
    expect(wrapper.find('v-alert').exists()).toBe(false);
  });
});

// HomeView.test.js
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import HomeView from '../../views/HomeView.vue'; // Update the path according to your file structure

describe('HomeView.vue', () => {
  it('renders the message "AYO!" within the <main> tag', () => {
    const wrapper = mount(HomeView);
    expect(wrapper.find('main').text()).toContain('AYO!');
  });
});

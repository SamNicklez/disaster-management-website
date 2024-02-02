// App.test.js
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import App from '../../App.vue'; // Update the path according to your file structure

describe('App.vue', () => {
  it('renders a header with the text "Hello!"', () => {
    const wrapper = mount(App);
    expect(wrapper.find('header').text()).toContain('Hello!');
  });
});

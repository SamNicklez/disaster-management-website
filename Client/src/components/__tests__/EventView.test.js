import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import EventView from '@/views/EventView.vue';

describe('EventView.vue', () => {
  let wrapper;
  const mockRoute = {
    params: {
      event: {
        name: 'Sample Event',
        location: 'Sample Location',
        date: '2024-02-28',
        time: '10:00',
        description: 'This is a sample event description.',
      },
    },
  };
  const mockRouter = {
    push: vi.fn(),
  };

  beforeEach(() => {
    wrapper = mount(EventView, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
    });
  });

  it('displays event details correctly', () => {
    expect(wrapper.text()).toContain('Sample Event');
    expect(wrapper.text()).toContain('Sample Location');
    expect(wrapper.text()).toContain('2024-02-28');
    expect(wrapper.text()).toContain('10:00');
    expect(wrapper.text()).toContain('This is a sample event description.');
  });

  it('loads event details on creation', () => {
    expect(wrapper.vm.event).toEqual(mockRoute.params.event);
  });
});

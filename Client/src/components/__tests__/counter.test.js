// index.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useCounterStore } from '../../stores/counter';

describe('counter store', () => {
  beforeEach(() => {
    // Creates a fresh Pinia store before each test
    setActivePinia(createPinia());
  });

  it('initializes with a count of 0', () => {
    const counterStore = useCounterStore();
    expect(counterStore.count).toBe(0);
  });

  it('increments the count by 1', () => {
    const counterStore = useCounterStore();
    counterStore.increment();
    expect(counterStore.count).toBe(1);
  });

  it('doubles the count correctly', () => {
    const counterStore = useCounterStore();
    counterStore.increment(); // count is now 1
    counterStore.increment(); // count is now 2
    expect(counterStore.doubleCount).toBe(4);
  });
});

// addNumbers.test.js
import { describe, it, expect } from 'vitest';
import addNumbers from '../addNumbers.js';

describe('addNumbers', () => {
  it('correctly adds two numbers', () => {
    const result = addNumbers(2, 3);
    expect(result).toBe(5);
  });
});

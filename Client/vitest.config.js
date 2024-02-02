import { fileURLToPath } from 'node:url';
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config';
import viteConfig from './vite.config';

export default mergeConfig(viteConfig, defineConfig({
  test: {
    // Define test environment, root, and exclusions
    environment: 'jsdom',
    root: fileURLToPath(new URL('./', import.meta.url)),
    exclude: [...configDefaults.exclude, 'e2e/*'],

    // Configure coverage separately
    coverage: {
      provider: 'istanbul',
      reporters: ['text','lcov'],
      exclude: [
        'src/main.js',
        '**/router/**',
        '**/*.eslintrc.cjs',
        '**/node_modules/**',
        '**/tests/**',
        '**/*.test.js',
        '**/*.spec.js'
      ],
    },
    reporters: ['default', 'vitest-sonar-reporter'],
    outputFile: 'test-results.xml',
  }
}));

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
      provider: 'v8',
      reporters: ['text', 'lcov'], // Ensure coverage reporters are correctly specified
    },

    // Specify test reporters (for test results) correctly to avoid conflicts
    reporters: ['default', 'vitest-sonar-reporter'], // Include 'default' or any other reporters as needed
    outputFile: 'test-results.xml', // This likely applies to your test reporter
  }
}));

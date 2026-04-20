import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.js'],
    globals: true
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react')) return 'vendor';
            if (id.includes('firebase')) return 'firebase';
            if (id.includes('dompurify')) return 'utils';
          }
        }
      }
    }
  },
  esbuild: {
    drop: ['console', 'debugger'],
  }
})

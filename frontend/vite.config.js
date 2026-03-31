import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/static/frontend/',
  build: {
    outDir: '../static/frontend',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'js/app.js',
        chunkFileNames: 'js/[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'css/app.css';
          }
          return 'assets/[name][extname]';
        }
      }
    }
  },
  server: {
    proxy: {
      '/download_options': 'http://localhost:8000',
      '/static/downloader': 'http://localhost:8000',
    }
  }
})

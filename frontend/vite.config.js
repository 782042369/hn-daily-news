import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/hn-daily-news/', // GitHub Pages子路径
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})

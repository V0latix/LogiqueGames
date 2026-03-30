import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  build: {
    outDir: '../docs',
    // Keep repo docs (markdown, prompts, etc.) alongside the static site output.
    // Otherwise Vite wipes the whole ../docs directory before each build.
    emptyOutDir: false,
  },
});

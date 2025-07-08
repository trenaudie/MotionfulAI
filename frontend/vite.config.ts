// animation_snippets/vite.config.ts
import {defineConfig} from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';

export default defineConfig({
  server: {
    fs: {
      // let it load external files when using local motion-canvas/ui
      strict: false,
    },
  },
  plugins: [motionCanvas()],
});
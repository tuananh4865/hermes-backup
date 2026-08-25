import { Config } from '@remotion/cli/config';

// Edit durationInFrames, width, height per project.
export default {
  Config: {
    fps: 24,
    durationInFrames: 24 * 30, // 30s
    width: 1080,
    height: 1080,
    outDir: 'out',
  } satisfies Config,
};
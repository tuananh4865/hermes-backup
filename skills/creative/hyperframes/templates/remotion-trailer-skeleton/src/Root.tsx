import React from 'react';
import { Composition } from 'remotion';
import { Trailer } from './Trailer';

export const FPS = 24;
export const DURATION_IN_FRAMES = FPS * 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Trailer"
        component={Trailer}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={1080}
        height={1080}
      />
    </>
  );
};
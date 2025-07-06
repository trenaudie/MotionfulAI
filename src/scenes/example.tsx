// import {Circle, makeScene2D} from '@motion-canvas/2d';
// import {createRef} from '@motion-canvas/core';

// export default makeScene2D(function* (view) {
//   // Create your animations here

//   const circle = createRef<Circle>();

//   view.add(<Circle ref={circle} size={320} fill={'lightseagreen'} />);

//   yield* circle().scale(2, 2).to(1, 2);
// });

// scenes/example.tsx

import { Circle, makeScene2D } from '@motion-canvas/2d';
import { createRef } from '@motion-canvas/core';

// 1. List out each yield‑duration (in seconds)
const animationDurations: number[] = [
  /* circle.scale(2,2) → instantaneous, so duration = 0, */
  2 /* from .to(1, 2) */,
  // If you add more yields like yield* something.to(x, y), push y here
];

// 2. Compute total duration by summing the array
export const SCENE_DURATION = animationDurations.reduce((sum, d) => sum + d, 0);

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(<Circle ref={circle} size={320} fill={'lightseagreen'} />);

  // 3. Perform your animated yield
  yield* circle().scale(2, 2).to(1, 2);

  // If you later do:
  // animationDurations.push(1.5);
  // yield* circle().position([100, 0], 1.5);
});


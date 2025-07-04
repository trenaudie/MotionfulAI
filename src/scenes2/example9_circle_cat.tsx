import {Circle, makeScene2D, Path, Rect} from '@motion-canvas/2d';
import {createRef} from '@motion-canvas/core';
import {Node} from '@motion-canvas/2d';
import {logMethods} from './utils';
import {all, waitFor} from '@motion-canvas/core';
import {Layout} from '@motion-canvas/2d';
export default makeScene2D(function* (view) {
  view.fill('#000000');
  const path = createRef<Path>();
const circle = createRef<Circle>();
  const arrow = createRef<Path>();
  const pathBox = createRef<Rect>();
  const circleBox = createRef<Rect>();
  const arrowBox = createRef<Rect>();
  view.add(
    <Layout justifyContent={'center'} alignItems={'center'} gap = {50} layout direction={'row'}>
    <Layout>
      <Rect
        ref={pathBox}
        width={200}
        height={200}
        stroke={'#444'}
        lineWidth={1}
        opacity={0}
      />
      {/* <Path
        ref={path}
        lineWidth={4}
        stroke={'#e13238'}
        data="M 151.34904,307.20455 L 264.34904,307.20455 C 264.34904,291.14096 263.2021,287.95455 236.59904,287.95455 C 240.84904,275.20455 258.12424,244.35808 267.72404,244.35808 C 276.21707,244.35808 286.34904,244.82592 286.34904,264.20455 C 286.34904,286.20455 323.37171,321.67547 332.34904,307.20455 C 345.72769,285.63897 309.34904,292.21514 309.34904,240.20455 C 309.34904,169.05135 350.87417,179.18071 350.87417,139.20455 C 350.87417,119.20455 345.34904,116.50374 345.34904,102.20455 C 345.34904,83.30695 361.99717,84.403577 358.75805,68.734879 C 356.52061,57.911656 354.76962,49.23199 353.46516,36.143889 C 352.53959,26.857305 352.24452,16.959398 342.59855,17.357382 C 331.26505,17.824992 326.96549,37.77419 309.34904,39.204549 C 291.76851,40.631991 276.77834,24.238028 269.97404,26.579549 C 263.22709,28.901334 265.34904,47.204549 269.34904,60.204549 C 275.63588,80.636771 289.34904,107.20455 264.34904,111.20455 C 239.34904,115.20455 196.34904,119.20455 165.34904,160.20455 C 134.34904,201.20455 135.49342,249.3212 123.34904,264.20455 C 82.590696,314.15529 40.823919,293.64625 40.823919,335.20455 C 40.823919,353.81019 72.349045,367.20455 77.349045,361.20455 C 82.349045,355.20455 34.863764,337.32587 87.995492,316.20455 C 133.38711,298.16014 137.43914,294.47663 151.34904,307.20455 z"
        scale={0.3}
        start={0}
        end={0}
      /> */}
      <Circle
        ref={path}
        lineWidth={4}
        stroke={'#e13238'}
        height={100}
        width={100}
        start={0}
        end={0}
        position={[0, 0]}
      />
    </Layout>
    <Layout>
      <Rect
        ref={arrowBox}
        width={220}
        height={40}
        stroke={'#444'}
        lineWidth={1}
        opacity={0}
      />
      <Path
        ref={arrow}
        lineWidth={4}
        stroke={'#e13238'}
        data="M -80 0 L 80 0 M 70 -8 L 80 0 L 70 8"
        start={0}
        end={0}
      />
    </Layout>
    <Layout>
      <Rect
        ref={circleBox}
        width={220}
        height={220}
        stroke={'#444'}
        lineWidth={1}
        opacity={0}
      />
      <Circle
        ref={circle}
        size={180}
        stroke={'#e13238'}
        lineWidth={4}
        start={0}
        end={0}
      />
    </Layout>
    </Layout>
  );
  yield* waitFor(1);
  logMethods(circle(), 3);
  yield* all(...[circle().end(1, 1), path().end(1, 1), pathBox().opacity(1, 0), arrowBox().opacity(1, 0), circleBox().opacity(1, 0)]);
  yield* arrow().end(1, 1);
  yield* circle().fill('#e13238', 1);
  yield* path().fill('#e13238', 1);
});
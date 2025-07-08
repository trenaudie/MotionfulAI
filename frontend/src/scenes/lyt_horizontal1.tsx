import { Node, Rect, makeScene2D } from '@motion-canvas/2d';
import { createRef } from '@motion-canvas/core';
import { waitFor } from '@motion-canvas/core';
export default makeScene2D(function* (view) {
  const leftNode = createRef<Node>();
  const rightNode = createRef<Node>();
  view.fill('#000000');
  view.add(
    <>
      <Node
        ref={leftNode}
        x={-480} // Half of view width (960) / 2 = 480, positioned to the left
        width={900} // Taking up a significant portion of the width
        height={900} // Taking up a significant portion of the height
      >
        {/* Content for the left node will go here */}
      </Node>
      <Node
        ref={rightNode}
        x={480} // Half of view width (960) / 2 = 480, positioned to the right
        width={900} // Taking up a significant portion of the width
        height={900} // Taking up a significant portion of the height
      >
        {/* Content for the right node will go here */}
      </Node>
    </>
  );

  // You can optionally add visual cues during development,
  // but remove them for the final output as per your request.
  // For example, to see the nodes during development:
  view.add(
    <Rect
      ref={leftNode} // Re-using the ref to apply a border for visualization
      stroke={'#FF0000'}
      lineWidth={5}
    />
  );

  view.add(
    <Rect
      ref={rightNode} // Re-using the ref to apply a border for visualization
      stroke={'#0000FF'}
      lineWidth={5}
    />
  );

  yield* waitFor(1); // Keep the scene visible for 1 second
});
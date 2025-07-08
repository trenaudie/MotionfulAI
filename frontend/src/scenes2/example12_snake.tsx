import { makeScene2D } from '@motion-canvas/2d';
import { createRef, createSignal } from '@motion-canvas/core';
import { Rect, Circle } from '@motion-canvas/2d';
import { easeInOutCubic } from '@motion-canvas/core';

export default makeScene2D(function* (view) {
    // refs to our shapes
    view.fill('black');
    const snake = createRef<Rect>();
    const target = createRef<Circle>();

    // reactive state
    const snakeLength = createSignal(1);
    const snakeY = createSignal(0);
    const targetY = createSignal(150);

    // some preset Y positions for the target
    const positions = [150, -150, 0, 100, -100];
    let posIndex = 0;

    view.add(
        <>
            {/* white square snake */}
            <Rect
                ref={snake}
                x={() => -200}
                y={() => snakeY()}
                width={() => 50 * snakeLength()}
                height={() => 50 * snakeLength()}
                fill={() => 'white'}
            />
            {/* red circle target */}
            <Circle
                ref={target}
                x={() => 200}
                y={() => targetY()}
                width={() => 50}
                height={() => 50}
                fill={() => 'red'}
            />
        </>
    );

    // grow until length 5
    const maxLength = 5;
    while (snakeLength() < maxLength) {
        // move vertically to the target
        yield* snakeY(targetY(), 1, easeInOutCubic);
        yield* snake().position.x( target().position.x(), 1, easeInOutCubic );

        // “eat” the target: fade out and grow
        yield* target().opacity(0, 0.2);
        yield* snakeLength(snakeLength() + 1, 0.2);

        // choose next target position and fade back in
        posIndex = (posIndex + 1) % positions.length;
        targetY(positions[posIndex]);
        yield* target().opacity(1, 0.2);
    }
});
import {Circle, makeScene2D} from '@motion-canvas/2d';
import {
  createRef, 
  easeOutSine, 
  easeInOutCubic, 
  easeInExpo,
  easeOutExpo,
  easeInOutExpo,
  linear,
  map, 
  tween, 
  Vector2
} from '@motion-canvas/core';
import { Color } from '@motion-canvas/core';
import {arcLerp} from '@motion-canvas/core';

/**
 * Creates a visual plot of an interpolation function and saves it as an image.
 * 
 * @param interpolation_function The timing function to plot
 * @param num_iterations Number of points to sample (default: 120)
 * @param reverse Whether to use the reverse parameter for the function (default: false)
 * @returns Array of sampled values
 */
function plot_interpolation_function(interpolation_function: InterpolationFunction, num_iterations=120, reverse = false) {
  // Create a canvas for plotting
  const canvas = document.createElement('canvas');
  canvas.width = 500;
  canvas.height = 300;
  const ctx = canvas.getContext('2d');
  
  // Set background
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Calculate values
  const values = [];
  for (let i = 0; i < num_iterations; i++) {
    values.push(interpolation_function(i / num_iterations, reverse, 1));
  }
  
  // Find min and max for scaling
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const valueRange = maxValue - minValue;
  
  // Draw axes
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(30, 30);
  ctx.lineTo(30, canvas.height - 30);
  ctx.lineTo(canvas.width - 30, canvas.height - 30);
  ctx.stroke();
  
  // Draw labels
  ctx.fillStyle = '#333';
  ctx.font = '14px Arial';
  ctx.fillText('0', 25, canvas.height - 15);
  ctx.fillText('1', canvas.width - 15, canvas.height - 15);
  ctx.fillText('0', 15, canvas.height - 35);
  ctx.fillText('1', 15, 35);
  
  // Add function name as title
  const functionName = interpolation_function.name || 'Function';
  ctx.font = '16px Arial';
  ctx.fillText(`${functionName}${reverse ? ' (reversed)' : ''}`, canvas.width / 2 - 60, 20);
  
  // Draw the curve
  ctx.strokeStyle = '#ff6470';
  ctx.lineWidth = 3;
  ctx.beginPath();
  
  const plotHeight = canvas.height - 60;
  const plotWidth = canvas.width - 60;
  
  for (let i = 0; i < values.length; i++) {
    const x = 30 + (i / (num_iterations - 1)) * plotWidth;
    const normalizedValue = (values[i] - minValue) / (valueRange || 1);
    const y = canvas.height - 30 - normalizedValue * plotHeight;
    
    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }
  ctx.stroke();
  
  // Draw reference line at y=x (linear)
  ctx.strokeStyle = '#88C0D0';
  ctx.lineWidth = 1;
  ctx.setLineDash([5, 5]);
  ctx.beginPath();
  ctx.moveTo(30, canvas.height - 30);
  ctx.lineTo(canvas.width - 30, 30);
  ctx.stroke();
  ctx.setLineDash([]);
  
  // Save the image
  const dataUrl = canvas.toDataURL('image/png');
  
  // Log the function name and its min/max values
  console.log(`Plot for ${functionName}${reverse ? ' (reversed)' : ''}:`);
  console.log(`Min value: ${minValue}, Max value: ${maxValue}`);
  
  // In Motion Canvas, we need to use the export mechanism
  if (import.meta.hot) {
    import.meta.hot.send('motion-canvas:export', {
      frame: Date.now(), // Use timestamp to ensure unique filename
      name: `interpolation_${functionName}${reverse ? '_reversed' : ''}`,
      data: dataUrl,
      mimeType: 'image/png',
      subDirectories: ['plots'],
    });
    console.log(`Plot saved to output/plots/interpolation_${functionName}${reverse ? '_reversed' : ''}.png`);
  }
  
  return values;
}

export default makeScene2D(function* (view) {

  const circle = createRef<Circle>();

  view.add(
    <Circle
      ref={circle}
      x={-300}
      width={240}
      height={240}
      fill="#e13238"
    />,
  );

  // // Plot various interpolation functions
  // plot_interpolation_function(linear);
  // plot_interpolation_function(easeInOutCubic);
  // plot_interpolation_function(easeOutSine);
  // plot_interpolation_function(easeInExpo);
  // plot_interpolation_function(easeOutExpo);
  // plot_interpolation_function(easeInOutExpo);
  
  // // Also plot some reversed functions
  // plot_interpolation_function(easeInOutCubic, 120, true);
  // plot_interpolation_function(easeOutSine, 120, true);
  
  // Example of color lerp
  const colours_lerped = []
  const num_seconds_tween = 2;
  const num_iterations_tween = num_seconds_tween * 60;
  
  for (let i = 0; i < num_iterations_tween; i++) {
    colours_lerped.push(
      Color.lerp(
        new Color('red'),
        new Color('blue'), 
        i / num_iterations_tween
      )
    );
  }
  
  for (let i = 0; i < num_iterations_tween; i++) {
    colours_lerped.push(
      Color.lerp(
        new Color('blue'),
        new Color('green'), 
        i / num_iterations_tween
      )
    );
  }
  
  console.log(`len colours_lerped ${colours_lerped.length}`);
  const colours_lerped_final = colours_lerped.filter((_, index) => index % 2 === 0);
  
  // Animate the circle using easeInOutCubic and arcLerp
  yield*   tween(2, value => {
    const colour_1lerp =       Color.lerp(
      new Color('#e6a700'),
      new Color('#e13238'),
      easeInOutCubic(value),
    );
    console.log(`colour_1lerp ${colour_1lerp}`)
    circle().fill(colour_1lerp);
  });
});
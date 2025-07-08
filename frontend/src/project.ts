import {makeProject} from '@motion-canvas/core';


// export async function generateScene(prompt: string) {
//   const response = await fetch('http://localhost:5000/write_code', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ prompt }),
//   });

//   if (!response.ok) {
//     const error = await response.json();
//     throw new Error(error.error || 'Failed to generate scene');
//   }
  
//   const { filename } = await response.json();
//   console.log(`Received response from server: Scene2d written to ${filename}`);
//   return filename;
// }

// const filename = await generateScene('create a bouncing circle animation using motion-canvas');
// let filenameWithoutExtension :string= filename.split('.')[0];
// const sceneModule = await import(`./scenes/${filenameWithoutExtension}?scene`);
// const example = sceneModule.default;

import example from './scenes2/example12_snake?scene';
export default makeProject({
  scenes: [example],
});

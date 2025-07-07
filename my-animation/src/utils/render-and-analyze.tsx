// // scripts/render-and-analyze.ts

// import fs from "fs";
// import path from "path";
// import { renderSceneToBuffer } from "@motion-canvas/node";
// import scene, { SCENE_DURATION } from "../scenes/example";
// import { analyzeFrames } from "../src/utils/video";

// async function run() {
//   // 1. Get the duration from the scene itself—no hard‑coding!
//   const duration = SCENE_DURATION; // seconds
//   const times = [0, duration / 2, duration];

//   // 2. Where are we saving? outDir is: <projectRoot>/out
//   //    __dirname is <projectRoot>/scripts, so "../out" → projectRoot/out
//   const outDir = path.resolve(__dirname, "../out");

//   // 3. Ensure the output directory exists
//   //    fs.existsSync checks “does this path exist?”
//   //    If not, mkdirSync creates it (with recursive=true to make parent dirs too).
//   if (!fs.existsSync(outDir)) {
//     fs.mkdirSync(outDir, { recursive: true });
//   }

//   // 4. Render & save each frame immediately
//   console.log("Rendering frames…");
//   const buffers = await Promise.all(
//     times.map(async (t, i) => {
//       const buf = await renderSceneToBuffer(scene, {
//         time: t * 1000, // ms
//         width: 1280,
//         height: 720,
//       });
//       const filename = path.join(outDir, `frame-${i}-${t}s.png`);
//       fs.writeFileSync(filename, buf);
//       console.log(`✔ Saved ${filename}`);
//       return buf;
//     })
//   );

//   // 5. Prepare for analysis
//   const framesBase64 = buffers.map((b) => b.toString("base64"));

//   // 6. Analyze—and on error, still save an error report
//   try {
//     console.log("Analyzing frames…");
//     const analysis = await analyzeFrames(framesBase64);
//     fs.writeFileSync(
//       path.join(outDir, "analysis.json"),
//       JSON.stringify(analysis, null, 2)
//     );
//     console.log("✔ Analysis saved to analysis.json");
//   } catch (err: any) {
//     console.error("✖ Analysis error:", err.message);
//     fs.writeFileSync(
//       path.join(outDir, "analysis-error.json"),
//       JSON.stringify(
//         { message: err.message, stack: err.stack?.toString() },
//         null,
//         2
//       )
//     );
//     console.log("✔ Error details saved to analysis-error.json");
//     process.exitCode = 1;
//     return;
//   }

//   console.log("All done! Check the `out/` folder in your project root.");
// }

// run().catch((e) => {
//   console.error("Fatal error:", e);
//   process.exit(1);
// });

// scripts/render-and-analyze.ts
// src/scripts/render-and-analyze.tsx

import 'dotenv/config';
import fs from 'fs/promises';
import path from 'path';
import { analyzeFrames, VideoAnalysis } from './api';
import scene, { SCENE_DURATION } from '../scenes/example';

if (!process.env.GROQ_API_KEY) {
  throw new Error('GROQ_API_KEY is missing. Check your .env setup.');
}

export async function runAnalysis(): Promise<
  | { success: true; data: VideoAnalysis }
  | { success: false; error: string }
> {
  const times: number[] = [0, SCENE_DURATION / 2, SCENE_DURATION];
  const fps = 30;

  const frames: string[] = [
    `frame-0.png`,
    `frame-${Math.floor(fps * (SCENE_DURATION / 2))}.png`,
    `frame-${Math.floor(fps * SCENE_DURATION)}.png`,
  ];

  try {
    const framesBase64: string[] = await Promise.all(
      frames.map(async (file) => {
        const buf = await fs.readFile(path.resolve('out', file));
        return buf.toString('base64');
      })
    );

    const analysis = await analyzeFrames(framesBase64, times);
    return { success: true, data: analysis };
  } catch (err: any) {
    return { success: false, error: err.message || 'Unknown error occurred' };
  }
}





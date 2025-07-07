import Groq from "groq-sdk";
import { z } from "zod";

// Constants
const MODEL = "meta-llama/llama-4-scout-17b-16e-instruct";
const TEMPERATURE = 0.3;
const MAX_TOKENS = 8192;
const RETRY_ATTEMPTS = 3;
const RETRY_DELAY_MS = 1000;
const BATCH_DELAY_MS = 200;

const groqClient = new Groq({ apiKey: process.env.GROQ_API_KEY! });

// Custom error class
export class AnalysisError extends Error {
  constructor(
    message: string,
    public code: "VALIDATION" | "API" | "PARSER" | "NETWORK"
  ) {
    super(message);
    this.name = "AnalysisError";
  }
}

// Schema Definitions
const FrameIssue = z.object({
  severity: z.enum(["low", "medium", "high", "critical"]),
  description: z.string(),
  suggestion: z.string().optional(),
});

const FrameAnalysis = z.object({
  frameIndex: z.number(),
  timestamp: z.number(),
  qualityScore: z.number().min(1).max(10),
  objectsDetected: z.array(z.string()),
  dominantColors: z.array(z.string()),
  compositionNotes: z.string(),
  issues: z.array(FrameIssue),
});

export const VideoAnalysis = z.object({
  summary: z.string(),
  overallScore: z.number().min(1).max(10),
  frames: z.array(FrameAnalysis),
  recommendations: z.array(z.string()),
  processingTime: z.number(),
});

export type VideoAnalysis = z.infer<typeof VideoAnalysis>;
export type FrameAnalysis = z.infer<typeof FrameAnalysis>;
export type FrameIssue = z.infer<typeof FrameIssue>;

// Prompt Builder
function buildAnalysisPrompt(timestamps: number[]): string {
  return `
You are an expert multimodal code-motion reviewer analyzing frames from a Motion Canvas animation.

For each frame, analyze:
• Visual composition and layout quality
• Object detection and positioning
• Color palette and visual harmony
• Technical rendering quality
• Potential issues or improvements

Provide a quality score (1-10) for each frame and overall.
Identify any issues with severity levels: low, medium, high, critical.

Analyze frames at timestamps: ${timestamps.join(", ")} seconds.

Return your analysis as a JSON object with this exact structure:
{
  "summary": "Brief overall assessment of the animation quality",
  "overallScore": 8,
  "frames": [
    {
      "frameIndex": 0,
      "timestamp": 0,
      "qualityScore": 8,
      "objectsDetected": ["circle", "text", "background"],
      "dominantColors": ["blue", "white", "gray"],
      "compositionNotes": "Well-balanced composition with clear focal point",
      "issues": [
        {
          "severity": "medium",
          "description": "Text readability could be improved",
          "suggestion": "Increase contrast or font size"
        }
      ]
    }
  ],
  "recommendations": ["Improve text contrast", "Consider smoother transitions"],
  "processingTime": 0
}

Be thorough but concise. Focus on actionable feedback.
`;
}

// Extractor
function extractJson(content: string): string {
  const trimmed = content.trim();
  const jsonMatch = trimmed.match(/__BEGIN_JSON__([\s\S]+?)__END_JSON__/);
  if (jsonMatch) {
    return jsonMatch[1].trim();
  }
  return trimmed;
}

// Schema parser
function safeParseVideoAnalysis(jsonString: string): Omit<VideoAnalysis, 'processingTime'> {
  let rawAnalysis: unknown;

  try {
    rawAnalysis = JSON.parse(jsonString);
  } catch (error) {
    throw new AnalysisError(
      `Invalid JSON response: ${error instanceof Error ? error.message : 'Unknown error'}`,
      "PARSER"
    );
  }

  const result = VideoAnalysis.omit({ processingTime: true }).safeParse(rawAnalysis);
  if (!result.success) {
    console.error("Validation errors:", result.error.format());
    throw new AnalysisError(
      `Invalid analysis JSON structure: ${result.error.errors.map(e => e.message).join(', ')}`,
      "VALIDATION"
    );
  }

  return result.data;
}

// Sleep
async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Retry wrapper
async function retryable<T>(
  operation: () => Promise<T>,
  attempts: number = RETRY_ATTEMPTS
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i < attempts; i++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (error instanceof AnalysisError && error.code === "VALIDATION") {
        throw error;
      }

      if (i === attempts - 1) {
        throw new AnalysisError(
          `Operation failed after ${attempts} attempts: ${lastError.message}`,
          "NETWORK"
        );
      }

      const delay = RETRY_DELAY_MS * Math.pow(2, i);
      console.warn(`Attempt ${i + 1} failed, retrying in ${delay}ms...`);
      await sleep(delay);
    }
  }

  throw lastError!;
}

// 🔍 Main function
export async function analyzeFrames(
  frames: string[],
  timestamps: number[]
): Promise<VideoAnalysis> {
  const startTime = Date.now();

  if (frames.length !== timestamps.length) {
    throw new AnalysisError(
      "Frames and timestamps arrays must have the same length",
      "VALIDATION"
    );
  }

  if (frames.length === 0) {
    throw new AnalysisError("No frames provided for analysis", "VALIDATION");
  }

  const prompt = buildAnalysisPrompt(timestamps);

  try {
    const response = await retryable(() =>
      groqClient.chat.completions.create({
        model: MODEL,
        messages: [
          { role: "system", content: prompt },
          {
            role: "user",
            content: [
              {
                type: "text",
                text: `Analyze these ${frames.length} frames from a Motion Canvas animation.`
              },
              ...frames.map((frame) => ({
                type: "image_url" as const,
                image_url: {
                  url: `data:image/png;base64,${frame}`
                }
              }))
            ]
          }
        ],
        max_tokens: MAX_TOKENS,
        temperature: TEMPERATURE,
        response_format: { type: "json_object" },
      })
    );

    const content = response.choices[0].message.content;
    if (!content) {
      throw new AnalysisError("No response content from Groq API", "API");
    }

    if (process.env.NODE_ENV === 'development') {
      console.log("Raw API response:", content);
    }

    const jsonString = extractJson(content);
    const parsed = safeParseVideoAnalysis(jsonString);

    return {
      ...parsed,
      processingTime: Date.now() - startTime
    };

  } catch (error) {
    if (error instanceof AnalysisError) throw error;

    throw new AnalysisError(
      `Unexpected error during analysis: ${error instanceof Error ? error.message : String(error)}`,
      "API"
    );
  }
}

// 🔎 Single frame
// export async function analyzeFrame(
//   frame: string,
//   timestamp: number,
//   frameIndex: number
// ): Promise<FrameAnalysis> {
//   const analysis = await analyzeFrames([frame], [timestamp]);
//   return analysis.frames[0];
// }

// // 🗂 Batching
// export async function analyzeFramesBatch(
//   frames: string[],
//   timestamps: number[],
//   batchSize: number = 3
// ): Promise<VideoAnalysis> {
//   if (frames.length !== timestamps.length) {
//     throw new AnalysisError(
//       "Frames and timestamps arrays must have the same length",
//       "VALIDATION"
//     );
//   }

//   if (frames.length <= batchSize) {
//     return analyzeFrames(frames, timestamps);
//   }

//   const batches = [];
//   for (let i = 0; i < frames.length; i += batchSize) {
//     batches.push({
//       frames: frames.slice(i, i + batchSize),
//       timestamps: timestamps.slice(i, i + batchSize),
//     });
//   }

//   const results: VideoAnalysis[] = [];

//   for (let i = 0; i < batches.length; i++) {
//     const batch = batches[i];
//     console.log(`Processing batch ${i + 1}/${batches.length}...`);

//     try {
//       const result = await analyzeFrames(batch.frames, batch.timestamps);
//       results.push(result);
//       if (i < batches.length - 1) {
//         await sleep(BATCH_DELAY_MS);
//       }
//     } catch (error) {
//       console.error(`Batch ${i + 1} failed:`, error);
//       throw error;
//     }
//   }

//   const combined: VideoAnalysis = {
//     summary: results.map(r => r.summary).join(' '),
//     overallScore: Math.round(results.reduce((sum, r) => sum + r.overallScore, 0) / results.length),
//     frames: results.flatMap(r => r.frames),
//     recommendations: [...new Set(results.flatMap(r => r.recommendations))],
//     processingTime: results.reduce((sum, r) => sum + r.processingTime, 0)
//   };

//   return combined;
// }

// // 🧪 Schema test
// export function testSchema(): void {
//   const exampleData = {
//     summary: "Test animation with good composition",
//     overallScore: 8,
//     frames: [
//       {
//         frameIndex: 0,
//         timestamp: 0,
//         qualityScore: 8,
//         objectsDetected: ["circle", "text"],
//         dominantColors: ["blue", "white"],
//         compositionNotes: "Well balanced",
//         issues: [
//           {
//             severity: "low" as const,
//             description: "Minor alignment issue",
//             suggestion: "Adjust positioning"
//           }
//         ]
//       }
//     ],
//     recommendations: ["Improve contrast"],
//     processingTime: 1500
//   };

//   const result = VideoAnalysis.safeParse(exampleData);
//   if (!result.success) {
//     console.error("Schema test failed:", result.error.format());
//     throw new Error("Schema validation failed");
//   }

//   console.log("Schema validation passed ✓");
// }

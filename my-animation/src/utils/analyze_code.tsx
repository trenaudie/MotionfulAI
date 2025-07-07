import Groq from "groq-sdk";
import { z } from "zod";
import { VideoAnalysis } from './api';

// Constants
const MODEL = "meta-llama/llama-4-scout-17b-16e-instruct";
const TEMPERATURE = 0.2;
const MAX_TOKENS = 8192;
const RETRY_ATTEMPTS = 3;
const RETRY_DELAY_MS = 1000;

const groqClient = new Groq({ apiKey: process.env.GROQ_API_KEY! });

// Custom error class
export class CodeAnalysisError extends Error {
  constructor(
    message: string,
    public code: "VALIDATION" | "API" | "PARSER" | "NETWORK"
  ) {
    super(message);
    this.name = "CodeAnalysisError";
  }
}

// Schema Definitions
const CodeIssue = z.object({
  severity: z.enum(["low", "medium", "high", "critical"]),
  line: z.number().optional(),
  description: z.string(),
  suggestion: z.string(),
  diffPatch: z.string().optional(),
});

const CodeAnalysis = z.object({
  summary: z.string(),
  overallCodeQuality: z.number().min(1).max(10),
  issues: z.array(CodeIssue),
  improvements: z.array(z.string()),
  errorAnalysis: z.string().optional(),
  videoCorrelation: z.string().optional(),
  processingTime: z.number(),
});

export type CodeAnalysis = z.infer<typeof CodeAnalysis>;
export type CodeIssue = z.infer<typeof CodeIssue>;

// Prompt Builder
function buildCodeAnalysisPrompt(
  code: string,
  videoAnalysis?: VideoAnalysis,
  errorOutput?: string
): string {
  const videoContext = videoAnalysis ? `
Video Analysis Context:
- Overall Score: ${videoAnalysis.overallScore}/10
- Summary: ${videoAnalysis.summary}
- Key Issues: ${videoAnalysis.frames.flatMap(f => f.issues.map(i => i.description)).join(', ')}
- Recommendations: ${videoAnalysis.recommendations.join(', ')}
` : '';

  const errorContext = errorOutput ? `
Error Output:
${errorOutput}
` : '';

  return `
You are an expert TypeScript/React code reviewer with expertise in Motion Canvas animations.

Analyze the provided TSX code and suggest improvements. Focus on:
• Code quality and best practices
• Performance optimizations
• Type safety improvements
• Animation-specific optimizations
• Error handling improvements
• Code structure and maintainability

${videoContext}${errorContext}

**IMPORTANT**: If video analysis or error output is provided, correlate code issues with visual problems or runtime errors. Pinpoint the exact code lines causing issues.

Return your analysis as a JSON object with this exact structure:
{
  "summary": "Brief overall assessment of code quality",
  "overallCodeQuality": 7,
  "issues": [
    {
      "severity": "medium",
      "line": 42,
      "description": "Potential performance issue in animation loop",
      "suggestion": "Use useCallback to memoize the animation function",
      "diffPatch": "- const animate = () => { ... }\\n+ const animate = useCallback(() => { ... }, [dependencies]);"
    }
  ],
  "improvements": ["Add proper error boundaries", "Implement loading states"],
  "errorAnalysis": "Analysis of any runtime errors and their causes",
  "videoCorrelation": "How code issues relate to visual problems in the video",
  "processingTime": 0
}

Provide clear, actionable diff-style suggestions that can be applied directly to the codebase.
Be thorough but concise. Focus on the most impactful improvements first.
`;
}

// JSON extractor
function extractJson(content: string): string {
  const trimmed = content.trim();
  const jsonMatch = trimmed.match(/```json\s*([\s\S]+?)\s*```/);
  if (jsonMatch) {
    return jsonMatch[1].trim();
  }
  
  // Try to find JSON object boundaries
  const startIndex = trimmed.indexOf('{');
  const lastIndex = trimmed.lastIndexOf('}');
  if (startIndex !== -1 && lastIndex !== -1 && lastIndex > startIndex) {
    return trimmed.substring(startIndex, lastIndex + 1);
  }
  
  return trimmed;
}

// Schema parser
function safeParseCodeAnalysis(jsonString: string): Omit<CodeAnalysis, 'processingTime'> {
  let rawAnalysis: unknown;

  try {
    rawAnalysis = JSON.parse(jsonString);
  } catch (error) {
    throw new CodeAnalysisError(
      `Invalid JSON response: ${error instanceof Error ? error.message : 'Unknown error'}`,
      "PARSER"
    );
  }

  const result = CodeAnalysis.omit({ processingTime: true }).safeParse(rawAnalysis);
  if (!result.success) {
    console.error("Validation errors:", result.error.format());
    throw new CodeAnalysisError(
      `Invalid analysis JSON structure: ${result.error.errors.map(e => e.message).join(', ')}`,
      "VALIDATION"
    );
  }

  return result.data;
}

// Sleep utility
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

      if (error instanceof CodeAnalysisError && error.code === "VALIDATION") {
        throw error;
      }

      if (i === attempts - 1) {
        throw new CodeAnalysisError(
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
export async function analyzeCode(
  code: string,
  videoAnalysis?: VideoAnalysis,
  errorOutput?: string
): Promise<CodeAnalysis> {
  const startTime = Date.now();

  if (!code.trim()) {
    throw new CodeAnalysisError("No code provided for analysis", "VALIDATION");
  }

  const prompt = buildCodeAnalysisPrompt(code, videoAnalysis, errorOutput);

  try {
    const response = await retryable(() =>
      groqClient.chat.completions.create({
        model: MODEL,
        messages: [
          { role: "system", content: prompt },
          {
            role: "user",
            content: `Analyze this TSX code and provide improvement suggestions:\n\n\`\`\`tsx\n${code}\n\`\`\``
          }
        ],
        max_tokens: MAX_TOKENS,
        temperature: TEMPERATURE,
        response_format: { type: "json_object" },
      })
    );

    const content = response.choices[0].message.content;
    if (!content) {
      throw new CodeAnalysisError("No response content from Groq API", "API");
    }

    if (process.env.NODE_ENV === 'development') {
      console.log("Raw API response:", content);
    }

    const jsonString = extractJson(content);
    const parsed = safeParseCodeAnalysis(jsonString);

    return {
      ...parsed,
      processingTime: Date.now() - startTime
    };

  } catch (error) {
    if (error instanceof CodeAnalysisError) throw error;

    throw new CodeAnalysisError(
      `Unexpected error during code analysis: ${error instanceof Error ? error.message : String(error)}`,
      "API"
    );
  }
}

// Utility function to format analysis output
export function formatAnalysisOutput(analysis: CodeAnalysis): string {
  const sections = [
    ` Code Analysis Summary`,
    `Overall Quality: ${analysis.overallCodeQuality}/10`,
    `${analysis.summary}`,
    ``,
    ` Issues Found (${analysis.issues.length}):`,
    ...analysis.issues.map((issue, index) => {
      const severity = issue.severity.toUpperCase();
      const line = issue.line ? ` (Line ${issue.line})` : '';
      return [
        `${index + 1}. [${severity}]${line} ${issue.description}`,
        `   💡 Suggestion: ${issue.suggestion}`,
        ...(issue.diffPatch ? [`   Diff: ${issue.diffPatch}`] : []),
        ``
      ].join('\n');
    }),
    `Improvements:`,
    ...analysis.improvements.map((improvement, index) => `${index + 1}. ${improvement}`),
    ``,
    ...(analysis.errorAnalysis ? [`🐛 Error Analysis:`, analysis.errorAnalysis, ``] : []),
    ...(analysis.videoCorrelation ? [`🎬 Video Correlation:`, analysis.videoCorrelation, ``] : []),
    ` Processing Time: ${analysis.processingTime}ms`
  ];

  return sections.join('\n');
}

// Example usage function
export async function analyzeCodeWithContext(
  tsxCode: string,
  videoAnalysis?: VideoAnalysis,
  errorOutput?: string
): Promise<void> {
  try {
    console.log(' Starting code analysis...');
    const analysis = await analyzeCode(tsxCode, videoAnalysis, errorOutput);
    
    console.log('\n' + formatAnalysisOutput(analysis));
    
    // Save analysis to file if needed
    if (process.env.NODE_ENV === 'development') {
      const fs = await import('fs/promises');
      await fs.writeFile(
        'code-analysis-result.json',
        JSON.stringify(analysis, null, 2)
      );
      console.log('\n Analysis saved to code-analysis-result.json');
    }
    
  } catch (error) {
    console.error('Error analyzing code:', error instanceof Error ? error.message : String(error));
    
    if (error instanceof CodeAnalysisError) {
      console.error(`Error type: ${error.code}`);
    }
  }
}
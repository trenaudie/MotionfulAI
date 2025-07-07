# import os
# import time
# import base64
# import json
# import re
# from pathlib import Path
# from typing import List, Dict, Optional, Union
# from pydantic import BaseModel, ValidationError, Field
# from groq import Groq
# import logging
# from dotenv import load_dotenv

# # ─── Config ──────────────────────────────────────────────────────
# MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
# TEMPERATURE = 0.3
# MAX_TOKENS = 8192
# FRAME_COUNT = 5
# SCENE_DURATION = 5.0  # seconds
# OUTPUT_DIR = Path("D:\\New_hackathon\\my-animation\\my-animation\\out2")
# ERROR_JSON = Path("D:\\New_hackathon\\my-animation\\my-animation\\out2_text.json")

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # ─── Groq Client ─────────────────────────────────────────────────


# load_dotenv()  # loads variables from .env into environment

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise RuntimeError("Missing GROQ_API_KEY in environment")
# groq_client = Groq(api_key=api_key)

# # ─── Models ──────────────────────────────────────────────────────
# class AnalysisError(Exception):
#     def __init__(self, message: str, code: str):
#         super().__init__(message)
#         self.code = code

# class FrameIssue(BaseModel):
#     severity: str = Field(..., pattern=r"^(low|medium|high|critical)$")
#     description: str
#     suggestion: Optional[str] = None

# class FrameAnalysis(BaseModel):
#     frameIndex: int
#     timestamp: float
#     qualityScore: int = Field(..., ge=1, le=10)
#     objectsDetected: List[str]
#     dominantColors: List[str]
#     compositionNotes: str
#     issues: List[FrameIssue] = []

# class VideoAnalysis(BaseModel):
#     summary: str
#     overallScore: int = Field(..., ge=1, le=10)
#     frames: List[FrameAnalysis]
#     recommendations: List[str]
#     processingTime: int = 0

# # ─── Prompt Builder ──────────────────────────────────────────────
# def build_analysis_prompt(timestamps: List[float]) -> str:
#     return f"""You are an expert multimodal motion-canvas reviewer. Analyze the following frames semantically.

# ONLY respond with **strictly valid JSON**. Do NOT include markdown formatting, assistant tags, or extra tokens.

# Required aspects to analyze:
# - Layout, balance, and visual hierarchy
# - Object recognition and spatial placement
# - Color harmony and emotional tone
# - Technical rendering fidelity
# - Suggestions for improvement

# Timestamps: {', '.join(f'{t:.2f}' for t in timestamps)}

# Respond with this exact structure:
# {{
#   "summary": "Brief overall assessment of the animation",
#   "overallScore": 8,
#   "frames": [
#     {{
#       "frameIndex": 0,
#       "timestamp": 0.00,
#       "qualityScore": 8,
#       "objectsDetected": ["object1", "object2"],
#       "dominantColors": ["color1", "color2"],
#       "compositionNotes": "Frame layout explanation",
#       "issues": [
#         {{
#           "severity": "low",
#           "description": "Brief issue description",
#           "suggestion": "How to improve"
#         }}
#       ]
#     }}
#   ],
#   "recommendations": ["Final visual recommendations"],
#   "processingTime": 0
# }}"""

# # ─── JSON Extractor ─────────────────────────────────────────────
# def extract_json(content: str) -> str:
#     patterns = [
#         r'(\{.*?\})',
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, content, re.DOTALL)
#         if match:
#             candidate = match.group(1)
#             try:
#                 json.loads(candidate)
#                 return candidate
#             except json.JSONDecodeError:
#                 continue
#     raise AnalysisError("Could not extract valid JSON", "PARSER")

# # ─── Validator ───────────────────────────────────────────────────
# def safe_parse_video_analysis(json_str: str) -> VideoAnalysis:
#     try:
#         data = json.loads(json_str)
#         logger.info("JSON parsed successfully")
#         return VideoAnalysis(**data)
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decode error: {e}")
#         raise AnalysisError(f"Invalid JSON: {e}", "PARSER")
#     except ValidationError as e:
#         logger.error(f"Pydantic validation error: {e}")
#         raise AnalysisError(f"Schema validation failed: {e}", "VALIDATION")

# # ─── Retry Logic ─────────────────────────────────────────────────
# def retryable(fn, attempts=3, delay_ms=1000):
#     for i in range(attempts):
#         try:
#             return fn()
#         except AnalysisError as e:
#             if i < attempts - 1:
#                 logger.warning(f"Attempt {i+1} failed, retrying: {e}")
#                 time.sleep(delay_ms / 1000 * (2 ** i))
#             else:
#                 raise

# # ─── Frame Helpers ──────────────────────────────────────────────
# def get_evenly_spaced_frames(folder: Path, count: int) -> List[Path]:
#     imgs = sorted(folder.glob("*.png"))
#     if len(imgs) == 0:
#         raise AnalysisError("No frames found", "NOT_FOUND")
#     if len(imgs) <= count:
#         return imgs
#     step = (len(imgs) - 1) / (count - 1)
#     return [imgs[round(i * step)] for i in range(count)]

# def load_render_errors(json_path: Path) -> Dict[str, str]:
#     try:
#         if json_path.exists():
#             return json.loads(json_path.read_text()).get("errors", {})
#     except Exception:
#         return {}
#     return {}

# def load_frames_base64(paths: List[Path]) -> List[str]:
#     frames = []
#     for path in paths:
#         data = base64.b64encode(path.read_bytes()).decode("utf-8")
#         frames.append(data)
#     return frames

# # ─── API Request ────────────────────────────────────────────────
# def analyze_frames(frames_b64: List[str], timestamps: List[float]) -> VideoAnalysis:
#     prompt = build_analysis_prompt(timestamps)
#     def request():
#         resp = groq_client.chat.completions.create(
#             model=MODEL,
#             messages=[
#                 {"role": "system", "content": prompt},
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Please analyze the following frames and respond only with valid JSON."},
#                         *[
#                             {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}
#                             for img in frames_b64
#                         ]
#                     ]
#                 }
#             ],
#             temperature=TEMPERATURE,
#             max_tokens=MAX_TOKENS,
#             response_format={"type": "json_object"}
#         )
#         raw = resp.choices[0].message.content
#         if not raw:
#             raise AnalysisError("Empty response", "API")
#         js = extract_json(raw)
#         analysis = safe_parse_video_analysis(js)
#         analysis.processingTime = int((time.time() - start) * 1000)
#         return analysis
#     start = time.time()
#     return retryable(request)

# # ─── API Response ───────────────────────────────────────────────
# class APIResponse(BaseModel):
#     success: bool
#     data: Optional[VideoAnalysis] = None
#     error: Optional[str] = None
#     error_code: Optional[str] = None
#     timestamp: str
#     processing_time_ms: int

# def create_api_response(analysis: VideoAnalysis = None, error: Exception = None) -> Dict:
#     response = APIResponse(
#         success=analysis is not None,
#         data=analysis,
#         error=str(error) if error else None,
#         error_code=getattr(error, 'code', None) if error else None,
#         timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
#         processing_time_ms=analysis.processingTime if analysis else 0
#     )
#     return response.model_dump()

# # ─── Main ───────────────────────────────────────────────────────
# def main():
#     print("Analyzing semantic frames from Motion Canvas...")
#     try:
#         frames = get_evenly_spaced_frames(OUTPUT_DIR, FRAME_COUNT)
#         print(f"Found {len(frames)} frames")
#         errors = load_render_errors(ERROR_JSON)
#         timestamps = [i * SCENE_DURATION / (FRAME_COUNT - 1) for i in range(FRAME_COUNT)]
#         print(f"Analyzing at timestamps: {timestamps}")
#         frames_b64 = load_frames_base64(frames)
#         print(f"Loaded {len(frames_b64)} frames for analysis")
#         analysis = analyze_frames(frames_b64, timestamps)
#         for fa in analysis.frames:
#             err = errors.get(frames[fa.frameIndex].name)
#             if err:
#                 fa.issues.append(FrameIssue(severity="high", description=f"Render error: {err}"))
#         output_path = OUTPUT_DIR.parent / "semantic_analysis.json"
#         with open(output_path, 'w') as f:
#             json.dump(analysis.model_dump(), f, indent=2)
#         print(f"Analysis saved to {output_path}")
#         api_response = create_api_response(analysis=analysis)
#         api_output_path = OUTPUT_DIR.parent / "api_response.json"
#         with open(api_output_path, 'w') as f:
#             json.dump(api_response, f, indent=2)
#         print(f"API response saved to {api_output_path}")
#     except Exception as e:
#         print(f"Analysis failed: {e}")
#         api_response = create_api_response(error=e)
#         api_output_path = OUTPUT_DIR.parent / "api_response.json"
#         with open(api_output_path, 'w') as f:
#             json.dump(api_response, f, indent=2)
#         print(f"Error response saved to {api_output_path}")

# if __name__ == "__main__":
#     main()

# semantic_analysis.py

import os
import time
import base64
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from groq import Groq
import logging

# ───── Config ──────────────────────────────
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEMPERATURE = 0.3
MAX_TOKENS = 8192
FRAME_COUNT = 5
SCENE_DURATION = 5.0
OUTPUT_DIR = Path("D:\\New_hackathon\\my-animation\\my-animation\\out2")
ERROR_JSON = Path("D:\\New_hackathon\\my-animation\\my-animation\\out2_text.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("Missing GROQ_API_KEY")
groq_client = Groq(api_key=api_key)


# ─── Models ──────────────────────────────────────────────────────
class AnalysisError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

class FrameIssue(BaseModel):
    severity: str = Field(..., pattern=r"^(low|medium|high|critical)$")
    description: str
    suggestion: Optional[str] = None

class FrameAnalysis(BaseModel):
    frameIndex: int
    timestamp: float
    qualityScore: int = Field(..., ge=1, le=10)
    objectsDetected: List[str]
    dominantColors: List[str]
    compositionNotes: str
    issues: List[FrameIssue] = []

class VideoAnalysis(BaseModel):
    summary: str
    overallScore: int = Field(..., ge=1, le=10)
    frames: List[FrameAnalysis]
    recommendations: List[str]
    processingTime: int = 0  # ms

# ─── Improved Prompt ───────────────────────────────────────────────────────
def build_analysis_prompt(timestamps: List[float]) -> str:
    return f"""You are an expert multimodal motion-canvas reviewer. Analyze the following frames semantically.

IMPORTANT: You MUST respond with valid JSON only. No additional text, explanations, or markdown formatting.

Analyze these aspects:
• Layout, balance, and visual hierarchy
• Object recognition and spatial placement
• Color harmony and emotional tone
• Technical rendering fidelity
• Suggestions for improvement

Please analyze the *sequence of frames as a whole*, not just individually. You must focus on:
- Object continuity across time
- Motion consistency and natural progression
- Frame-to-frame semantic coherence
- Animation logic and cause-effect
- Visual storytelling and emotional flow
- Unexpected glitches or rendering breaks

Timestamps (seconds): {', '.join(f'{t:.2f}' for t in timestamps)}

Respond with this exact JSON structure:
{{
  "summary": "Brief overall assessment of the animation",
  "overallScore": 8,
  "frames": [
    {{
      "frameIndex": 0,
      "timestamp": 0.00,
      "qualityScore": 8,
      "objectsDetected": ["object1", "object2"],
      "dominantColors": ["color1", "color2"],
      "compositionNotes": "Description of composition",
      "issues": [
        {{
          "severity": "low",
          "description": "Issue description",
          "suggestion": "Improvement suggestion"
        }}
      ]
    }}
  ],
  "recommendations": ["recommendation1", "recommendation2"],
  "processingTime": 0
}}

Severity levels: low, medium, high, critical
Quality scores: 1-10 (integers only)
Provide valid JSON with no extra text."""

# ─── Improved JSON Extraction ─────────────────────────────────────────────────
def extract_json_and_save(content: str, save_path: Path) -> None:
    """Save raw or near-JSON API response directly to a text file for review."""
    if not content:
        raise AnalysisError("Empty content received", "API")
    
    try:
        save_path.write_text(content, encoding="utf-8")
        logger.info(f"Raw API output saved to: {save_path}")
    except Exception as e:
        logger.error(f"Failed to save raw output: {e}")
        raise AnalysisError(f"Failed to save output: {e}", "FILE_ERROR")


# def safe_parse_video_analysis(json_str: str) -> VideoAnalysis:
#     """Parse JSON with detailed error reporting"""
#     try:
#         # First, try to parse JSON
#         data = json.loads(json_str)
#         logger.info("JSON parsed successfully")
        
#         # Then validate with Pydantic
#         analysis = VideoAnalysis(**data)
#         logger.info("Pydantic validation successful")
#         return analysis
        
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decode error: {e}")
#         logger.error(f"Problematic JSON: {json_str[:500]}...")
#         raise AnalysisError(f"Invalid JSON: {e}", "PARSER")
        
#     except ValidationError as e:
#         logger.error(f"Pydantic validation error: {e}")
#         logger.error(f"Data structure: {data}")
#         raise AnalysisError(f"Schema validation failed: {e}", "VALIDATION")
        
#     except Exception as e:
#         logger.error(f"Unexpected parsing error: {e}")
#         raise AnalysisError(f"Parsing failed: {e}", "PARSER")

def retryable(fn, attempts=3, delay_ms=1000):
    """Retry function with exponential backoff"""
    last_error = None
    
    for i in range(attempts):
        try:
            return fn()
        except AnalysisError as e:
            last_error = e
            if e.code == "VALIDATION":
                logger.error(f"Validation error (no retry): {e}")
                raise
            
            if i < attempts - 1:
                delay = delay_ms * (2 ** i)  # Exponential backoff
                logger.warning(f"Attempt {i+1} failed, retrying in {delay}ms: {e}")
                time.sleep(delay / 1000)
            else:
                logger.error(f"All {attempts} attempts failed")
                
        except Exception as e:
            last_error = AnalysisError(f"Unexpected error: {e}", "API")
            if i < attempts - 1:
                delay = delay_ms * (2 ** i)
                logger.warning(f"Attempt {i+1} failed, retrying in {delay}ms: {e}")
                time.sleep(delay / 1000)
    
    raise last_error or AnalysisError("Unknown failure", "API")

def get_evenly_spaced_frames(folder: Path, count: int) -> List[Path]:
    """Get evenly spaced frames from folder"""
    imgs = sorted(folder.glob("*.png"))
    total = len(imgs)
    if total == 0:
        raise AnalysisError(f"No PNG frames in {folder}", "NOT_FOUND")
    if total <= count:
        return imgs
    step = (total - 1) / (count - 1)
    return [imgs[round(i * step)] for i in range(count)]

def load_render_errors(json_path: Path) -> Dict[str, str]:
    """Load render errors from JSON file"""
    if not json_path.exists():
        return {}
    try:
        data = json.loads(json_path.read_text())
        return data.get("errors", {}) or {}
    except Exception as e:
        logger.warning(f"Could not load render errors: {e}")
        return {}

def load_frames_base64(paths: List[Path]) -> List[str]:
    """Load frames and encode as base64"""
    frames = []
    for path in paths:
        try:
            data = base64.b64encode(path.read_bytes()).decode("utf-8")
            frames.append(data)
            logger.info(f"Loaded frame: {path.name}")
        except Exception as e:
            logger.error(f"Failed to load frame {path}: {e}")
            raise AnalysisError(f"Failed to load frame {path}: {e}", "FILE_ERROR")
    return frames

# ─── Core Analysis ───────────────────────────────────────────────
def analyze_frames(frames_b64: List[str], timestamps: List[float]) -> None:
    """Call Groq API and save raw LLM response directly to a .txt file (no JSON parsing)."""
    if len(frames_b64) != len(timestamps):
        raise AnalysisError("Frames/timestamps length mismatch", "VALIDATION")

    prompt = build_analysis_prompt(timestamps)
    start = time.time()

    def request():
        logger.info(f"Making API request for {len(frames_b64)} frames...")

        try:
            resp = groq_client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please analyze these frames. Reply however you see fit."},
                            *[
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{img}"}
                                } for img in frames_b64
                            ]
                        ]
                    }
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )

            raw = resp.choices[0].message.content or ""
            logger.info(f"API response received ({len(raw)} characters)")

            # Save raw output to txt
            save_path = OUTPUT_DIR.parent / "api_raw_output.txt"
            save_path.write_text(raw, encoding="utf-8")
            logger.info(f"Raw API output saved to: {save_path}")

        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise AnalysisError(f"API request failed: {e}", "API")

    retryable(request)


# ─── API Response for UI ─────────────────────────────────────────────────
class APIResponse(BaseModel):
    """Standard API response format for UI"""
    success: bool
    data: Optional[VideoAnalysis] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: str
    processing_time_ms: int

def create_api_response(analysis: VideoAnalysis = None, error: Exception = None) -> Dict:
    """Create standardized API response"""
    response = APIResponse(
        success=analysis is not None,
        data=analysis,
        error=str(error) if error else None,
        error_code=getattr(error, 'code', None) if error else None,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        processing_time_ms=analysis.processingTime if analysis else 0
    )
    return response.dict()

# ─── Main Function ─────────────────────────────────────────────────────
def main():
    """Main function with raw output (no JSON parsing or structured objects)"""
    print(" Analyzing semantic frames from Motion Canvas...")
    
    try:
        # Load frames
        frames = get_evenly_spaced_frames(OUTPUT_DIR, FRAME_COUNT)
        print(f" Found {len(frames)} frames")
        
        # Load render errors
        errors = load_render_errors(ERROR_JSON)
        if errors:
            print(f"  Found {len(errors)} render errors")
        
        # Generate timestamps
        timestamps = [i * SCENE_DURATION / (FRAME_COUNT - 1) for i in range(FRAME_COUNT)]
        print(f" Analyzing at timestamps: {timestamps}")
        
        # Load frames as base64
        frames_b64 = load_frames_base64(frames)
        print(f" Loaded {len(frames_b64)} frames for analysis")
        
        # Analyze frames (no return, just saves raw output)
        analyze_frames(frames_b64, timestamps)
        print(f" Analysis completed and raw output saved.")

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f" Analysis failed: {e}")


if __name__ == "__main__":
    main()
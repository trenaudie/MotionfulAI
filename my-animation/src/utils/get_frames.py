# # # # # import asyncio
# # # # # from playwright.async_api import async_playwright

# # # # # async def main():
# # # # #     async with async_playwright() as p:
# # # # #         browser = await p.chromium.launch(headless=True)
# # # # #         page = await browser.new_page()
# # # # #         await page.goto("https://example.com")
# # # # #         await page.screenshot(path="example.png")
# # # # #         print(" Screenshot taken successfully at ")

# # # # #         await browser.close()

# # # # # asyncio.run(main())

# # # # import asyncio
# # # # import os
# # # # from playwright.async_api import async_playwright

# # # # async def main():
# # # #     os.makedirs("out", exist_ok=True)

# # # #     async with async_playwright() as p:
# # # #         browser = await p.chromium.launch(headless=True)
# # # #         page = await browser.new_page()
# # # #         await page.goto("https://example.com", wait_until="networkidle")

# # # #         # Screenshot full page
# # # #         path = "out/example.png"
# # # #         await page.screenshot(path=path)
# # # #         print(f"Screenshot saved to {os.path.abspath(path)}")

# # # #         await browser.close()

# # # # asyncio.run(main())

# # # import asyncio
# # # from playwright.async_api import async_playwright
# # # import os

# # # OUTPUT_DIR = "out"
# # # os.makedirs(OUTPUT_DIR, exist_ok=True)

# # # async def capture_frames():
# # #     async with async_playwright() as p:
# # #         browser = await p.chromium.launch(headless=True)
# # #         page = await browser.new_page()
# # #         await page.goto("http://localhost:9000", wait_until="networkidle")

# # #         # Wait for Motion Canvas to load
# # #         await page.wait_for_selector('canvas', timeout=10000)

# # #         # 1. Disable looping
# # #         await page.click('button[title*="Looping"]')

# # #         # 2. Click Play
# # #         await page.click('button[title*="Play"]')

# # #         # 3. Capture frames at intervals
# # #         timestamps = [0, 2, 4, 6]  # seconds
# # #         for i, t in enumerate(timestamps):
# # #             await asyncio.sleep(timestamps[i] - timestamps[i-1] if i > 0 else t)
# # #             path = os.path.join(OUTPUT_DIR, f"frame-{i}.png")
# # #             await page.screenshot(path=path, full_page=False)
# # #             print(f"📸 Saved: {path}")

# # #         await browser.close()

# # # asyncio.run(capture_frames())

# # import subprocess
# # import asyncio
# # import time
# # from playwright.async_api import async_playwright, TimeoutError
# # import os

# # VITE_DEV_PORT = 9000
# # OUTPUT_DIR = "out"
# # PROJECT_DIR = "D:/New_hackathon/my-animation/my-animation"

# # async def wait_for_server(url, timeout=15):
# #     import requests
# #     for _ in range(timeout * 2):
# #         try:
# #             requests.get(url)
# #             return True
# #         except Exception:
# #             time.sleep(0.5)
# #     return False

# # async def capture_frames():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=True)
# #         page = await browser.new_page()

# #         try:
# #             await page.goto(f"http://localhost:{VITE_DEV_PORT}", wait_until="networkidle")
# #         except TimeoutError:
# #             print("Could not connect to localhost. Is the dev server running?")
# #             return

# #         await page.wait_for_selector("canvas", timeout=15000)
# #         await page.evaluate("window.player?.disableLooping()")
# #         await page.evaluate("window.player?.play()")

# #         print("▶ Animation started. Capturing frames...")

# #         for frame_num, time_s in enumerate([0, 2.5, 5.0]):
# #             await page.evaluate(f"window.motionCanvas?.seek({time_s})")
# #             await asyncio.sleep(0.7)

# #             canvas = await page.query_selector("canvas")
# #             if canvas:
# #                 os.makedirs(OUTPUT_DIR, exist_ok=True)
# #                 await canvas.screenshot(path=f"{OUTPUT_DIR}/frame-{frame_num}.png")
# #                 print(f" Frame captured: frame-{frame_num}.png")
# #             else:
# #                 print(f" Canvas not found at time {time_s}s")

# #         await browser.close()


# # def main():
# #     # 1. Start Vite dev server
# #     print(" Starting Vite dev server...")
# #     vite_proc = subprocess.Popen(["npm", "run", "start"], cwd=PROJECT_DIR)

# #     # 2. Wait until server is ready
# #     print(" Waiting for server...")
# #     if not asyncio.run(wait_for_server(f"http://localhost:{VITE_DEV_PORT}")):
# #         print(" Dev server did not start in time.")
# #         vite_proc.kill()
# #         return

# #     # 3. Capture frames
# #     try:
# #         asyncio.run(capture_frames())
# #     finally:
# #         print(" Stopping dev server...")
# #         vite_proc.terminate()


# # if __name__ == "__main__":
# #     main()

# # import subprocess
# # import asyncio
# # import time
# # from playwright.async_api import async_playwright, TimeoutError
# # import os

# # VITE_DEV_PORT = 9000
# # OUTPUT_DIR = "out"
# # PROJECT_DIR = "D:/New_hackathon/my-animation"

# # async def wait_for_server(url, timeout=15):
# #     import requests
# #     for _ in range(timeout * 2):
# #         try:
# #             requests.get(url)
# #             return True
# #         except Exception:
# #             time.sleep(0.5)
# #     return False

# # async def capture_frames():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=True)
# #         page = await browser.new_page()

# #         try:
# #             await page.goto(f"http://localhost:{VITE_DEV_PORT}", wait_until="networkidle")
# #         except TimeoutError:
# #             print("Could not connect to localhost. Is the dev server running?")
# #             return

# #         await page.wait_for_selector("canvas", timeout=15000)
# #         await page.evaluate("window.player?.disableLooping()")
# #         await page.evaluate("window.player?.play()")

# #         print(" Animation started. Capturing frames...")

# #         for frame_num, time_s in enumerate([0, 2.5, 5.0]):
# #             await page.evaluate(f"window.motionCanvas?.seek({time_s})")
# #             await asyncio.sleep(0.7)

# #             canvas = await page.query_selector("canvas")
# #             if canvas:
# #                 os.makedirs(OUTPUT_DIR, exist_ok=True)
# #                 await canvas.screenshot(path=f"{OUTPUT_DIR}/frame-{frame_num}.png")
# #                 print(f" Frame captured: frame-{frame_num}.png")
# #             else:
# #                 print(f" Canvas not found at time {time_s}s")

# #         await browser.close()

# # def main():
# #     # Verify project directory
# #     if not os.path.exists(os.path.join(PROJECT_DIR, "package.json")):
# #         print(f"Error: No npm project found at {PROJECT_DIR}")
# #         return

# #     # 1. Start Vite dev server
# #     print(" Starting Vite dev server...")
# #     try:
# #         vite_proc = subprocess.Popen(
# #             ["cmd", "/c", "npm", "run", "dev"],  # Changed 'start' to 'dev' if that's your script name
# #             cwd=PROJECT_DIR,
# #             stdout=subprocess.PIPE,
# #             stderr=subprocess.PIPE
# #         )
# #     except FileNotFoundError:
# #         print("Error: npm command not found. Please ensure Node.js is installed and in your PATH.")
# #         return

# #     # 2. Wait until server is ready
# #     print(" Waiting for server...")
# #     if not asyncio.run(wait_for_server(f"http://localhost:{VITE_DEV_PORT}")):
# #         print(" Dev server did not start in time.")
# #         vite_proc.kill()
# #         return

# #     # 3. Capture frames
# #     try:
# #         asyncio.run(capture_frames())
# #     finally:
# #         print(" Stopping dev server...")
# #         vite_proc.terminate()

# # if __name__ == "__main__":
# #     main()

# # import subprocess
# # import asyncio
# # import time
# # import math
# # from playwright.async_api import async_playwright, TimeoutError
# # import os
# # import requests

# # VITE_DEV_PORT    = 9000
# # OUTPUT_DIR       = "out"
# # PROJECT_DIR      = "D:/New_hackathon/my-animation"
# # CAPTURE_INTERVAL = 10    # seconds between screenshots
# # MAX_CAPTURES     = 100   # safety cap if duration isn’t detectable

# # async def wait_for_server(url, timeout=15):
# #     for _ in range(timeout * 2):
# #         try:
# #             requests.get(url)
# #             return True
# #         except Exception:
# #             time.sleep(0.5)
# #     return False

# # async def capture_every_interval():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=True)
# #         page = await browser.new_page()

# #         try:
# #             await page.goto(f"http://localhost:{VITE_DEV_PORT}", wait_until="networkidle")
# #         except TimeoutError:
# #             print("Could not connect to localhost. Is the dev server running?")
# #             return

# #         await page.wait_for_selector("canvas", timeout=15000)

# #         # disable looping and seek to start
# #         await page.evaluate("window.player?.disableLooping?.()")
# #         await page.evaluate("window.player?.seek(0)")
# #         await page.evaluate("window.player?.play?.()")

# #         # try to read the total duration
# #         duration = await page.evaluate("""
# #             () => {
# #                 if (window.player && typeof window.player.duration === 'number') {
# #                     return window.player.duration;
# #                 }
# #                 if (window.motionCanvas && typeof window.motionCanvas.duration === 'number') {
# #                     return window.motionCanvas.duration;
# #                 }
# #                 return 0;
# #             }
# #         """)

# #         if duration and duration > 0:
# #             print(f"Detected animation duration: {duration:.2f}s")
# #             num_captures = math.ceil(duration / CAPTURE_INTERVAL) + 1
# #             timestamps = [i * CAPTURE_INTERVAL for i in range(num_captures)]
# #         else:
# #             print("Could not detect duration—falling back to max captures")
# #             timestamps = [i * CAPTURE_INTERVAL for i in range(MAX_CAPTURES)]

# #         os.makedirs(OUTPUT_DIR, exist_ok=True)
# #         print(f"Capturing {len(timestamps)} frames every {CAPTURE_INTERVAL}s...")

# #         for time_s in timestamps:
# #             if duration and time_s > duration:
# #                 break

# #             await page.evaluate(f"window.motionCanvas?.seek?.({time_s})")
# #             await asyncio.sleep(0.5)

# #             canvas = await page.query_selector("canvas")
# #             if not canvas:
# #                 print(f"Canvas not found at {time_s}s, skipping")
# #                 continue

# #             filename = os.path.join(OUTPUT_DIR, f"frame-{int(time_s)}.png")
# #             await canvas.screenshot(path=filename)
# #             print(f"Captured frame at {time_s}s -> {filename}")

# #         await browser.close()

# # def main():
# #     # check project folder
# #     if not os.path.exists(os.path.join(PROJECT_DIR, "package.json")):
# #         print(f"Error: No npm project found at {PROJECT_DIR}")
# #         return

# #     print("Starting Vite dev server...")
# #     try:
# #         vite_proc = subprocess.Popen(
# #             ["cmd", "/c", "npm", "run", "dev"],
# #             cwd=PROJECT_DIR,
# #             stdout=subprocess.PIPE,
# #             stderr=subprocess.PIPE
# #         )
# #     except FileNotFoundError:
# #         print("npm not found. Make sure Node.js is installed and in your PATH.")
# #         return

# #     print("Waiting for dev server to be ready...")
# #     if not asyncio.run(wait_for_server(f"http://localhost:{VITE_DEV_PORT}")):
# #         print("Dev server did not respond in time.")
# #         vite_proc.kill()
# #         return

# #     try:
# #         asyncio.run(capture_every_interval())
# #     finally:
# #         print("Shutting down dev server...")
# #         vite_proc.terminate()

# # if __name__ == "__main__":
# #     main()

# import subprocess
# import asyncio
# import time
# import math
# from playwright.async_api import async_playwright, TimeoutError
# import os
# import requests

# VITE_DEV_PORT    = 9000
# OUTPUT_DIR       = "out"
# PROJECT_DIR      = "D:/New_hackathon/my-animation"
# CAPTURE_INTERVAL = 10    # seconds between screenshots
# MAX_CAPTURES     = 100   # safety cap if duration isn’t detectable

# async def wait_for_server(url, timeout=15):
#     for _ in range(timeout * 2):
#         try:
#             requests.get(url)
#             return True
#         except Exception:
#             time.sleep(0.5)
#     return False

# async def capture_image_sequence():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         try:
#             await page.goto(f"http://localhost:{VITE_DEV_PORT}", wait_until="networkidle")
#         except TimeoutError:
#             print("Could not connect to localhost. Is the dev server running?")
#             return

#         await page.wait_for_selector("canvas", timeout=15000)

#         await page.evaluate("window.player?.disableLooping?.()")
#         await page.evaluate("window.player?.seek(0)")
#         await page.evaluate("window.player?.play?.()")

#         duration = await page.evaluate("""
#             () => {
#                 if (window.player && typeof window.player.duration === 'number') {
#                     return window.player.duration;
#                 }
#                 if (window.motionCanvas && typeof window.motionCanvas.duration === 'number') {
#                     return window.motionCanvas.duration;
#                 }
#                 return 0;
#             }
#         """)

#         if duration and duration > 0:
#             print(f"Detected animation duration: {duration:.2f} seconds")
#             timestamps = [i for i in range(0, math.ceil(duration) + 1, CAPTURE_INTERVAL)]
#         else:
#             print("Could not detect duration. Falling back to fixed frame count.")
#             timestamps = [i * CAPTURE_INTERVAL for i in range(MAX_CAPTURES)]

#         os.makedirs(OUTPUT_DIR, exist_ok=True)
#         print(f"Capturing {len(timestamps)} frames at {CAPTURE_INTERVAL}-second intervals...")

#         for time_s in timestamps:
#             if duration and time_s > duration:
#                 break

#             await page.evaluate(f"window.motionCanvas?.seek?.({time_s})")
#             await asyncio.sleep(0.5)

#             canvas = await page.query_selector("canvas")
#             if not canvas:
#                 print(f"Canvas not found at {time_s}s, skipping.")
#                 continue

#             filename = os.path.join(OUTPUT_DIR, f"frame-{int(time_s)}.png")
#             await canvas.screenshot(path=filename)
#             print(f"Captured frame at {time_s}s -> {filename}")

#         await browser.close()

# def main():
#     if not os.path.exists(os.path.join(PROJECT_DIR, "package.json")):
#         print(f"Error: No npm project found at {PROJECT_DIR}")
#         return

#     print("Starting Vite dev server...")
#     try:
#         vite_proc = subprocess.Popen(
#             ["cmd", "/c", "npm", "run", "dev"],
#             cwd=PROJECT_DIR,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )
#     except FileNotFoundError:
#         print("npm not found. Make sure Node.js is installed and in your PATH.")
#         return

#     print("Waiting for dev server to be ready...")
#     if not asyncio.run(wait_for_server(f"http://localhost:{VITE_DEV_PORT}")):
#         print("Dev server did not respond in time.")
#         vite_proc.kill()
#         return

#     try:
#         asyncio.run(capture_image_sequence())
#     finally:
#         print("Shutting down dev server...")
#         vite_proc.terminate()

# if __name__ == "__main__":
#     main()

# import asyncio
# import os
# from playwright.async_api import async_playwright, TimeoutError
# import time

# # Config
# VITE_DEV_PORT = 9000
# PROJECT_URL = f"http://localhost:{VITE_DEV_PORT}"
# OUTPUT_DIR = "out2"
# CAPTURE_INTERVAL = 1 / 30  # ~30 FPS
# MAX_TOTAL_FRAMES = 300
# IMAGE_FORMAT = "png"

# # Ensure output directory exists
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# async def capture_motion_canvas():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(device_scale_factor=2.0)
#         page = await context.new_page()

#         try:
#             print("[INFO] Opening Motion Canvas preview...")
#             await page.goto(PROJECT_URL, timeout=60000)

#             await page.wait_for_selector("canvas", timeout=30000)
#             await asyncio.sleep(2)

#             print("[INFO] Checking available buttons...")
#             buttons = await page.query_selector_all("button")
#             for idx, btn in enumerate(buttons):
#                 label = await btn.get_attribute("title")
#                 print(f"  Button {idx}: {label}")

#             print("[INFO] Attempting to disable looping...")
#             try:
#                 loop_btn = await page.wait_for_selector("button[title='Disable looping [L]']", timeout=5000)
#                 await loop_btn.click()
#                 print("[INFO] Looping disabled.")
#             except TimeoutError:
#                 print("[WARN] Looping toggle not found. Skipping.")

#             print("[INFO] Triggering animation playback via JS...")
#             await page.evaluate("""
#                 () => {
#                     const player = window.player || window.project;
#                     if (player && typeof player.play === 'function') {
#                         player.play();
#                     }
#                     window.animationComplete = false;
#                     if (player && typeof player.onFinish === 'function') {
#                         player.onFinish(() => { window.animationComplete = true; });
#                     } else {
#                         setTimeout(() => { window.animationComplete = true; }, 60000);
#                     }
#                 }
#             """)

#             print("[INFO] Capturing canvas frames...")
#             frame_index = 0

#             while True:
#                 canvas = await page.query_selector("canvas")
#                 filename = os.path.join(OUTPUT_DIR, f"frame_{frame_index:05d}.{IMAGE_FORMAT}")
#                 await canvas.screenshot(path=filename)
#                 print(f"[CAPTURED] {filename}")
#                 frame_index += 1

#                 if frame_index >= MAX_TOTAL_FRAMES:
#                     print("[WARN] Max frame limit reached. Stopping.")
#                     break

#                 is_finished = await page.evaluate("() => window.animationComplete === true")
#                 if is_finished:
#                     print("[INFO] Animation completed.")
#                     break

#                 await asyncio.sleep(CAPTURE_INTERVAL)

#         except TimeoutError:
#             print("[ERROR] Timeout while loading or interacting with the preview.")
#         finally:
#             await browser.close()

# if __name__ == "__main__":
#     asyncio.run(capture_motion_canvas())

#-----------------------------------------WORKING--------------------------------------------------------

# import asyncio
# import os
# from playwright.async_api import async_playwright, TimeoutError
# import time

# # Config
# VITE_DEV_PORT = 9000
# PROJECT_URL = f"http://localhost:{VITE_DEV_PORT}"
# OUTPUT_DIR = "out2"
# CAPTURE_INTERVAL = 1 / 30  # ~30 FPS
# MAX_TOTAL_FRAMES = 5000
# IMAGE_FORMAT = "png"
# IDLE_FRAME_THRESHOLD = 30  # stop after this many identical frames

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# async def capture_motion_canvas():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context(device_scale_factor=2.0)
#         page = await context.new_page()

#         try:
#             print("[INFO] Opening Motion Canvas preview...")
#             await page.goto(PROJECT_URL, timeout=60000)
#             await page.wait_for_selector("canvas", timeout=30000)
#             await asyncio.sleep(2)

#             print("[INFO] Disabling loop if enabled...")
#             try:
#                 await page.click("button[title='Disable looping [L]']", timeout=3000)
#                 print("[INFO] Looping disabled.")
#             except:
#                 print("[WARN] Loop button not found. Skipping.")

#             print("[INFO] Clicking Play button...")
#             try:
#                 await page.click("button[title='Play [Space]']", timeout=5000)
#                 print("[INFO] Play clicked.")
#             except TimeoutError:
#                 print("[ERROR] Play button not found. Exiting.")
#                 return

#             print("[INFO] Capturing frames from canvas...")
#             frame_index = 0
#             identical_count = 0
#             last_frame = None

#             while frame_index < MAX_TOTAL_FRAMES:
#                 canvas = await page.query_selector("canvas")
#                 buffer = await canvas.screenshot(type=IMAGE_FORMAT)

#                 filename = os.path.join(OUTPUT_DIR, f"frame_{frame_index:05d}.{IMAGE_FORMAT}")
#                 with open(filename, "wb") as f:
#                     f.write(buffer)
#                 print(f"[CAPTURED] {filename}")

#                 # Check if frame is identical to previous
#                 if last_frame == buffer:
#                     identical_count += 1
#                 else:
#                     identical_count = 0
#                     last_frame = buffer

#                 if identical_count >= IDLE_FRAME_THRESHOLD:
#                     print("[INFO] Animation appears to be finished.")
#                     break

#                 frame_index += 1
#                 await asyncio.sleep(CAPTURE_INTERVAL)

#         except TimeoutError:
#             print("[ERROR] Timeout while loading or interacting with the preview.")
#         finally:
#             await browser.close()

# if __name__ == "__main__":
#     asyncio.run(capture_motion_canvas())

import asyncio
import os
import json
from playwright.async_api import async_playwright, TimeoutError
import time

# Config
VITE_DEV_PORT = 9000
PROJECT_URL = f"http://localhost:{VITE_DEV_PORT}"
OUTPUT_DIR = "my-animation\\out2"
OUTPUT_LOG_JSON = "my-animation\\out2_json"
CAPTURE_INTERVAL = 1 / 30  # ~30 FPS
MAX_TOTAL_FRAMES = 5000
IMAGE_FORMAT = "png"
IDLE_FRAME_THRESHOLD = 30  # stop after this many identical frames

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def capture_motion_canvas():
    result = {
        "status": "failed",
        "error": None,
        "framesCaptured": 0,
        "startTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": None
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2.0)
        page = await context.new_page()

        try:
            print("[INFO] Opening Motion Canvas preview...")
            await page.goto(PROJECT_URL, timeout=60000)
            await page.wait_for_selector("canvas", timeout=30000)
            await asyncio.sleep(2)

            print("[INFO] Disabling loop if enabled...")
            try:
                await page.click("button[title='Disable looping [L]']", timeout=3000)
                print("[INFO] Looping disabled.")
            except:
                print("[WARN] Loop button not found. Skipping.")

            print("[INFO] Clicking Play button...")
            try:
                await page.click("button[title='Play [Space]']", timeout=5000)
                print("[INFO] Play clicked.")
            except TimeoutError as e:
                error_msg = "Play button not found. Exiting."
                print(f"[ERROR] {error_msg}")
                result["error"] = error_msg
                return result

            print("[INFO] Capturing frames from canvas...")
            frame_index = 0
            identical_count = 0
            last_frame = None

            while frame_index < MAX_TOTAL_FRAMES:
                canvas = await page.query_selector("canvas")
                buffer = await canvas.screenshot(type=IMAGE_FORMAT)

                filename = os.path.join(OUTPUT_DIR, f"frame_{frame_index:05d}.{IMAGE_FORMAT}")
                with open(filename, "wb") as f:
                    f.write(buffer)
                print(f"[CAPTURED] {filename}")

                # Check if frame is identical to previous
                if last_frame == buffer:
                    identical_count += 1
                else:
                    identical_count = 0
                    last_frame = buffer

                frame_index += 1

                if identical_count >= IDLE_FRAME_THRESHOLD:
                    print("[INFO] Animation appears to be finished.")
                    break

                await asyncio.sleep(CAPTURE_INTERVAL)

            result["status"] = "success"
            result["framesCaptured"] = frame_index

        except TimeoutError as e:
            error_msg = "Timeout while loading or interacting with the preview."
            print(f"[ERROR] {error_msg}")
            result["error"] = error_msg
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            result["error"] = str(e)
        finally:
            await browser.close()
            result["endTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(OUTPUT_LOG_JSON, "w") as f:
                json.dump(result, f, indent=2)
            print(f"[INFO] Results written to {OUTPUT_LOG_JSON}")

if __name__ == "__main__":
    asyncio.run(capture_motion_canvas())

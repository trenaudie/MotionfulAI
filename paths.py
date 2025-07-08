import re
from pathlib import Path

AGENTS_PROMPTS_DIR = Path(__file__).parent / 'agents' / 'prompts'
SCENES_DIR = Path(__file__).parent / 'frontend' / 'src' / 'scenes'

def get_next_scene_filepath() -> Path:
    numbered_files = []
    pattern = re.compile(r"^(\d+)_scene\.tsx$")

    for file in SCENES_DIR.glob("*.tsx"):
        match = pattern.match(file.name)
        if match:
            numbered_files.append(int(match.group(1)))

    if not numbered_files:
        next_number = 1
    else:
        next_number = max(numbered_files) + 1

    return SCENES_DIR / f"{next_number:02d}_scene.tsx"

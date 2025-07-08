#%%
from fileinput import filename
from agents.coder_general_agent import CoderGeneralAgent
from agents.verify_update_agent import VerifyUpdateAgent
from pathlib import Path
from typing import List, Dict

coderagent = CoderGeneralAgent()
filepath, status = coderagent.generate_code('create a bouncing circle animation using motion-canvas')
# Define symbolic example list (from frontend/src/scenes2)

verify_update_agent = VerifyUpdateAgent()



# old_Examples_dir = "/Users/tanguy.renaudie/motion_canvas_projects/lablab_hack/frontend/src/motion_canvas_examples"
# new_examples_dir = "/Users/tanguy.renaudie/motion_canvas_projects/lablab_hack/frontend/src/extra_examples"
# # copy all files from old_Examples_dir to new_examples_dir
# import os, shutil
# for file in os.listdir(old_Examples_dir):
#     filepath = Path(old_Examples_dir) / file
#     if filepath.is_file() and filepath.suffix == ".tsx" and not (Path(new_examples_dir) / filepath.name).exists():
#         print(f"copying {filepath} to {new_examples_dir}")
#         shutil.copy(os.path.join(old_Examples_dir, file), os.path.join(new_examples_dir, file))
# #%% 

import openai

# %%
system_prompt = build_system_prompt(coderagent.yaml_template, [Path(EXTRA_EXAMPLES_DIR)])
# %%
print(system_prompt)

# %%


EXTRA_EXAMPLES_DIR = "/Users/tanguy.renaudie/motion_canvas_projects/lablab_hack/frontend/src/extra_examples"
from agents.agents import Agent
from pathlib import Path
from typing import List, Dict
import os
from paths import AGENTS_PROMPTS_DIR
from utils import build_model_from_structure
import yaml
from ai_utils.openai import chat_completion_structured, OpenAIModels
yaml_data = yaml.safe_load(open("agents/prompts/coder_general_01.yaml"))
output_template_str = yaml_data["output_template"]
output_template_dict = yaml.safe_load(output_template_str)
DynamicResponseModel = build_model_from_structure("MotionCanvasResponse", output_template_dict)


def build_system_prompt_coder_general(agent_config: dict, extra_example_dirs: List[Path] = None) -> str:
    system_base = agent_config.get("system_prompt", "")
    output_template = agent_config.get("output_template", "")
    examples = agent_config.get("examples", [])

    # add examples from files
    if extra_example_dirs:
        extra_examples = load_additional_examples_from_files(
            directories=extra_example_dirs,
            exclude_prefixes=["tweening"],
        )
        examples += extra_examples

    formatted_examples = "\n\n".join(
        f"INPUT: {ex['input']}\nOUTPUT:\n{ex['output']}" for ex in examples
    )

    system_prompt = (
        f"{system_base.strip()}\n\n"
        f"EXAMPLES:\n{formatted_examples}\n\n"
        f"OUTPUT TEMPLATE:\n{output_template.strip()}"
    )

    return system_prompt

def load_additional_examples_from_files(
    directories: List[Path],
    exclude_prefixes: List[str] = [],
) -> List[Dict[str, str]]:
    examples = []
    for directory in directories:
        for path in directory.glob("*.tsx"):
            if any(path.name.startswith(prefix) for prefix in exclude_prefixes):
                continue
            content = path.read_text()
            examples.append({
                "input": f"From file: {path.name}",
                "output": f"Reasoning: | \n... \nOutput: \ncode: |\n```typescript\n{content}\n```"
            })
    return examples



class CoderGeneralAgent(Agent):
    def __init__(self):
        super().__init__('coder_general_01', os.path.join(AGENTS_PROMPTS_DIR, 'coder_general_01.yaml'))
        
    def generate_code(self, prompt : str, dummy : bool = False):
        if dummy:
            return "dummy.tsx", "success"
        system_prompt = build_system_prompt_coder_general(self.yaml_template, [Path(EXTRA_EXAMPLES_DIR)])
        print(f'system_prompt: {system_prompt[:500]}')
        output = chat_completion_structured(OpenAIModels.GPT_4_1_NANO, system_prompt, prompt, DynamicResponseModel)
        code = output.Output.code
        reasoning = output.Reasoning
        return code, reasoning


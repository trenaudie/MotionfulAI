from pydantic import create_model, BaseModel
from typing import Dict, Any, Type
import re
from typing import Optional


def build_model_from_structure(name: str, structure: dict) -> Type[BaseModel]:
    fields = {}
    for key, value in structure.items():
        if isinstance(value, dict):
            # Recursively create a submodel
            submodel = build_model_from_structure(f"{name}_{key}", value)
            fields[key] = (submodel, ...)
        else:
            fields[key] = (str, ...)  # Treat leaf nodes as strings for now
    return create_model(name, **fields)



def parse_markdown_output(markdown: str) -> Optional[str]:
    """
    Extracts the content of the first triple-backtick code block from a Markdown string.

    Returns the code as a string, or None if no block is found.
    """
    match = re.search(r"```(?:\w+)?\n(.*?)```", markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

from pydantic import create_model, BaseModel
from typing import Dict, Any, Type

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

\
# %%

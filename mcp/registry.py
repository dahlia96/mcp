from typing import Callable, Type, Dict, Any, Optional
from pydantic import BaseModel
from mcp import types as mcp_types

REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_tool(
    *,
    name: str,
    description: str,
    input_schema: Type[BaseModel],
    output_schema: Optional[Type[BaseModel]] = None,
):
    """
    Decorator to register a tool with its schemas and handler.
    Usage:
      @register_tool(name="tool@v1", description="...", input_schema=MyInput, output_schema=MyOutput)
      def handler(args: MyInput): ...
    """
    def decorator(fn: Callable[[BaseModel], Any]):
        REGISTRY[name] = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "handler": fn,
        }
        return fn
    return decorator

def to_mcp_tool(spec: Dict[str, Any]) -> mcp_types.Tool:
    return mcp_types.Tool(
        name=spec["name"],
        description=spec["description"],
        inputSchema=spec["input_schema"].model_json_schema(),
        outputSchema=(
            spec["output_schema"].model_json_schema()
            if spec["output_schema"] is not None
            else {"type": "object"}
        ),
    )

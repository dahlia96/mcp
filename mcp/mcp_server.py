from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from mcp.registry import REGISTRY, to_mcp_tool

def build_server():
    app = Server("felix-tools")

    @app.list_tools()
    async def list_mcp_tools():
        # Dynamically convert all registered tools into MCP Tools
        return [to_mcp_tool(spec) for spec in REGISTRY.values()]

    @app.call_tool()
    async def call_tool(name, arguments):
        # Look up the tool in the registry
        if name not in REGISTRY:
            return [mcp_types.JsonContent(type="json", json={"ok": False, "error": f"Unknown tool: {name}"})]
        
        tool_spec = REGISTRY[name]
        input_schema = tool_spec["input_schema"]
        output_schema = tool_spec["output_schema"]
        handler = tool_spec["handler"]
        
        try:
            # Validate input arguments
            args_model = input_schema(**arguments)
            # Call the handler
            result = handler(args_model)
            
            # Validate output against schema if one is defined
            if output_schema:
                validated_output = output_schema(**result)
                result = validated_output.model_dump()
            
            return [mcp_types.JsonContent(type="json", json=result)]
        except Exception as e:
            return [mcp_types.JsonContent(type="json", json={"ok": False, "error": str(e)})]

import json
from app.services.ai_tools import add_to_cart, get_current_offers


class ToolRegistry:
    def __init__(self):
        # Map the string name from the LLM JSON to the actual Python function
        self.registry = {
            "add_to_cart": add_to_cart,
            "get_current_offers": get_current_offers,
        }

    async def execute(self, tool_call, cart_state):
        """Validates and executes the requested tool."""
        name = tool_call.get("name")
        args_str = tool_call.get("arguments", "{}")

        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON arguments provided by LLM."}

        func = self.registry.get(name)
        if not func:
            return {"error": f"Tool '{name}' not found in registry."}

        # Execute the matched function
        if name == "add_to_cart":
            return func(cart_state, args.get("item_id"), args.get("modifiers"))
        elif name == "get_current_offers":
            return func()

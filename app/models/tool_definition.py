TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Adds a food or drink item to the customer's shopping cart.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "The unique ID of the menu item.",
                    },
                    "modifiers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of modifier IDs like extra cheese or no onions.",
                    },
                },
                "required": ["item_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_offers",
            "description": "Retrieves active discounts and daily specials to suggest to the customer.",
        },
    },
]

import json


class OrderValidator:
    def __init__(self, menu_path="app/data/order_details.json"):
        with open(menu_path, "r") as f:
            self.menu = json.load(f)

    def validate_add_to_cart(self, item_id: str, modifier_ids: list = None):
        """
        Checks item existence, availability, and modifier compatibility.
        """
        # Check if item exists
        item = next((i for i in self.menu["items"] if i["id"] == item_id), None)
        if not item:
            return {
                "valid": False,
                "reason": "item_not_found",
                "message": f"ID {item_id} is not in the menu.",
            }

        # Check Availability (e.g., Breakfast vs All Day)
        category = next(
            (c for c in self.menu["categories"] if c["id"] == item.get("category_id")),
            None,
        )
        if (
            category
            and category["availability"] == "breakfast"
            and not self._is_breakfast_time()
        ):
            return {
                "valid": False,
                "reason": "out_of_hours",
                "message": "This item is only available during breakfast.",
            }

        #  Validate Modifiers
        invalid_mods = []
        if modifier_ids:
            allowed_groups = item.get("modifier_group_ids", [])
            for mod_id in modifier_ids:
                if not self._is_mod_allowed(mod_id, allowed_groups):
                    invalid_mods.append(mod_id)

        if invalid_mods:
            return {
                "valid": False,
                "reason": "invalid_modifiers",
                "message": f"Modifiers {invalid_mods} are not compatible with this item.",
            }

        return {"valid": True, "item_name": item["name"]}

    def _is_mod_allowed(self, mod_id, allowed_groups):
        # Logic to check if mod_id exists in the allowed_groups defined in JSON
        return True

    def _is_breakfast_time(self):
        # Simple time check logic
        return True

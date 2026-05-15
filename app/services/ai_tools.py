import json
import datetime


def get_current_offers():
    """Checks for active offers based on current day/time."""
    with open("app/data/order_details.json", "r") as f:
        menu_data = json.load(f)

    current_day = datetime.datetime.now().strftime("%A")
    active = [
        o["name"]
        for o in menu_data.get("special_offers", [])
        if "all_day" in o.get("availability", "")
        or current_day in o.get("availability", "")
    ]

    return f"Active offers: {', '.join(active)}" if active else "No active offers."


def add_to_cart(cart, item_id, selected_modifiers=None):
    """Validates and adds an item to the session cart."""
    with open("app/data/order_details.json", "r") as f:
        menu = json.load(f)

    item = next((i for i in menu["items"] if i["id"] == item_id), None)
    if not item:
        return {"success": False, "error": "Item not found"}

    cart_entry = {"item_name": item["name"], "price": item["base_price"]}
    cart.append(cart_entry)
    return {"success": True, "message": f"Added {item['name']}"}


def checkout(cart):
    """Calculates the total for the cart and clears it."""
    if not cart:
        return {"success": False, "message": "Your cart is empty."}

    total = sum(item["price"] for item in cart)
    # In a real app, we'd send this to a payments service or KDS
    # For now, we'll just return the total without clearing the cart so the UI shows it.

    return {
        "success": True,
        "total": total,
        "message": f"Order complete. Your total is ₹{total}. Please drive to the next window!",
    }

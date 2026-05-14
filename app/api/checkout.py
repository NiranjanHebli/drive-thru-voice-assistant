from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def process_checkout():
    return {"status": "checkout initiated"}


@router.post("/checkout")
async def checkout(cart_data: list):
    """Calculates final total including tax and packaging[cite: 1]."""
    optimized = optimize_cart(cart_data)
    subtotal = sum(item["price"] for item in optimized)
    tax = subtotal * 0.05
    total = subtotal + tax + 15  # 15 is packaging charge

    return {
        "total": round(total, 2),
        "script": f"Your total is ₹{round(total)}. Please pull forward.",
    }


@router.post("/offers")
async def fetch_offers():
    return {"message": get_current_offers()}


@router.post("/cart/add")
async def add_to_cart_endpoint(item_id: str, selected_modifiers: list = None):
    cart = get_current_cart()
    return add_to_cart(cart, item_id, selected_modifiers)

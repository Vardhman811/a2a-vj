from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent

# 🥕 Inventory of vegetables
inventory = {
    "carrot": {"price": 30, "stock": 15},
    "potato": {"price": 25, "stock": 20},
    "onion": {"price": 35, "stock": 12}
}

# ✅ Tool: Show available vegetables
def show_vegetables() -> str:
    """List available vegetables with their prices."""
    return ", ".join([f"{veg.capitalize()}: ₹{data['price']}" for veg, data in inventory.items()])

# ✅ Tool: Buy a vegetable
def buy_vegetable(vegetable: str, quantity: int) -> str:
    """Buy a vegetable from the inventory."""
    if vegetable not in inventory:
        return f"Sorry, {vegetable} is not available."
    if inventory[vegetable]["stock"] < quantity:
        return f"Sorry, we only have {inventory[vegetable]['stock']} {vegetable}(s) in stock."
    inventory[vegetable]["stock"] -= quantity
    total = inventory[vegetable]["price"] * quantity
    return f"You have bought {quantity} {vegetable}(s) for ₹{total}."

# ✅ Root ADK Agent
root_agent = Agent(
    name="vegetable_seller_agent",
    description="A vegetable seller who sells vegetables to customers",
    model="gemini-2.0-flash",
    instruction="""You can ask me what vegetables are available or buy vegetables like carrots, potatoes, and onions. You can also ask me to show the inventory. Output should be in markdown format with bullets if needed. 
- If the user asks for a vegetable that is not available, say that it is not available.
- If the user asks for a vegetable that is available, say that it is available and the price.
- If the user asks for the inventory, show the inventory.
- If the user asks to buy a vegetable, say that you will buy the vegetable and the price.
- If the user asks to buy a vegetable with a quantity, say that you will buy the vegetable and the price.
- If the user asks to buy a vegetable with a quantity that is not available, say that only that much is available.
- Use LLM to respond to other questions that are not handled by tools.
""",
    tools=[show_vegetables, buy_vegetable],
)

# Expose the agent via A2A
from google.adk.a2a.utils.agent_to_a2a import to_a2a

a2a_app = to_a2a(root_agent, port=8001)


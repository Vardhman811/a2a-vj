from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent

# 🥝 Inventory of fruits
inventory = {
    "apple": {"price": 20, "stock": 10},
    "banana": {"price": 10, "stock": 10},
    "orange": {"price": 15, "stock": 10}
}


# ✅ Tool: Show available fruits
def show_fruits() -> str:
    """List available fruits with their prices."""
    return ",".join([f"{fruit.capitalize()}: ₹{data['price']}" for fruit, data in inventory.items()])

# ✅ Tool: Buy a fruit
def buy_fruit(fruit: str, quantity: int) -> str:
    """Buy a fruit from the inventory."""
    if fruit not in inventory:
        return f"Sorry, {fruit} is not available."
    if inventory[fruit]["stock"] < quantity:
        return f"Sorry, we only have {inventory[fruit]['stock']} {fruit} in stock."
    inventory[fruit]["stock"] -= quantity
    return f"You have bought {quantity} {fruit} for ₹{inventory[fruit]['price'] * quantity}."

# ✅ Root ADK Agent
root_agent = Agent(
    name="fruit_seller_agent",
    description="A fruit seller who sells fruits to customers",
    model="gemini-2.0-flash",
    instruction="""You can ask me what fruits are available or buy fruits like apples, bananas, and oranges. You can also ask me to show the inventory. Output should be in markdown format with bullets if needed. 
            - If the user asks for a fruit that is not available, say that it is not available.
            - If the user asks for a fruit that is available, say that it is available and the price.
            - If the user asks for the inventory, show the inventory.
            - If the user asks to buy a fruit, say that you will buy the fruit and the price.
            - If the user asks to buy a fruit with a quantity, say that you will buy the fruit and the price.
            - If the user asks to buy a fruit with a quantity that is not available, say that you will buy the fruit and the price.
            - Use LLM to respond to the user's question that are not in the tools.
            """,
    tools=[show_fruits, buy_fruit],
)

# Expose the agent via A2A
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Make your agent A2A-compatible and expose it
a2a_app = to_a2a(root_agent, port=8002)

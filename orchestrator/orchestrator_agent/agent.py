from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
import os

# Load environment variables (Optional, if you are using environment variables)
from dotenv import load_dotenv
load_dotenv()


# Remote agents (Fruit Seller and Vegetable Seller)
fruit_agent = RemoteA2aAgent(
    name="fruit_agent",
    description="Agent that handles fruit sales.",
    agent_card=f"http://127.0.0.1:8001/{AGENT_CARD_WELL_KNOWN_PATH}",
)

vegetable_agent = RemoteA2aAgent(
    name="vegetable_agent",
    description="Agent that handles vegetable sales.",
    agent_card=f"http://127.0.0.1:8002/{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Orchestrator Agent that delegates tasks
root_agent = Agent(
    model="gemini-2.0-flash",
    name="orchestrator_agent",
    description="Orchestrates between Fruit and Vegetable Seller Agents.",
    instruction="""
    You are an orchestrator that can handle fruit and vegetable sales. 
    - If the user asks for fruits, delegate to the fruit_agent.
    - If the user asks for vegetables, delegate to the vegetable_agent.
    - If the user asks to buy a fruit, delegate to the fruit_agent.
    - If the user asks to buy a vegetable, delegate to the vegetable_agent.
    - If the user asks for both, first handle fruits, then vegetables.
    """,
    global_instruction="You are a sales orchestrator that communicates with fruit and vegetable agents.",
    sub_agents=[fruit_agent, vegetable_agent],  # Includes both remote agents
)

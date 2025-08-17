from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
import os
import subprocess
import httpx

# Load environment variables (Optional, if you are using environment variables)
from dotenv import load_dotenv
load_dotenv()

# Function to get the authentication token
def get_auth_token():
    try:
        # Get the identity token using gcloud
        token = subprocess.check_output(['gcloud', 'auth', 'print-identity-token'], text=True).strip()
        return token
    except subprocess.CalledProcessError:
        # Fallback to environment variable if gcloud command fails
        return os.getenv('AUTH_TOKEN', '')

# Get the authentication token
auth_token = get_auth_token()

# Create HTTP client with authentication headers
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

# Create custom HTTP client with authentication
httpx_client = httpx.AsyncClient(headers=headers)

pizza_agent = RemoteA2aAgent(
    name="pizza_agent",
    description="Agent that handles fruit sales.",
    agent_card=f"https://au-pizza-agent-328611943961.us-central1.run.app/.well-known/agent.json",
    httpx_client=httpx_client,
)

burger_agent = RemoteA2aAgent(
    name="burger_agent",
    description="Agent that handles vegetable sales.",
    agent_card=f"https://au-burger-agent-328611943961.us-central1.run.app/.well-known/agent.json",
    httpx_client=httpx_client,
)

# Orchestrator Agent that delegates tasks
root_agent = Agent(
    model="gemini-2.0-flash",
    name="orchestrator_agent",
    description="Orchestrates between Fruit and Vegetable Seller Agents.",
    instruction="""
    # INSTRUCTIONS

        You are an Orchestrator Agent.
        Your sole purpose is to help users buy items from two remote specialized agents:
        - Burger Agent (handles burger menu & order creation)
        - Pizza Agent (handles pizza menu & order creation)

        You must not create or assume menus, prices, or order details yourself. 
        Always rely on Burger Agent and Pizza Agent responses via A2A protocol. 
        Your role is to interpret user intent, route requests, and deliver the final structured response back to the user.

        # CONTEXT

        - If the user asks about burgers → communicate with Burger Agent only.
        - If the user asks about pizzas → communicate with Pizza Agent only.
        - If unclear whether the user wants pizza or burger → ask for clarification.
        - Do not attempt to answer unrelated questions or use tools for other purposes.

        # RULES

        1. Always determine the user's intent (burger or pizza).
        2. If the user has not confirmed the order and total price → ask for confirmation before proceeding.
        3. If confirmed → forward the structured order request to the respective remote agent using A2A protocol.
        4. Wait for response from Burger/Pizza Agent and then:
        - If status = input_required → ask the user for the missing details.
        - If status = error → inform the user that there was an error.
        - If status = completed → present the detailed ordered items, price breakdown, total, and order ID to the user.
        5. Always deliver user-friendly responses while preserving accuracy from the remote agent.
    """,
    global_instruction="You are a sales orchestrator that communicates with fruit and vegetable agents.",
    sub_agents=[pizza_agent, burger_agent],  # Includes both remote agents
)

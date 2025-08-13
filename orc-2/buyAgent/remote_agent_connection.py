from typing import Callable
import httpx
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse,
    Task,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)
from google.auth import default
import httpx

TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]


class RemoteAgentConnections:
    """A class to hold the connections to the remote agents."""

    def __init__(self, agent_card: AgentCard, agent_url: str):
        print(f"agent_card: {agent_card}")
        print(f"agent_url: {agent_url}")
        
        # Use Google Cloud authentication for service-to-service calls
        credentials, _ = default()
        
        # Create httpx client with authentication headers
        headers = {}
        if credentials:
            from google.auth.transport.requests import Request
            auth_req = Request()
            credentials.refresh(auth_req)
            headers = {"Authorization": f"Bearer {credentials.token}"}
        
        self._httpx_client = httpx.AsyncClient(timeout=30, headers=headers)
        self.agent_client = A2AClient(self._httpx_client, agent_card, url=agent_url)
        self.card = agent_card

    def get_agent(self) -> AgentCard:
        return self.card

    async def send_message(
        self, message_request: SendMessageRequest
    ) -> SendMessageResponse:
        return await self.agent_client.send_message(message_request)

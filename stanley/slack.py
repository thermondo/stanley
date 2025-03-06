from asyncio import Future

from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

from stanley.settings import SLACK_API_TOKEN

slack_client = WebClient(SLACK_API_TOKEN, timeout=30)


def get_team_members() -> list[tuple]:
    """Return user list in format (USER_ID, USER_NAME)."""
    members = slack_client.api_call("users.list").get("members")
    if members:
        return [(member.get("id"), member.get("name")) for member in members]
    else:
        return []


def send_slack_message(channel: str, message: str) -> Future | SlackResponse:
    response = slack_client.chat_postMessage(
        channel=channel,
        text=message,
        as_user=True,
    )
    return response

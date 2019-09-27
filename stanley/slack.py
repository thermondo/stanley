from asyncio import Future
from typing import List, Union

import slack  # type: ignore
from slack.web.slack_response import SlackResponse  # type: ignore

from stanley.settings import SLACK_API_TOKEN

slack_client = slack.WebClient(SLACK_API_TOKEN, timeout=30)


def get_team_members() -> List[tuple]:
    """Return user list in format (USER_ID, USER_NAME)."""
    members = slack_client.api_call('users.list').get('members')
    return [(member.get('id'), member.get('name')) for member in members]


def send_slack_message(channel: str, message: str) -> Union[Future, SlackResponse]:
    response = slack_client.chat_postMessage(
        channel=channel,
        text=message,
        as_user=True,
    )
    return response

import os

from slackclient import SlackClient

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']


def slack_api():
    return SlackClient(SLACK_API_TOKEN)


def get_team_members():
    """Return user list in format (USER_ID, USER_NAME)."""
    sc = slack_api()
    members = sc.api_call('users.list').get('members')
    return [(member.get('id'), member.get('name')) for member in members]


def send_slack_message(channel, message):
    sc = slack_api()
    response = sc.api_call(
        'chat.postMessage',
        channel=channel,
        text=message,
        as_user=True,
    )
    return response

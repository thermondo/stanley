import os
from slackclient import SlackClient

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
FEEDBACK_BOT_NAME = os.environ.get('FEEDBACK_BOT_NAME', 'dad')


def slack_api():
    return SlackClient(SLACK_API_TOKEN)


def get_team_members():
    """Returns user list in format (USER_ID, USER_NAME)."""
    sc = slack_api()
    members = sc.api_call('users.list').get('members')
    return [(member.get('id'), member.get('name')) for member in members]


def send_slack_message(channel, message):
    sc = slack_api()
    return sc.api_call(
        'chat.postMessage',
        channel=channel,
        text=message,
        username=FEEDBACK_BOT_NAME
    )

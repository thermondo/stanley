from unittest.mock import patch, call

from stanley.slack import get_team_members, send_slack_message


def test_get_team_members(slack_api_call_mock):
    members = get_team_members()

    assert isinstance(members, list)
    assert isinstance(members[0], tuple)


def test_send_slack_message(slack_api_call_mock):
    channel = 'random'
    message = 'I am a test an I know it'
    expected_call = call(as_user=True, channel=channel, text=message)

    with patch('stanley.slack.slack.WebClient.chat_postMessage') as post_message_mock:
        send_slack_message(channel, message)

    assert post_message_mock.called
    assert post_message_mock.call_args == expected_call

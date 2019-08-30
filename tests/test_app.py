from unittest.mock import patch

from stanley.app import app, request_feedback_command, team_command


def test_team_command(slack_api_call_mock):
    runner = app.test_cli_runner()
    result = runner.invoke(team_command)

    assert result.exit_code == 0
    assert "('USLACKBOT', 'slackbot')" in result.output
    assert "('UANA', 'ana.gomes')" in result.output
    assert "('UAMUREKI', 'amureki')" in result.output
    assert "('USEBASTIAN', 'sebastiankapunkt')" in result.output


def test_send_slack_message(slack_api_call_mock):
    runner = app.test_cli_runner()

    with patch('stanley.app.request_feedback') as request_feedback_mock:
        result = runner.invoke(request_feedback_command)

    assert result.exit_code == 0
    assert request_feedback_mock.called

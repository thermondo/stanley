from unittest.mock import patch

from stanley.app import app, request_feedback_command, team_command


def test_team_command(slack_api_call_mock):
    runner = app.test_cli_runner()
    result = runner.invoke(team_command)

    assert result.exit_code == 0
    assert "('U03H6N5JZ', 'anne')" in result.output
    assert "('U01FECGP57X', 'ayyoub.maknassa')" in result.output
    assert "('U0PES7Z6J', 'amureki')" in result.output
    assert "('U029MJK62', 'syphar')" in result.output


def test_send_slack_message(slack_api_call_mock):
    runner = app.test_cli_runner()

    with patch("stanley.app.request_feedback") as request_feedback_mock:
        result = runner.invoke(request_feedback_command)

    assert result.exit_code == 0
    assert request_feedback_mock.called

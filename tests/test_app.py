import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from stanley.app import team_command, request_feedback_command


@pytest.fixture
def flask_app(monkeypatch):
    envs = {
        'FLASK_APP': 'stanley/app.py',
    }
    monkeypatch.setattr(os, 'environ', envs)


def test_team_command(slack_api_call_mock, flask_app):
    runner = CliRunner()
    result = runner.invoke(team_command)

    assert result.exit_code == 0
    assert "('USLACKBOT', 'slackbot')" in result.output
    assert "('UANA', 'ana.gomes')" in result.output
    assert "('UAMUREKI', 'amureki')" in result.output
    assert "('USEBASTIAN', 'sebastiankapunkt')" in result.output


def test_send_slack_message(slack_api_call_mock, flask_app):
    runner = CliRunner()

    with patch('stanley.app.request_feedback') as request_feedback_mock:
        result = runner.invoke(request_feedback_command)

    assert result.exit_code == 0
    assert request_feedback_mock.called

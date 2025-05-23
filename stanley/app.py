import click
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from stanley.helpers import request_feedback
from stanley.settings import SENTRY_DSN
from stanley.slack import get_team_members

sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FlaskIntegration()])

app = Flask(__name__)

import stanley.routes  # noqa: E402, F401


@app.cli.command()
def request_feedback_command() -> None:
    request_feedback()


@app.cli.command()
def team_command() -> None:
    members = get_team_members()
    for member in members:
        click.echo(member)

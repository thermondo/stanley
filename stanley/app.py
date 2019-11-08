import click
from flask import Flask
from raven.contrib.flask import Sentry

from stanley.helpers import request_feedback
from stanley.settings import SENTRY_DSN
from stanley.slack import get_team_members

app = Flask(__name__)
sentry = Sentry(app, dsn=SENTRY_DSN)

import stanley.routes  # NoQA # isort:skip # pylint: disable=unused-import
assert stanley.routes  # nosec


@app.cli.command()
def request_feedback_command() -> None:
    request_feedback()


@app.cli.command()
def team_command() -> None:
    members = get_team_members()
    for member in members:
        click.echo(member)

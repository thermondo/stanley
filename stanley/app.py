import click
import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryIntegration

from stanley.helpers import request_feedback
from stanley.settings import SENTRY_DSN
from stanley.slack import get_team_members

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[SentryIntegration()]
)

app = FastAPI()

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

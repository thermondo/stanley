from flask import Flask
from raven.contrib.flask import Sentry

from stanley.helpers import request_feedback
from stanley.settings import SENTRY_DSN

app = Flask(__name__)
sentry = Sentry(app, dsn=SENTRY_DSN)

import stanley.routes  # NoQA # isort:skip # pylint: disable=unused-import


@app.cli.command()
def request_feedback_command():
    request_feedback()

import os
from flask import Flask
from slackclient import SlackClient

SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']

app = Flask(__name__)


@app.route("/")
def hello():
    sc = SlackClient(SLACK_API_TOKEN)

    sc.api_call(
        "chat.postMessage",
        channel="@amureki",
        text="Hello from Python! :tada:"
    )
    return "Hello World!"

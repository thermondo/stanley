import json
import os
import secrets

from flask import Flask, jsonify, request

from slack import send_slack_message, get_team_members

SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']

app = Flask(__name__)

# should be user name:
# sc.api_call("users.list").get('members')[X].get('profile').get('name')
TEAM_MEMBERS = ['amureki']


@app.route('/')
def hello():
    return 'Hello World! Please, use `/ask` to ask for a feedback', 200


@app.route('/team')
def team():
    members = get_team_members()
    return jsonify(members), 200


@app.route('/ask')
def ask():
    random_user = secrets.choice(TEAM_MEMBERS)
    send_slack_message('@{}'.format(random_user), message='hey')
    return 'Hello World!', 200


@app.route('/forward-feedback', methods=['POST'])
def forward_feedback():
    data = json.loads(request.data)
    challenge = data.get('challenge')
    if challenge:
        return challenge, 200
    receiver = TEAM_MEMBERS[0]
    token = data.get('token')
    if token != SLACK_VERIFICATION_TOKEN:
        return 'bad request', 403
    event = data.get('event')
    text = event.get('text')
    # sender_user = event.get('user')
    message = 'Hey :wave: \n We\'ve got a feedback for you: \n {}'.format(text)
    send_slack_message('@{}'.format(receiver), message=message)
    return 'Hello World!', 200

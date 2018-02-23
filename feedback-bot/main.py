import json
import os
import secrets

import redis as redis
from flask import Flask, jsonify, request

from .slack import send_slack_message, get_team_members

SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']
FEEDBACK_MEMBERS = os.environ.get('FEEDBACK_MEMBERS')

app = Flask(__name__)
redis_storage = redis.from_url(url=os.environ['REDIS_URL'], charset='utf-8', decode_responses=True)


@app.route('/')
def hello():
    return 'Hello World! Please, use `/ask` to ask for a feedback', 200


@app.route('/team')
def team():
    members = get_team_members()
    return jsonify(members), 200


@app.route('/ask')
def ask():
    members = get_team_members()
    if FEEDBACK_MEMBERS:
        # if we have variable set, ignore other people
        members = [member for member in members if member[1] in FEEDBACK_MEMBERS]

    random_sender = secrets.choice(members)
    random_receiver = secrets.choice(members)
    while random_receiver == random_sender:
        random_receiver = secrets.choice(members)

    # set sender, receiver pair in the storage
    redis_storage.set(random_sender[0], random_receiver[0])
    message = 'Hey, tell me something nice about @{}'.format(random_receiver[1])
    send_slack_message(channel='@{}'.format(random_sender[0]), message=message)
    return 'Hello World!', 200


@app.route('/forward-feedback', methods=['POST'])
def forward_feedback():
    data = json.loads(request.data)
    challenge = data.get('challenge')
    if challenge:
        # slack verification
        return challenge, 200

    sender = data.get('event').get('user')
    # get receiver from the storage, which is matching sender
    receiver = str(redis_storage.get(sender))
    if not receiver:
        # Ignore message without a receiver
        return 'OK', 200

    token = data.get('token')
    if token != SLACK_VERIFICATION_TOKEN:
        # Security check
        return 'Bad request', 403

    event = data.get('event')
    text = event.get('text')
    # Ignore messages from bot to prevent loops (could happen while debugging)
    # if event.get('bot_id'):
    #     return 'OK', 200

    message = 'Hey :wave: \n We\'ve got a feedback for you: \n {}'.format(text)
    send_slack_message('{}'.format(receiver), message=message)
    # delete sent feedback pair from the storage
    redis_storage.delete(sender)
    return 'OK', 200

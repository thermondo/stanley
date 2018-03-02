import json
import os
import secrets

import redis as redis
from flask import Flask, jsonify, request

from .slack import get_team_members, send_slack_message

SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']
FEEDBACK_MEMBERS = os.environ.get('FEEDBACK_MEMBERS')
# redis key for list of person that already provided feedback
REDIS_KEY_SEND_FEEDBACK = 'SEND_FEEDBACK'
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')

app = Flask(__name__)
redis_storage = redis.from_url(
    url=REDIS_URL,
    charset='utf-8',
    decode_responses=True
)


@app.route('/')
def hello():
    return 'Hello World! Please, use `/ask` to ask for a feedback', 200


@app.route('/team')
def team():
    members = get_team_members()
    return jsonify(members), 200


@app.route('/ask')
def ask():
    members = get_filtered_member()
    sender, receiver = get_sender_receiver(members)

    # set sender, receiver pair in the storage
    redis_storage.set(sender[0], receiver[0])
    message = 'Hey, tell me something nice about @{}'.format(receiver[1])
    send_slack_message(channel='@{}'.format(sender[0]), message=message)
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


def get_filtered_member():
    members = get_team_members()
    if FEEDBACK_MEMBERS:
        # if we have variable set, ignore other people
        members = [member for member in members if member[1]
                   in FEEDBACK_MEMBERS]
    return members


def get_sender_receiver(members):
    # list of user that send a feedback already
    sent_already = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)

    # if the size of both list is the same, it means that everyone already
    # gave feedback and we can start from the beginning
    if len(sent_already) >= len(members):
        redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)
        sent_already = []

    # subtract the list of people that already have send from the member
    can_send = [member for member in members if member[0] not in sent_already]
    random_sender = secrets.choice(can_send)
    # put the picked sender as key to list so we don't bother him until
    # everyone else was askes to provide feedback
    redis_storage.sadd(REDIS_KEY_SEND_FEEDBACK, random_sender[0])

    # figure out to who we can send the feedback, besicly just not to
    # the person we picked to give a feedback
    can_receive = [member for member in members if member is not random_sender]
    random_receiver = secrets.choice(can_receive)

    return random_sender, random_receiver

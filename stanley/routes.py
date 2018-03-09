import json

from flask import jsonify, request

from stanley.app import SLACK_VERIFICATION_TOKEN, app, redis_storage, request_feedback_command
from stanley.slack import get_team_members, send_slack_message


@app.route('/')
def hello():
    return 'Welcome!', 200


@app.route('/team')
def team():
    members = get_team_members()
    return jsonify(members), 200


@app.route('/ask')
def ask():
    request_feedback_command()
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

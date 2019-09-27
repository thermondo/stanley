import json
from typing import Tuple

from flask import request

from stanley.app import app
from stanley.redis import redis_storage
from stanley.settings import SLACK_VERIFICATION_TOKEN
from stanley.slack import send_slack_message


@app.route('/')
def hello() -> Tuple[str, int]:
    return 'This is pretzel day!', 200


@app.route('/forward-feedback', methods=['POST'])
def forward_feedback() -> Tuple[str, int]:
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

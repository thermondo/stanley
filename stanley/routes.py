import json
from typing import Tuple

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from stanley.app import app
from stanley.redis import redis_storage
from stanley.settings import SLACK_VERIFICATION_TOKEN
from stanley.slack import send_slack_message

app = FastAPI()


@app.get('/')
async def hello() -> Tuple[str, int]:
    return 'This is pretzel day!', 200


@app.post('/forward-feedback')
async def forward_feedback(request: Request) -> PlainTextResponse:
    data = await request.json()
    challenge = data.get('challenge')
    if challenge:
        # slack verification
        return PlainTextResponse(challenge, status_code=200)

    sender = data.get('event').get('user')
    # get receiver from the storage, which is matching sender
    receiver = redis_storage.get(sender)
    if not receiver:
        # Ignore message without a receiver
        return PlainTextResponse('OK', status_code=200)

    token = data.get('token')
    if token != SLACK_VERIFICATION_TOKEN:
        # Security check
        return PlainTextResponse('Bad request', status_code=403)

    event = data.get('event')
    text = event.get('text')
    # Ignore messages from bot to prevent loops (could happen while debugging)
    # if event.get('bot_id'):
    #     return 'OK', 200

    message = f'Hey :wave: \n We\'ve got a feedback for you: \n {text}'
    send_slack_message(f'@{receiver}', message=message)
    # delete sent feedback pair from the storage
    redis_storage.delete(sender)
    return PlainTextResponse('OK', status_code=200)

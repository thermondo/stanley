import secrets

import redis as redis
from flask import Flask
from raven.contrib.flask import Sentry

from stanley.settings import FEEDBACK_MEMBERS, REDIS_KEY_SEND_FEEDBACK, REDIS_URL, SENTRY_DSN
from stanley.slack import get_team_members, send_slack_message

app = Flask(__name__)
redis_storage = redis.from_url(
    url=REDIS_URL,
    charset='utf-8',
    decode_responses=True
)
sentry = Sentry(app, dsn=SENTRY_DSN)


@app.cli.command()
def request_feedback_command():
    """Ask random user to give a feedback for another random user."""
    members = get_filtered_member()
    sender, receiver = get_sender_receiver(members)

    # set sender, receiver pair in the storage
    redis_storage.set(sender[0], receiver[0])
    message = 'Hey, tell me something nice about @{}'.format(receiver[1])
    send_slack_message(channel='@{}'.format(sender[0]), message=message)


def get_filtered_member():
    members = get_team_members()
    if FEEDBACK_MEMBERS:
        # if we have variable set, ignore other people
        members = [member for member in members if member[1] in FEEDBACK_MEMBERS]
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
    # everyone else was asked to provide a feedback
    redis_storage.sadd(REDIS_KEY_SEND_FEEDBACK, random_sender[0])

    # figure out to who we can send the feedback, basically just not to
    # the person we picked to give a feedback
    can_receive = [member for member in members if member is not random_sender]
    random_receiver = secrets.choice(can_receive)

    return random_sender, random_receiver

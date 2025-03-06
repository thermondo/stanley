import secrets

from sentry_sdk import capture_message

from stanley.redis import redis_storage
from stanley.settings import (
    FEEDBACK_MEMBERS,
    REDIS_KEY_RECEIVE_FEEDBACK,
    REDIS_KEY_SEND_FEEDBACK,
)
from stanley.slack import get_team_members, send_slack_message


def request_feedback() -> None:
    """Ask random user to give a feedback for another random user."""
    members = get_filtered_member()
    sender = get_sender(members)
    receiver = get_receiver(members, sender)

    message = f"Hey, tell me something nice about @{receiver[1]}"
    response = send_slack_message(channel=f"@{sender[0]}", message=message)

    if response["ok"]:  # type: ignore[index]
        # set sender, receiver pair in the storage
        redis_storage.set(sender[0], receiver[0])
    else:
        capture_message(f"Couldn't send slack message. Response: {response}")


def get_filtered_member() -> list[tuple]:
    members = get_team_members()
    if FEEDBACK_MEMBERS:
        # if we have variable set, ignore other people
        members = [m for m in members if m[1] in FEEDBACK_MEMBERS]
    return members


def get_sender(members: list[tuple]) -> tuple:
    # list of user that send a feedback already
    sent_already = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)

    # if the size of both list is the same, it means that everyone already was
    # asked to give feedback and we can start from the beginning
    if len(sent_already) >= len(members):
        redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)
        sent_already = set()

    # subtract the list of people that already have send from the member
    can_send = [m for m in members if m[0] not in sent_already]
    random_sender = secrets.choice(can_send)
    # put the picked sender as key to list so we don't bother him until
    # everyone else was asked to provide a feedback
    redis_storage.sadd(REDIS_KEY_SEND_FEEDBACK, random_sender[0])

    return random_sender


def get_receiver(members: list[tuple], sender: tuple) -> tuple:
    # subtract the list of people that already have received a feedback and
    # also remove the person that is the sender
    received_already = redis_storage.smembers(REDIS_KEY_RECEIVE_FEEDBACK)
    can_receive = [
        m for m in members if m[0] not in received_already and m is not sender
    ]

    # if the size of the list is zero, everyone received a feedback and we can start
    # again
    if len(can_receive) == 0:
        # FIXME the last person will never get a feedback from this round
        redis_storage.delete(REDIS_KEY_RECEIVE_FEEDBACK)
        can_receive = [m for m in members if m is not sender]

    random_receiver = secrets.choice(can_receive)
    # put the picked receiver as key to list so we don't bother him until
    # everyone else received a feedback
    redis_storage.sadd(REDIS_KEY_RECEIVE_FEEDBACK, random_receiver[0])

    return random_receiver

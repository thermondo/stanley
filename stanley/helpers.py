import secrets

from stanley.redis import redis_storage
from stanley.settings import FEEDBACK_MEMBERS, REDIS_KEY_RECEIVE_FEEDBACK, REDIS_KEY_SEND_FEEDBACK
from stanley.slack import get_team_members, send_slack_message


def request_feedback():
    """Ask random user to give a feedback for another random user."""
    members = get_filtered_member()
    sender = get_sender(members)
    receiver = get_receiver(members, sender)

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


def get_sender(members):
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

    return random_sender


def get_receiver(members, sender):
    received_aready = redis_storage.smembers(REDIS_KEY_RECEIVE_FEEDBACK)
    # subtract the list of people that already have received feedback
    can_receive = [member for member in members if member[0] not in received_aready]
    # also remove the person that is the sender
    can_receive = [member for member in can_receive if member is not sender]

    # if the size of the list is zero, everyone received a feedback and
    # we can start again
    if len(can_receive) == 0:
        redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)
        can_receive = [member for member in members if member is not sender]

    random_receiver = secrets.choice(can_receive)
    # put the picked receiver as key to list so we don't bother him until
    # everyone else received a feedback
    redis_storage.sadd(REDIS_KEY_RECEIVE_FEEDBACK,  random_receiver[0])

    return random_receiver

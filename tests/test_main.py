from stanley.helpers import get_sender_receiver
from stanley.redis import redis_storage
from stanley.settings import REDIS_KEY_SEND_FEEDBACK


def test_get_sender_receiver(members):
    sender, receiver = get_sender_receiver(members)

    assert sender is not receiver
    saved_sender = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)
    assert sender[0] in saved_sender

    # cleanup used key
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)


def test_get_sender_receiver_when_already_run(members):
    amureki_id = members[0][0]
    sebastian_id = members[1][0]

    # let's say that amureki already provided a feedback
    redis_storage.sadd(REDIS_KEY_SEND_FEEDBACK, amureki_id)

    sender, receiver = get_sender_receiver(members)

    # we have just two members and one is already answered so
    # we know who will be the sender and the receiver
    assert sender[0], sebastian_id
    assert receiver[0], amureki_id

    saved_sender = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)
    assert amureki_id in saved_sender
    assert sebastian_id in saved_sender

    # cleanup used key
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)

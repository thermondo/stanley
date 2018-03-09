from stanley.helpers import get_sender, get_receiver
from stanley.redis import redis_storage
from stanley.settings import REDIS_KEY_SEND_FEEDBACK, REDIS_KEY_RECEIVE_FEEDBACK


def test_get_sender(members):
    sender = get_sender(members)

    saved_sender = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)
    assert sender[0] in saved_sender

    # cleanup used key
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)


def test_get_sender_when_already_run(members):
    amureki_id = members[0][0]
    sebastian_id = members[1][0]

    # let's say that amureki already provided a feedback
    redis_storage.sadd(REDIS_KEY_SEND_FEEDBACK, amureki_id)

    sender = get_sender(members)

    # we have just two members and one has already answered so
    # we know who will be the sender
    assert sender[0], sebastian_id

    saved_sender = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)
    assert amureki_id in saved_sender
    assert sebastian_id in saved_sender

    # cleanup used key
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)


def test_get_receiver(members):
    amureki = members[0]
    sebastian = members[1]

    # say sebastian is the sender so we expect amureki
    # to be the receiver
    receiver = get_receiver(members, sebastian)

    assert receiver, amureki

    # cleanup used key
    redis_storage.delete(REDIS_KEY_RECEIVE_FEEDBACK)


def test_get_receiver_impossible(members):
    """Handle edge case.

    It is possible that the last person that is left to get feedback
    is the same person as the sender. The function should handle this
    case and return a proper receiver.

    """
    amureki = members[0]
    sebastian = members[1]

    # let's say that amureki already received feedback
    # that means that only sebastian is left as receiver of a feedback
    redis_storage.sadd(REDIS_KEY_RECEIVE_FEEDBACK, amureki[0])

    # here we decide that sebastian is the sender, so he can't be
    # the receiver
    receiver = get_receiver(members, sebastian)

    saved_receiver = redis_storage.smembers(REDIS_KEY_RECEIVE_FEEDBACK)

    # since sebastian is the sender, we expect that amureki is the receiver
    assert amureki[0] in saved_receiver
    # sebastian shouln't have received a feedback yet
    assert sebastian[0] not in saved_receiver
    assert receiver, amureki

    # cleanup used key
    redis_storage.delete(REDIS_KEY_RECEIVE_FEEDBACK)

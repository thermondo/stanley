from stanley.helpers import get_receiver, get_sender
from stanley.redis import redis_storage
from stanley.settings import REDIS_KEY_RECEIVE_FEEDBACK, REDIS_KEY_SEND_FEEDBACK


def test_get_sender(redis_clean_up, members):
    assert redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK) == set()

    sender = get_sender(members)

    saved_sender = redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)
    assert sender[0] in saved_sender


def test_get_sender_when_everyone_was_asked(redis_clean_up, members):
    members_len = len(members)
    [get_sender(members) for _ in range(members_len)]

    assert len(redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)) == members_len

    get_sender(members)

    assert len(redis_storage.smembers(REDIS_KEY_SEND_FEEDBACK)) == 1


def test_get_sender_when_someone_sent_feedback_already(redis_clean_up, two_members):
    members = two_members
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


def test_get_receiver(redis_clean_up, members):
    sebastian = members[1]

    receiver = get_receiver(members, sebastian)

    assert receiver != sebastian


def test_everybody_has_received_feedback(redis_clean_up, members):
    redis_storage.delete(REDIS_KEY_RECEIVE_FEEDBACK)
    sebastian = members[1]

    get_receiver(members, sebastian)
    get_receiver(members, sebastian)

    assert len(redis_storage.smembers(REDIS_KEY_RECEIVE_FEEDBACK)) == 2

    get_receiver(members, sebastian)

    # when all members received feedback, reset the queue
    assert len(redis_storage.smembers(REDIS_KEY_RECEIVE_FEEDBACK)) == 1


def test_get_receiver_impossible(redis_clean_up, two_members):
    """Handle edge case.

    It is possible that the last person that is left to get feedback
    is the same person as the sender. The function should handle this
    case and return a proper receiver.

    """
    members = two_members
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
    # sebastian should not have received a feedback yet
    assert sebastian[0] not in saved_receiver
    assert receiver, amureki

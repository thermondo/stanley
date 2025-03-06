from unittest.mock import patch

import pytest

from stanley.redis import redis_storage
from stanley.settings import REDIS_KEY_SEND_FEEDBACK
from stanley.slack import slack_client

from .utils import gen_string


@pytest.fixture
def two_members():
    amureki_id = gen_string(9)
    sebastian_id = gen_string(9)
    assert amureki_id is not sebastian_id

    members = [[amureki_id, "amureki"], [sebastian_id, "sebastiankapunkt"]]

    return members


@pytest.fixture
def members():
    amureki_id = gen_string(9)
    sebastian_id = gen_string(9)
    anapaulagomes_id = gen_string(9)
    assert len(set([amureki_id, sebastian_id, anapaulagomes_id])) == 3

    members = [
        [amureki_id, "amureki"],
        [sebastian_id, "sebastiankapunkt"],
        [anapaulagomes_id, "anapaulagomes"],
    ]

    return members


@pytest.fixture
def redis_clean_up():
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)
    yield
    redis_storage.delete(REDIS_KEY_SEND_FEEDBACK)


@pytest.fixture
def slack_api_call_mock(monkeypatch):
    def fake_api_call(endpoint):
        return {
            "ok": True,
            "members": [
                {"id": "U03H6N5JZ", "name": "anne"},
                {"id": "U01FECGP57X", "name": "ayyoub.maknassa"},
                {"id": "U0PES7Z6J", "name": "amureki"},
                {"id": "U029MJK62", "name": "syphar"},
            ],
        }

    monkeypatch.setattr(slack_client, "api_call", fake_api_call)


@pytest.fixture
def slack_post_message_mock():
    with patch("stanley.slack.slack_client.chat_postMessage") as mock:
        yield mock

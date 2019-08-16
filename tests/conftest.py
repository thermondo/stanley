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

    members = [
        [
            amureki_id,
            'amureki'
        ],
        [
            sebastian_id,
            'sebastiankapunkt'
        ]
    ]

    return members


@pytest.fixture
def members():
    amureki_id = gen_string(9)
    sebastian_id = gen_string(9)
    anapaulagomes_id = gen_string(9)
    assert len(set([amureki_id, sebastian_id, anapaulagomes_id])) == 3

    members = [
        [
            amureki_id,
            'amureki'
        ],
        [
            sebastian_id,
            'sebastiankapunkt'
        ],
        [
            anapaulagomes_id,
            'anapaulagomes'
        ]
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
            'ok': True,
            'members': [
                {'id': 'USLACKBOT', 'name': 'slackbot'},
                {'id': 'UCRJYDGTU', 'name': 'ana.gomes'},
                {'id': 'UCRPLKK2R', 'name': 'amureki'},
                {'id': 'U9D632ZK3', 'name': 'sebastiankapunkt'},
            ]
        }
    monkeypatch.setattr(slack_client, 'api_call', fake_api_call)

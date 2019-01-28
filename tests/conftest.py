import pytest

from .utils import gen_string


@pytest.fixture
def two_members():
    amureki_id = gen_string(9)
    sebastian_id = gen_string(9)
    assert amureki_id is not sebastian_id

    members = [
        [
            amureki_id,
            "amureki"
        ],
        [
            sebastian_id,
            "sebastiankapunkt"
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
            "amureki"
        ],
        [
            sebastian_id,
            "sebastiankapunkt"
        ],
        [
            anapaulagomes_id,
            "anapaulagomes"
        ]
    ]

    return members

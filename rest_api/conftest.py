import pytest
import os


@pytest.fixture(scope="session")
def token_grained_all():
    return os.environ["TOKEN_GRAINED_ALL"]


@pytest.fixture(scope="session")
def token_grained_none():
    return os.environ["TOKEN_GRAINED_NONE"]

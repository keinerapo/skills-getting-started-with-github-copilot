from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def reset_activities():
    snapshot = deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(snapshot)


@pytest.fixture
def client(reset_activities):
    return TestClient(app_module.app)
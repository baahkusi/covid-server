import falcon
from falcon import testing
import pytest
from covid19.app import api
from covid19.db import Logins


@pytest.fixture
def client():
    return testing.TestClient(api)


@pytest.fixture
def auth_headers():
    login = Logins.select().order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }

    return headers
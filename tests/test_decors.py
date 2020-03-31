from covid19.db import Logins, Users
import json


def test_decors(client):

    payload = {
        "111": {
            "decor_tester": {},
            "000": ["decor_tester"]
        },
        "000": ["111"]
    }

    login = Logins.select().join(Users).order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)
    print(response.json)
    assert response.json["111"]["decor_tester"]["status"]

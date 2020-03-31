import falcon
from falcon import testing
import pytest
import json
from covid19.app import api
from covid19.db import Logins, Users, Activations


def test_register(client):
    payload = {
        "111": {
            "register": {
                "email": "sbksoftwares@gmail.com",
                "password": "1234-sbksoftwares"
            },
            "000": ["register"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))
    assert response.json["111"]["register"]["status"]


def test_login(client):
    payload = {
        "111": {
            "login": {
                "email": "sbksoftwares@gmail.com",
                "password": "1234-sbksoftwares",
                "device_hash": "64bea9715647332937c9c2b03a9e9771",
                "device_data": {
                    "user_agent": "Mozilla"
                }
            },
            "000": ["login"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    assert response.json["111"]["login"]["status"]


def test_reset_password(client):
    payload = {
        "111": {
            "reset_password": {
                "phase": "generate",
                "email": "sbksoftwares@gmail.com"
            },
            "000": ["reset_password"]
        },
        "000": ["111"]
    }

    response = client.simulate_post('/action', body=json.dumps(payload))

    r1 = response.json["111"]["reset_password"]["status"]
    r2 = False
    if r1:
        code = Activations.select().order_by(Activations.id.desc()).get().code
        payload = {
            "111": {
                "reset_password": {
                    "phase": "reset",
                    "email": "sbksoftwares@gmail.com",
                    "password": "4321-sbksoftwares",
                    "code": code
                },
                "000": ["reset_password"]
            },
            "000": ["111"]
        }

        response = client.simulate_post('/action',body=json.dumps(payload))
        
        r2 = response.json["111"]["reset_password"]["status"]
    assert r1 and r2


def test_activate_account(client):
    medium = "email"
    payload = {
        "111": {
            "activate_account": {
                "phase": "generate",
                "medium": medium
            },
            "000": ["activate_account"]
        },
        "000": ["111"]
    }

    login = Logins.select().order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)

    r1 = response.json["111"]["activate_account"]["status"]
    print(response.json)
    r2 = False
    if r1:
        code = Activations.select().order_by(Activations.id.desc()).get().code
        payload = {
            "111": {
                "activate_account": {
                    "phase": "activate",
                    "medium": medium,
                    "code": code
                },
                "000": ["activate_account"]
            },
            "000": ["111"]
        }

        response = client.simulate_post('/action',
                                        body=json.dumps(payload),
                                        headers=headers)
        print(response.json)
        r2 = response.json["111"]["activate_account"]["status"]
    assert r1 and r2


def test_auth(client):

    payload = {"111": {"auth": {}, "000": ["auth"]}, "000": ["111"]}

    login = Logins.select().join(Users).order_by(Logins.id.desc()).get()

    headers = {
        'Authorization': login.token,
        'Account-ID': login.user.email,
        'Device-ID': login.device_hash
    }

    response = client.simulate_post('/action',
                                    body=json.dumps(payload),
                                    headers=headers)

    assert response.json["111"]["auth"]["status"]


def test_create_user(client):

    payload = {
            "111": {
                "create_user": {
                    "email":"usebaku@gmail.com", 
                    "phone":"987654321", 
                    "level":"admin", 
                    "country":["Ghana", "Ashanti"], 
                    "city":"Kumasi", 
                    "code":"+233", 
                    "phone_code":"+233 987654321",
                    "mode":"create",
                    "id":12
                },
                "000": ["create_user"]
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

    assert response.json["111"]["create_user"]["status"]
from moovie_api.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_genres_post():
    response = client.post(
        "/genres/",
        headers={"X-Token": "fake-super-secret-token"},
        json={"name": "TESTPYTEST1"}
    )
    assert response.status_code == 200


def test_genres_get():
    response = client.get(
        "/genres/", headers={"X-Token": "fake-super-secret-token"},)
    assert response.status_code == 200


def test_fail_genres_get():
    response = client.get("/genres/", headers={"X-Token": "badtoken"},)
    assert response.status_code == 400


def test_auth_token():
    response = client.post("/token", json={
        "username": "carlos@grydd.com",
        "password": "testpassnotreallyhashed"
    },)
    assert response.status_code == 422


def test_get_users_auth():
    response = client.get("/users/", headers={
        "X-Token": "fake-super-secret-token",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYXJsb3NAZ3J5ZGQuY29tIiwiZXhwIjoxNjUzNTA4OTI1fQ.LOFtxq7o-Zyi2xc23l4YSRrb3rlHD_ZLmb57fqgFwAk"
    },)
    assert response.status_code == 200


def test_fail_get_users_no_auth():
    response = client.get("/users/", headers={
        "X-Token": "fake-super-secret-token",
    },)
    assert response.status_code == 401


def test_create_user_post():
    response = client.post(
        "/users/",
        headers={
            "X-Token": "fake-super-secret-token",
        },
        json={
            "email": "charly@gmail.com",
            "full_name": "charly senerwan",
            "password": "12345"
        }
    )
    assert response.status_code == 200

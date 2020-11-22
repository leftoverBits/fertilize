from http import HTTPStatus

def test_hello_world(client):
    res = client.get("/")
    assert res.status_code == HTTPStatus.OK
    assert res.data == b"Hello, World!"
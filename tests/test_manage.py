import json
from http import HTTPStatus


class TestFindPlants:
    def test_find_plants(self, client):
        res = client.get("/")
        assert res.status_code == HTTPStatus.OK
        assert len(json.loads(res.data)) == 5

    def test_find_plant(self, client):
        res = client.get("/1")
        assert res.status_code == HTTPStatus.OK
        assert len(json.loads(res.data)) == 1


class TestAddPlant:
    def test_add_plant(self, client):
        res = client.post(
            "/add",
            data=json.dumps({"name": "foobar"}),
            headers={"Content-Type": "application/json"},
        )
        assert res.status_code == HTTPStatus.CREATED

        res = json.loads(res.data)
        assert res["id"] == 6
        assert res["name"] == "foobar"

    def test_name_conflict(self, client):
        res = client.post(
            "/add",
            data=json.dumps({"name": "plant1"}),
            headers={"Content-Type": "application/json"},
        )
        assert res.status_code == HTTPStatus.CONFLICT

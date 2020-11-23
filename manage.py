import json
import typing as t
from datetime import date
from http import HTTPStatus

from flask import Flask, jsonify, request
from safetywrap import Option


def date_to_str(_date: date) -> str:
    return _date.strftime("%Y-%m-%d")


def serialize_date(key: str, _date: date) -> t.Dict[str, str]:
    return Option.of(_date).map(date_to_str).map(lambda lw: {key: lw}).unwrap_or(dict())


class Plant(t.NamedTuple):
    uid: int
    name: str
    last_watered: t.Optional[date] = None
    last_fed: t.Optional[date] = None

    @property
    def serialized(self) -> t.Dict[str, str]:
        return {
            "id": self.uid,
            "name": self.name,
            **serialize_date("last_watered", self.last_watered),
            **serialize_date("last_fed", self.last_fed),
        }


DATE_1 = date(2020, 1, 1)
DATE_2 = date(2020, 2, 1)

PLANT_NEVER_CARED_FOR = Plant(uid=1, name="plant1", last_watered=None, last_fed=None)
WATERED_PLANT = Plant(uid=2, name="plant2", last_watered=DATE_1, last_fed=None)
FED_PLANT = Plant(uid=3, name="plant3", last_watered=None, last_fed=DATE_1)
PLANT_CARED_FOR_SEPARATE_TIMES = Plant(
    uid=4, name="plant4", last_watered=DATE_1, last_fed=DATE_2
)
PLANT_CARED_FOR_SAME_TIME = Plant(
    uid=5, name="plant5", last_watered=DATE_1, last_fed=DATE_1
)

ALL_PLANTS: t.List[Plant] = [
    PLANT_NEVER_CARED_FOR,
    WATERED_PLANT,
    FED_PLANT,
    PLANT_CARED_FOR_SEPARATE_TIMES,
    PLANT_CARED_FOR_SAME_TIME,
]


def _next_plant_uid() -> int:
    return max(ALL_PLANTS, key=lambda p: p.uid).uid + 1


def _add_plant(name: str) -> Plant:
    exists: bool = next(filter(lambda p: p.name == name, ALL_PLANTS), None) is not None
    if exists is True:
        raise Exception(f"Plant named {name} already exists!")
    new_plant = Plant(uid=_next_plant_uid(), name=name)
    ALL_PLANTS.append(new_plant)
    return new_plant


def _find_plants(ids: t.Set[int]) -> t.Tuple[Plant]:
    return tuple(filter(lambda p: p.uid in ids, ALL_PLANTS))


def create_app():
    app = Flask(__name__)

    @app.route("/")
    @app.route("/<plant_id>")
    def get_plants(plant_id=None):
        lookup_ids: t.Set[int] = set(
            [int(plant_id)] if plant_id is not None else [p.uid for p in ALL_PLANTS]
        )
        plants: t.Tuple[Plant] = _find_plants(lookup_ids)

        status_code: HTTPStatus = (
            HTTPStatus.OK if len(plants) > 0 else HTTPStatus.NOT_FOUND
        )
        return (
            json.dumps([p.serialized for p in plants]),
            status_code,
        )

    @app.route("/add", methods=["POST"])
    def add_plant():
        try:
            plant: Plant = _add_plant(name=request.get_json()["name"])
            return jsonify(plant.serialized), HTTPStatus.CREATED
        except Exception as e:
            # Plant already exists
            print(str(e))
            return "", HTTPStatus.CONFLICT

    return app
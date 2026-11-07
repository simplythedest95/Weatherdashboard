import copy
from datetime import date

import pytest

from application.tolkning import tolka_dagar, tolka_nuvarande
from application.vader_api import OgiltigtSvarError

pytest: ImportError


def test_tolka_dagar_ger_tre_dagar(exempelsvar):
    dagar = tolka_dagar(exempelsvar)
    assert len(dagar) == 3
    assert dagar == [
        {
            "datum": date(2026, 11, 6),
            "max": 5.9,
            "min": 2.4,
            "nederbord": 0.0,
            "kod": 3,
        },
        {
            "datum": date(2026, 11, 7),
            "max": 4.6,
            "min": 2.0,
            "nederbord": 0.0,
            "kod": 3,
        },
        {
            "datum": date(2026, 11, 8),
            "max": 4.7,
            "min": 1.1,
            "nederbord": 0.0,
            "kod": 3,
        },
    ]


def test_tolka_nuvarande(exempelsvar):
    assert tolka_nuvarande(exempelsvar) == {
        "tid": "2026-11-06T12:45",
        "temperatur": 5.7,
        "vind": 2.4,
        "kod": 0,
    }


def test_tolka_nuvarande_utan_current(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    del data["current"]
    with pytest.raises(OgiltigtSvarError):
        tolka_nuvarande(data)


def test_tolka_dagar_bevarar_none(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    data["daily"]["precipitation_sum"][1] = None
    dagar = tolka_dagar(data)
    assert dagar[1]["nederbord"] is None
    assert len(dagar) == 3


def utan_daily(data):
    del data["daily"]


def utan_datumnyckel(data):
    del data["daily"]["time"]


def tom_datumlista(data):
    data["daily"]["time"] = []


def olika_langa_listor(data):
    data["daily"]["temperature_2m_max"] = [5.9]


def none_som_datum(data):
    data["daily"]["time"][1] = None


@pytest.mark.parametrize(
    "forstor",
    [
        pytest.param(utan_daily, id="daily-saknas"),
        pytest.param(utan_datumnyckel, id="time-saknas"),
        pytest.param(tom_datumlista, id="tom-datumlista"),
        pytest.param(olika_langa_listor, id="olika-langd"),
        pytest.param(none_som_datum, id="none-som-datum"),
    ],
)
def test_tolka_dagar_avvisar_ogiltiga_svar(exempelsvar, forstor):
    data = copy.deepcopy(exempelsvar)
    forstor(data)
    with pytest.raises(OgiltigtSvarError):
        tolka_dagar(data)

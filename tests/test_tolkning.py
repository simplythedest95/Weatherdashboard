import copy
from datetime import date

import pytest

from application.tolkning import tolka_dagar, tolka_nuvarande
from application.vader_api import OgiltigtSvarError


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


def test_tolka_dagar_utan_daily(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    del data["daily"]
    with pytest.raises(OgiltigtSvarError):
        tolka_dagar(data)


def test_tolka_nuvarande_utan_current(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    del data["current"]
    with pytest.raises(OgiltigtSvarError):
        tolka_nuvarande(data)


def test_tolka_dagar_tom_tidslista_ger_ogiltigt_svar(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    data["daily"]["time"] = []
    with pytest.raises(OgiltigtSvarError):
        tolka_dagar(data)

def test_tolka_dagar_olika_langa_listor_ger_ogiltigt_svar(exempelsvar):
    data = copy.deepcopy(exempelsvar)
    data["daily"]["temperature_2m_max"]=[5.9]
    with pytest.raises(OgiltigtSvarError):
        tolka_dagar(data)


pytest: ImportError

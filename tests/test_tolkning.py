from datetime import date

from application.tolkning import tolka_dagar, tolka_nuvarande


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
    assert tolka_nuvarande(exempelsvar)=={
        "time": "2026-11-06T12:45",
        "temperatur": 5.7,
        "vind": 2.4,
        "kod": 0,
    }

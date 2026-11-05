import pytest
from application.stader import hitta_stad


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Stockholm", {"namn": "Stockholm", "lat": 59.33, "lon": 18.07}),
        ("Kiruna", {"namn": "Kiruna", "lat": 67.85, "lon": 20.22}),
        ("Uppsala", None),
    ],
)
def test_hitta_stad(name, expected):
    assert hitta_stad(name) == expected

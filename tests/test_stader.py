import pytest

from application.stader import hitta_stad

KIRUNA = {"namn": "Kiruna", "lat": 67.86, "lon": 20.23}
STOCKHOLM = {"namn": "Stockholm", "lat": 59.33, "lon": 18.07}
MALMÖ = {"namn": "Malmö", "lat": 55.61, "lon": 13.00}
UMEÅ = {"namn": "Umeå", "lat": 63.83, "lon": 20.26}
GÖTEBORG = {"namn": "Göteborg", "lat": 57.71, "lon": 11.97}


@pytest.mark.parametrize(
    "name, expected",
    [
        pytest.param("Umeå", UMEÅ, id="umea"),
        pytest.param("Malmö", MALMÖ, id="malmo"),
        pytest.param("Göteborg", GÖTEBORG, id="goteborg"),
        pytest.param("Stockholm", STOCKHOLM, id="stockholm"),
        pytest.param("Kiruna", KIRUNA, id="kiruna"),
        pytest.param("kiruna", KIRUNA, id="sma-bokstaver"),
        pytest.param("MALMÖ", MALMÖ, id="stora-bokstaver"),
        pytest.param(" Stockholm ", STOCKHOLM, id="mellanslag"),
        pytest.param("GOTEBORG", None, id="felstavning"),
        pytest.param("Uppsala", None, id="okand-stad"),
        pytest.param("", None, id="tom-strang"),
        pytest.param(" ", None, id="tom-strang-med-mellanslag"),
        pytest.param(None, None, id="inget-varde"),
    ],
)
def test_hitta_stad(name, expected):
    assert hitta_stad(name) == expected

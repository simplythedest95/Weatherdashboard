import pytest


@pytest.fixture
def exempelsvar():
    """Avkortat riktigt svar från Open-Meteo"""
    return {
        "current": {
            "time": "2026-11-06T12:45",
            "interval": 900,
            "temperature_2m": 5.7,
            "wind_speed_10m": 2.4,
            "weather_code": 0,
        },
        "daily": {
            "time": [
                "2026-11-06",
                "2026-11-07",
                "2026-11-08",
            ],
            "temperature_2m_max": [5.9, 4.6, 4.7],
            "temperature_2m_min": [2.4, 2.0, 1.1],
            "precipitation_sum": [0.0, 0.0, 0.0],
            "weather_code": [3, 3, 3],
        },
    }

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
# Timeout på 5 sekunder vid anrop
TIMEOUT = 5


class VaderTjanstError(Exception):
    """Kastas när vädertjänsten inte svarar
    eller svarar med ogitlig data."""


def hamta_prognos(lat, lon):
    """Hämtar nuvarande väder och tre dagars prognos.
    Tar emot latitud och longitud
    Returnerar API:ets svar som en dict
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "auto",
        "forecast_days": 3,
        "wind_speed_unit": "ms",
    }
    try:
        svar = requests.get(API_URL, params=params, timeout=TIMEOUT)
        svar.raise_for_status()
        return svar.json()
    except (requests.RequestException, ValueError) as fel:
        raise VaderTjanstError("Vädertjänsten svarar inte just nu.") from fel

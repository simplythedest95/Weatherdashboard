import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
# Timeout på 5 sekunder vid anrop
TIMEOUT = 5


def hamta_prognos(lat, lon):
    """Hämtar nuvarande väder och tre dagars prognos.
    Tar emot latitud och longitud
    Returnerar API:ets svar som en dict
    """
    params = {
        "latitude": lat,
        "longitude": lon,
    }
    svar = requests.get(API_URL, params=params, timeout=TIMEOUT)

    svar.raise_for_status()
    return svar.json()

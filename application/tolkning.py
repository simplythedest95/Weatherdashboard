from datetime import date
from application.vader_api import OgiltigtSvarError

"""Rena funktioner som tolkar svaret från Open-Meteo."""


def tolka_dagar(data):
    """Gör om daily-delen av API-svaret
    till en lista med en dict per dag"""
    try:
        daily = data["daily"]
    except KeyError as fel:
        raise OgiltigtSvarError("Svaret saknar dagsprognos") from fel

    dagar = []

    for tid, hogst, lagst, nederbord, kod in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["precipitation_sum"],
        daily["weather_code"],
        strict=True,
    ):
        dagar.append(
            {
                "datum": date.fromisoformat(tid),
                "max": hogst,
                "min": lagst,
                "nederbord": nederbord,
                "kod": kod,
            }
        )
    return dagar


def tolka_nuvarande(data):
    """Plockar ut nuvarande väder ur API-svaret
    med egna nyckelnamn"""
    try:
        current = data["current"]
    except KeyError as fel:
        raise OgiltigtSvarError("Svaret saknar nuvarande väderdata") from fel
    return {
        "temperatur": current["temperature_2m"],
        "vind": current["wind_speed_10m"],
        "kod": current["weather_code"],
        "tid": current["time"],
    }

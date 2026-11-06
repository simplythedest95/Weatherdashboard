from datetime import date

"""Rena funktioner som tolkar svaret från Open-Meteo."""


def tolka_dagar(data):
    """Gör om daily-delen av API-svaret
    till en lista med en dict per dag"""
    daily = data["daily"]
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

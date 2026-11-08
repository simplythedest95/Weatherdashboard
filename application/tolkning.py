from datetime import date

from application.vader_api import OgiltigtSvarError

"""Rena funktioner som tolkar svaret från Open-Meteo."""

VADERKODER = {
    0: ("Klart", "sun-fill"),
    1: ("Mestadels klart", "sun-fill"),
    2: ("Halvklart", "cloud-sun-fill"),
    3: ("Mulet", "clouds-fill"),
    45: ("Dimma", "cloud-fog-fill"),
    48: ("Dimma", "cloud-fog-fill"),
    51: ("Duggregn", "cloud-drizzle-fill"),
    53: ("Duggregn", "cloud-drizzle-fill"),
    55: ("Duggregn", "cloud-drizzle-fill"),
    56: ("Underkylt duggregn", "cloud-sleet-fill"),
    57: ("Underkylt duggregn", "cloud-sleet-fill"),
    61: ("Lätt regn", "cloud-rain-fill"),
    63: ("Regn", "cloud-rain-fill"),
    65: ("Kraftigt Regn", "cloud-rain-heavy-fill"),
    66: ("Underkylt regn", "cloud-sleet-fill"),
    67: ("Underkylt regn", "cloud-sleet-fill"),
    71: ("Lätt snöfall", "cloud-snow-fill"),
    73: ("Snöfall", "cloud-snow-fill"),
    75: ("Kraftigt snöfall", "cloud-snow-fill"),
    77: ("Snö", "snow"),
    80: ("Lätta regnskurar", "cloud-rain-fill"),
    81: ("Regnskurar", "cloud-rain-fill"),
    82: ("Kraftiga regnskurar", "cloud-rain-heavy-fill"),
    85: ("Lätta snöbyar", "cloud-snow-fill"),
    86: ("Kraftiga snöbyar", "cloud-snow-fill"),
    95: ("Åska", "cloud-lightning-fill"),
    96: ("Åska med hagel", "cloud-lightning-rain-fill"),
    97: ("Kraftig åska", "lightning-charge-fill"),
    99: ("Åska med kraftigt hagel", "cloud-lightning-rain-fill"),
}

OKANT_VADER = ("Okänt väder", "question-circle-fill")


def beskriv_vaderkod(kod):
    """Översätter en WMO-väderkod till svenksk text och ett ikonnamn.
    Okända koder och None ger OKANT_VADER"""
    return VADERKODER.get(kod, OKANT_VADER)


def tolka_dagar(data):
    """Gör om daily-delen av API-svaret
    till en lista med en dict per dag"""
    try:
        daily = data["daily"]
        if not daily["time"]:
            raise OgiltigtSvarError("Svaret innehåller inga datum")

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
    except (KeyError, ValueError, TypeError) as fel:
        raise OgiltigtSvarError("Svaret från vädertjänsten är ofullständigt") from fel
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

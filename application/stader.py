# Koordinaterna är tagna från tabellen i den individuella uppgiften.
STADER = [
    {"namn": "Stockholm", "lat": 59.33, "lon": 18.07},
    {"namn": "Kiruna", "lat": 67.86, "lon": 20.23},
    {"namn": "Göteborg", "lat": 57.71, "lon": 11.97},
    {"namn": "Umeå", "lat": 63.83, "lon": 20.26},
    {"namn": "Malmö", "lat": 55.61, "lon": 13.00},
]


def hitta_stad(namn):
    """Slår upp en stad i STADER
    Tar emot ett stadsnamn, t.ex. "Stockholm"
    Returnerar stadens dict med namn, lat och lon,
    eller None om staden inte finns i listan"""
    for stad in STADER:
        if stad["namn"] == namn:
            return stad
    return None

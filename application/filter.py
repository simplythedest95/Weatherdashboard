"""Jinja-filter som formaterar värden för visning"""

MINUS = "\u2212"  # riktigt minustecken
SAKNAS = "\u2013"  # Visas när ett värde saknas
GRADER = " °C"  # Celsius tecknet
MS = " m/s"  # Meter per sekund
MM = " mm"  # Millimeter
VECKODAGAR = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
MANADER = [
    "jan",
    "feb",
    "mar",
    "apr",
    "maj",
    "jun",
    "jul",
    "aug",
    "sep",
    "okt",
    "nov",
    "dec",
]


def _formatera_tal(varde):
    """Avrundar till en decimal,
    med decimalkomma och riktigt minustecken"""
    tal = round(varde, 1)
    if tal == 0:
        tal = 0.0  # tar bort "minusnolla"

    text = f"{tal:.1f}"
    return text.replace(".", ",").replace("-", MINUS)


def _med_enhet(varde, enhet):
    """Formaterar ett värde med enhet,
    eller SAKNAS om värdet saknas."""
    if varde is None:
        return SAKNAS
    return f"{_formatera_tal(varde)}{enhet}"


def temperatur(varde):
    """Formaterar en temperatur, t.ex. 12,3 °C"""
    return _med_enhet(varde, GRADER)


def vind(varde):
    """Formaterar en vindhastighet, t.ex 3,5 m/s"""
    return _med_enhet(varde, MS)


def nederbord(varde):
    """Formaterar en mängd nederbord, t.ex 1,2 mm"""
    return _med_enhet(varde, MM)


def veckodag(datum):
    """Formaterar ett datum, t.ex. Fredag 6 nov."""
    if datum is None:
        return SAKNAS
    namn = VECKODAGAR[datum.weekday()]
    manad = MANADER[datum.month - 1]
    return f"{namn} {datum.day} {manad}"

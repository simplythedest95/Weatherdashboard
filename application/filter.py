"""Jinja-filter som formaterar värden för visning"""

MINUS = "\u2212"  # riktigt minustecken
SAKNAS = "\u2013"  # Visas när ett värde saknas
GRADER = " °C"  # Celsius tecknet


def _formatera_tal(varde):
    """Avrundar till en decimal,
    med decimalkomma och riktigt minustecken"""
    tal = round(varde, 1)
    if tal == 0:
        tal = 0.0  # tar bort "minusnolla"

    text = f"{tal:.1f}"
    return text.replace(".", ",").replace("-", MINUS)


def temperatur(varde):
    """Formaterar en temperatur, t.ex. 12,3°C"""
    if varde is None:
        return SAKNAS
    return f"{_formatera_tal(varde)}{GRADER}"

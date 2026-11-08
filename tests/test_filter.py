import pytest

from application.filter import SAKNAS, nederbord, temperatur, vind, veckodag

from datetime import date
GRADER = " \u00b0C"  # Mellanslag plus gradertecken efterföljt av C för celsius.
MINUS = "\u2212"  # Riktigt minustecken istället för bindestreck


@pytest.mark.parametrize(
    "varde,forvantat",
    [
        pytest.param(12.34, "12,3" + GRADER, id="avrundning"),
        pytest.param(5, "5,0" + GRADER, id="heltal"),
        pytest.param(-8.4, MINUS + "8,4" + GRADER, id="minus"),
        pytest.param(-0.04, "0,0" + GRADER, id="minus-noll"),
        pytest.param(None, SAKNAS, id="saknas"),
    ],
)
def test_temperatur(varde, forvantat):
    assert temperatur(varde) == forvantat


@pytest.mark.parametrize(
    "varde, forvantat",
    [
        pytest.param(3.46, "3,5 m/s", id="avrundning"),
        pytest.param(0, "0,0 m/s", id="vindstilla"),
        pytest.param(12, "12,0 m/s", id="heltal"),
        pytest.param(None, SAKNAS, id="saknas"),
    ],
)
def test_vind(varde, forvantat):
    assert vind(varde) == forvantat


@pytest.mark.parametrize(
    "varde, forvantat",
    [
        pytest.param(1.2, "1,2 mm", id="nederbord"),
        pytest.param(0, "0,0 mm", id="ingen-nederbord"),
        pytest.param(15.75, "15,8 mm", id="avrundning"),
        pytest.param(None, SAKNAS, id="saknas"),
    ],
)
def test_nederbord(varde, forvantat):
    assert nederbord(varde) == forvantat

@pytest.mark.parametrize(
    "datum, forvantat",
    [
        pytest.param(date(2026,11,6),"Fredag 6 Nov",id="fredag"),
        pytest.param(date(2026,11,9),"Måndag 9 Nov",id="mandag-forsta-i-listan"),
        pytest.param(date(2027,1,3),"Söndag 3 jan",id="sondag-och-januari"),
        pytest.param(None,SAKNAS,id="saknas"),
    ])

def test_veckodag(datum,forvantat):
    assert veckodag(datum)==forvantat


import pytest   
from application.filter import temperatur

@pytest.mark.parametrize("varde,forvantat",[
    pytest.param(12.34, "12,3°C",id="avrundning"),
    pytest.param(5,"5,0°C",id="heltal"),
    pytest.param(-8.4,"-8,4°C",id="minus"),
    pytest.param(-0.04,"0,0°C",id="minus-noll"),
    pytest.param(None,"-",id="saknas"),
])
def test_temperatur(varde,forvantat):
    assert temperatur(varde)==forvantat
    
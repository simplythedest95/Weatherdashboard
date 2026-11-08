import pytest

from application.stader import STADER
from application.vader_api import VaderTjanstError


@pytest.mark.parametrize(
    "adress",
    [
        pytest.param("/", id="start"),
        pytest.param("/prognos?stad=Kiruna", id="prognos"),
        pytest.param("/prognos", id="fel-400"),
        pytest.param("/finns-inte", id="fel-404"),
    ],
)
def test_alla_sidor_anger_kalla(klient, mock_api, adress):
    html = klient.get(adress).get_data(as_text=True)
    assert "Open-Meteo" in html
    assert "CC BY 4.0" in html


def test_prognossidan_har_stadens_namn_i_titeln(klient, mock_api):
    html = klient.get("/prognos?stad=Kiruna").get_data(as_text=True)
    assert "<title>Kiruna" in html


@pytest.mark.parametrize(
    "adress, status, text",
    [
        pytest.param("/prognos", 400, "Välj en stad", id="stad-saknas"),
        pytest.param("/prognos?stad=", 400, "Välj en stad", id="tom-stad"),
        pytest.param(
            "/prognos?stad=Uppsala", 404, "Uppsala finns inte", id="okand-stad"
        ),
    ],
)
def test_prognos_med_felaktig_stad(klient, mock_api, adress, status, text):
    svar = klient.get(adress)
    assert svar.status_code == status
    assert text in svar.get_data(as_text=True)


def test_api_fel_ger_502_och_appen_lever(klient, monkeypatch):
    def trasigt_api(lat, lon):
        raise VaderTjanstError("Vädertjänsten svarar inte just nu.")

    monkeypatch.setattr("application.routes.hamta_prognos", trasigt_api)
    svar = klient.get("/prognos?stad=Kiruna")
    assert svar.status_code == 502
    assert "svarar inte" in svar.get_data(as_text=True)
    assert klient.get("/").status_code == 200


def test_startsidan_visar_alla_stader(klient):
    svar = klient.get("/")
    assert svar.status_code == 200
    html = svar.get_data(as_text=True)
    for stad in STADER:
        assert stad["namn"] in html


def test_okand_adress_ger_egen_404_sida(klient):
    svar = klient.get("/finns-inte")
    assert svar.status_code == 404
    assert "Sidan finns inte" in svar.get_data(as_text=True)


def test_filtren_ar_registrerade(app):
    for namn in ["temperatur", "vind", "nederbord", "veckodag"]:
        assert namn in app.jinja_env.filters

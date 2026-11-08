from application.stader import STADER


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
    for namn in ["temperatur","vind","nederbord","veckodag"]:
        assert namn in app.jinja_env.filters
        
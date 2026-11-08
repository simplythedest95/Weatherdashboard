# Väderappen

En Flask-app som visar vädret just nu och tre dagars prognos för fem svenska städer, med data från Open-Meteo. Byggd med testdriven utveckling (TDD).

## Funktioner

- Välj stad i en lista på startsidan
- Nuvarande temperatur, vind och väder med ikon
- Tre dagars prognos som kort och tabell
- Egna felsidor: 400 (ingen stad), 404 (okänd stad/sida), 502 (vädertjänsten svarar inte)

## Projektstruktur

- `application/` – appen (routes, API-anrop, tolkning, filter, mallar)
- `tests/` – pytest-tester, alla med mockat API

## Installation

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
python -m pip install -r requirements-dev.txt
```

## Köra appen

```bash
flask --app application run
```

Öppna http://127.0.0.1:5000

## Tester och kodkvalitet

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
```

Testerna gör inga nätverksanrop.

## Designbeslut

- **Tunna routes:** `routes.py` läser bara indata, anropar funktioner och väljer mall och statuskod. All logik ligger i egna moduler (`stader`, `vader_api`, `tolkning`, `filter`) som testas utan Flask och utan nätverk.
- **Statuskoder:** 400 när ingen stad valts (fel indata), 404 när staden eller sidan inte finns, och 502 när Open-Meteo inte svarar. 502 betyder att vår server fungerar men tjänsten bakom den svarar fel.
- **Egna felklasser:** alla requests-fel görs om till `VaderTjanstError`, och trasig data blir `OgiltigtSvarError` (som ärver från den). Då räcker det att routen fångar ett enda fel.
- **Gränsfall:** `zip(..., strict=True)` gör att listor av olika längd ger ett fel i stället för att dagar tyst försvinner. Ett saknat enstaka mätvärde (`None`) visas däremot som "–".
- **App-factory (`create_app`):** varje test får en ny, ren app.
- **Kodkvalitet:** ruff med kursens regler (E, F, I, N) plus B (vanliga buggar) och UP (modern syntax). B hittade till exempel att `zip` saknade `strict`.

## Frågor

### 1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde det?

Jag mockar anropen mot API:et i mina tester för att testerna blir snabba, ger samma resultat varje gång och de fungerar även utan åtkomst till internet. Utan mockning skulle testerna göra riktiga anrop. De skulle bli långsamma, faila utan internet eller när Open-Meteo har problem, och ge olika resultat beroende på dagens väder.

Som `mock_api` i min `conftest.py` som ersätter `hamta_prognos`, eller i `test_vader_api.py` där jag framkallar `Timeout` och `HTTPError` med `side_effect`. Fel som dessa skulle inte gå att få fram med ett riktigt API. Jag använde mig också av ett riktigt svar som jag sparat från API:et för att bygga min fixtur `exempelsvar`, så att mocken ska likna det verkliga API:et.

### 2. Vad gör timeout och raise_for_status(), och varför behövs de?

`timeout` bestämmer hur länge en request ska vänta på ett svar från servern. Om servern aldrig svarar väntar requests för alltid och sidan fryser, därför behövs timeout.

`raise_for_status()` gör att requests kastar ett fel om man får en statuskod i 400- eller 500-serien, till exempel 404 eller 500. Utan `raise_for_status()` försöker koden läsa felsvaret som om det vore riktig väderdata.

I `vader_api.py` har jag `TIMEOUT = 5`. Om servern inte svarar inom 5 sekunder kastar requests ett `Timeout`-fel. Det felet, och `HTTPError` från `raise_for_status()`, fångas i min `hamta_prognos` och görs om till `VaderTjanstError`, som routen visar som en 502-sida.

### 3. Hur fungerar mallarv i Jinja2? Förklara med exempel från dina egna mallar.

Mallar ärver struktur och innehåll från en gemensam "föräldermall", som min `base.html`. `base.html` innehåller det gemensamma (head, sidhuvud, sidfot) och definierar block. De andra mallarna skriver `{% extends "base.html" %}`, så att alla använder samma basmall och sidan behåller sitt grundutseende. "Barnmallarna" ersätter bara de block som de definierar. Block som de inte fyller får standardinnehållet från `base.html`.

Till exempel fyller `prognos.html` blocket `title` med stadens namn, medan startsidan inte har någon egen titel och därför får "Väderappen" som är definierad i `base.html`. Sidfoten med Open-Meteo finns bara i `base.html` men syns på alla sidor, och `test_alla_sidor_anger_kalla` bevisar det.

### 4. Vad är en fixture, och vilken använder du?

En fixture är förberedd testdata eller setup som pytest skickar in via parameternamnet. Jag använder `app`, `klient`, `exempelsvar` och `mock_api` i `conftest.py`.

Jag lärde mig också att fixtures kan bygga på varandra: min `klient` använder `app`, och min `mock_api` använder `exempelsvar`. Dessutom finns en inbyggd fixture som heter `monkeypatch`, som jag använder och som återställer det den ändrat efter testet.

## Källa

Väderdata från [Open-Meteo.com](https://open-meteo.com/), licens [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

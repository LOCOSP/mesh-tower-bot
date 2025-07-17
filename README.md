# Meshtastic Radio Python Control

Projekt umożliwia automatyczne i manualne sterowanie radiem Meshtastic podłączonym po USB z Pythona. Obsługuje zarówno wiadomości tekstowe, jak i automatyczne odpowiedzi na skonfigurowane komendy z sieci LoRa Mesh, korzystając z oficjalnej biblioteki Meshtastic.

---

## Spis treści

- [Meshtastic Radio Python Control](#meshtastic-radio-python-control)
  - [Spis treści](#spis-treści)
  - [Opis projektu](#opis-projektu)
  - [Funkcje](#funkcje)
  - [Wymagania](#wymagania)
  - [Instalacja](#instalacja)
  - [Szybki start](#szybki-start)
  - [Automatyczne komendy](#automatyczne-komendy)
  - [Konfiguracja uprawnień](#konfiguracja-uprawnień)
  - [Rozbudowa](#rozbudowa)
  - [Licencja](#licencja)

---

## Opis projektu

Skrypt łączy się automatycznie z radiem Meshtastic po USB i:
- odbiera komunikaty tekstowe z sieci mesh,
- pozwala wysyłać wiadomości ręcznie z linii poleceń,
- automatycznie reaguje na wybrane słowa-klucze (np. `maszt_info`, `maszt_status`, `maszt_pogoda`) udzielając konfigurowalnych odpowiedzi (status, uptime, liczba widocznych węzłów, aktualna pogoda w Opolu itp.).

Dzięki temu może służyć jako prywatny bot, maszt informacyjny, pogodynka lub interaktywny terminal Meshtastic.

---

## Funkcje

- **Odbiór wszystkich wiadomości** z sieci Meshtastic na Twój node.
- **Ręczne wysyłanie wiadomości** z linii poleceń (interaktywny chat LoRa).
- **Automatyczne odpowiedzi na komendy**:
    - `maszt_info`: nazwa bota, wersja, uptime, autor, lokalizacja
    - `maszt_status`: uptime, lokalizacja, liczba węzłów widzianych i bezpośrednich oraz wszystkich znanych
    - `maszt_pogoda`: dynamicznie pobierana aktualna pogoda w Opolu przez OpenWeatherMap
- **Przykład obsługi wielu słów-klucz**
- **Konfiguracja klucza API przez `.env`**
- **Modularność – łatwa rozbudowa o kolejne komendy**
- **Heurystyczne wyliczanie liczby bezpośrednich sąsiadów mesh**
- **Działa jednocześnie jako bot i terminal**

---

## Wymagania

- Python **3.8+**
- [meshtastic](https://github.com/meshtastic/python)
- `pypubsub`
- `requests`
- `python-dotenv`
- Konto i klucz API OpenWeatherMap (do funkcji pogody)
- Radio Meshtastic z firmware, podłączone do portu szeregowego (np. `/dev/ttyUSB0`)

---

## Instalacja

1. Sklonuj repozytorium:
```

git clone https://github.com/LOCOSP/mesh-tower-bot.git
cd mesh-tower-bot

```

2. **(Zalecane)** Stwórz środowisko wirtualne:
```

python3 -m venv venv
source venv/bin/activate

```

3. Zainstaluj zależności:
```

pip install meshtastic pubsub requests python-dotenv

```

4. Stwórz plik `.env` w katalogu projektu z zawartością:
```

OPENWEATHER_API_KEY=tu_wstaw_swoj_klucz_api

```

---

## Szybki start

1. Podłącz Meshtastic do USB.
2. Upewnij się, że Twój użytkownik ma prawo dostępu do portu (patrz: [Konfiguracja uprawnień](#konfiguracja-uprawnień)).
3. Uruchom:
```

python3 app.py

```
4. Wpisuj wiadomości lub wysyłaj komendy z aplikacji Meshtastic.

---

## Automatyczne komendy

- **maszt_info**  
Testowo zwraca:
```

nazwa: Meshtastic Tower Bot
wersja: 1.0
uptime: <czas>
autor: LSP
Lokalizacja: Opole

```
- **maszt_status**  
Testowo zwraca:
```

Maszt jest aktywny. Uptime: <czas>
Lokalizacja: JO80XQ42
Węzły w zasięgu (ostatnie 60s): <liczba>
Wszystkich węzłów: <liczba>

```
- **maszt_pogoda**  
Pobiera pogodę online i zwraca:
```

Maszt jest aktywny. Uptime: <czas>
Pogoda w Opole: Zachmurzenie umiarkowane, temp.: 21.4°C (odczuwalna 22.0°C), ciśnienie: 1011 hPa, wilgotność: 63%, wiatr: 3 m/s.
W sieci widocznych węzłów: <liczba>

```

---

## Konfiguracja uprawnień

Aby mieć dostęp do portu szeregowego (np. `/dev/ttyUSB0`), dodaj się do grupy `dialout`:
```

sudo usermod -a -G dialout \$USER

# Wyloguj się i zaloguj ponownie (lub zrestartuj komputer)

```

---

## Rozbudowa

Aby dodać nową komendę, edytuj sekcję słów kluczowych w funkcji `onReceive` w pliku `app.py`:

```

if message_string.strip().lower() == "nowa_komenda":
reply = "Moja nowa odpowiedź"
interface.sendText(reply, destinationId=dest_id)

```

Możesz łatwo dodać obsługę innych API, dowolne odpowiedzi czy kolejne integracje.

---

## Licencja

Projekt otwarty, przeznaczony do swobodnego wykorzystania.  
Meshtastic® jest zastrzeżonym znakiem towarowym Meshtastic LLC.  
Autorzy nie odpowiadają za wykorzystanie oprogramowania.

---
```
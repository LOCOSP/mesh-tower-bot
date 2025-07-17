# Meshtastic Radio Python Control

Projekt umożliwia automatyczne i interaktywne sterowanie radiem Meshtastic podłączonym przez port USB z poziomu Pythona. Obsługuje zarówno ręczne wiadomości tekstowe, jak i automatyczne odpowiedzi na wybrane komendy przez sieć LoRa Mesh, z użyciem oficjalnej biblioteki Meshtastic dla Pythona.

<img src="/media/demo.jpg" alt="Opis" width="200" height="300">

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
- automatycznie reaguje na wybrane słowa-klucze (np. `maszt_info`, `maszt_status`) udzielając konfigurowalnych odpowiedzi (status, uptime, liczba widocznych node’ów itp.).

Dzięki temu może służyć jako prywatny bot, maszt informacyjny lub interaktywny terminal dla sieci Meshtastic.

---

## Funkcje

- **Odbiór wszystkich wiadomości** z sieci Meshtastic na Twój node.
- **Ręczne wysyłanie wiadomości** z linii poleceń (interaktywny chat mesh przez LoRa).
- **Automatyczne odpowiedzi** na hasła:
    - `maszt_info`: nazwa oraz uptime urządzenia,
    - `maszt_status`: uptime i liczba ostatnio aktywnych węzłów w sieci,
    - łatwa rozbudowa o własne polecenia.
- **Działa w trybie ciągłym** — jednocześnie jako bot i terminal.

---

## Wymagania

- Python **3.8+**
- [meshtastic](https://github.com/meshtastic/python) (`pip install meshtastic`)
- `pypubsub` (`pip install pubsub`)
- Radio Meshtastic z firmware podłączone do portu szeregowego (np. `/dev/ttyUSB0` na Linuxie)

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

pip install meshtastic pubsub

```

---

## Szybki start

1. Podłącz urządzenie Meshtastic do portu USB.
2. Upewnij się, że Twój użytkownik ma prawo dostępu do portu (patrz: [Konfiguracja uprawnień](#konfiguracja-uprawnień)).
3. Uruchom skrypt:
```

python3 app.py

```
4. Wpisuj własne wiadomości w konsoli albo testuj z telefonu/aplikacji Meshtastic.

---

## Automatyczne komendy

Skrypt automatycznie odpowiada na wiadomości z określonym słowem kluczowym.  
Przykład domyślnych odpowiedzi:

- **maszt_info**  
Odpowiedź:  
`nazwa: Maszt Opole uptime: 1d 4h 12m 53s`

- **maszt_status**  
Odpowiedź:  
`Maszt aktywny. Uptime: 1d 4h 12m 53s. Bezpośrednio widocznych węzłów: 3`

Możesz samodzielnie modyfikować słowa kluczowe oraz treść odpowiedzi w kodzie źródłowym.

---

## Konfiguracja uprawnień

Aby mieć dostęp do portu szeregowego (np. `/dev/ttyUSB0`), dodaj się do grupy `dialout` i zrestartuj sesję:
```

sudo usermod -a -G dialout \$USER

# potem wyloguj się i zaloguj ponownie (lub zrestartuj komputer)

```

---

## Rozbudowa

Aby dodać nową komendę, edytuj funkcję obsługującą odbiór wiadomości w pliku `app.py`:

```

if message_string.strip().lower() == "twoje_haslo":
reply = "Twoja treść odpowiedzi"
interface.sendText(reply, destinationId=dest_id)

```

Możesz też zmienić nazwę, uptime, dodać własne polecenia lub logikę bota.

---

## Licencja

Projekt otwarty, przeznaczony do swobodnego wykorzystania.  
Meshtastic® jest zastrzeżonym znakiem towarowym Meshtastic LLC.  
Autorzy nie odpowiadają za wykorzystanie oprogramowania.
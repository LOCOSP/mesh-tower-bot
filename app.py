import meshtastic.serial_interface
from pubsub import pub
import time
import os
import requests
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Start służy do liczenia uptime
start_time = time.time()

# Inicjalizacja połączenia z radiem
interface = meshtastic.serial_interface.SerialInterface()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {secs}s"

# Heurystyczna funkcja wyciągająca bezpośrednich sąsiadów
def get_direct_neighbors(interface, threshold=60):
    now = time.time()
    direct = [
        nodeid for nodeid, node in interface.nodes.items()
        if node.get('lastHeard') and (now - node['lastHeard']) < threshold
    ]
    return direct

# Pobranie pogody z OpenWeatherMap
def get_opole_weather():
    if not OPENWEATHER_API_KEY:
        return "Brak klucza API do pogody."
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            "?lat=50.6751&lon=17.9213"
            f"&appid={OPENWEATHER_API_KEY}&units=metric&lang=pl"
        )
        response = requests.get(url, timeout=7)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            return f"Błąd pobierania pogody: {data.get('message', 'Nieznany błąd')}"
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind = data.get("wind", {}).get("speed", 0)
        city = data.get("name", "Opole")

        return (
            f"Pogoda w {city}: {desc}, temp.: {temp:.1f}°C (odczuwalna {feels:.1f}°C), "
            f"ciśnienie: {pressure} hPa, wilgotność: {humidity}%, wiatr: {wind} m/s."
        )
    except Exception as e:
        return f"Błąd pobierania pogody: {e}"

# Funkcja wywoływana po odebraniu wiadomości
def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            # Pobranie tekstu wiadomości
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"Odebrano: {message_string}\n> ", end="", flush=True)

            # Automatyczne odpowiedzi na słowa kluczowe
            if message_string.strip().lower() == "maszt_info":
                uptime_str = format_uptime(time.time() - start_time)
                reply = (
                    f"nazwa: Meshtastic Tower Bot\n"
                    f"wersja: 1.0\n"
                    f"uptime: {uptime_str}\n"
                    f"autor: LSP\n"
                    f"Lokalizacja: JO80XQ42"
                )
                dest_id = packet.get("fromId")
                interface.sendText(reply, destinationId=dest_id)

            elif message_string.strip().lower() == "maszt_status":
                uptime_str = format_uptime(time.time() - start_time)
                node_count = len(interface.nodes)
                direct_count = len(get_direct_neighbors(interface))
                reply = (
                    f"Maszt jest aktywny. Uptime: {uptime_str}.\n"
                    f"Lokalizacja: JO80XQ42\n"
                    f"Węzły w zasięgu (ostatnie 60s): {direct_count}\n"
                    f"Wszystkich węzłów: {node_count}"
                )
                dest_id = packet.get("fromId")
                interface.sendText(reply, destinationId=dest_id)

            elif message_string.strip().lower() == "maszt_pogoda":
                uptime_str = format_uptime(time.time() - start_time)
                pogoda = get_opole_weather()
                node_count = len(interface.nodes)
                reply = (
                    f"Maszt jest aktywny. Uptime: {uptime_str}.\n"
                    f"{pogoda}\n"
                    f"W sieci widocznych węzłów: {node_count}"
                )
                dest_id = packet.get("fromId")
                interface.sendText(reply, destinationId=dest_id)

    except Exception as e:
        print(f"Błąd podczas obsługi pakietu: {e}")

# Subskrypcja zdarzenia odbioru wiadomości
pub.subscribe(onReceive, 'meshtastic.receive')

def send_message(message):
    interface.sendText(message)

# Główna pętla: nadal możesz pisać z klawiatury
while True:
    text = input("> ")
    send_message(text)

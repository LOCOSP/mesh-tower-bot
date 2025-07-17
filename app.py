import meshtastic.serial_interface
from pubsub import pub
import time

# Start timestamp (do liczenia uptime)
start_time = time.time()

# Inicjalizacja połączenia z radiem
interface = meshtastic.serial_interface.SerialInterface()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {secs}s"

# Funkcja do pobrania bezpośrednich sąsiadów
# (węzłów, które wysłały coś w ciągu ostatnich 60 sekund)
def get_direct_neighbors(interface, threshold=60):
    now = time.time()
    direct = [
        nodeid for nodeid, node in interface.nodes.items()
        if node.get('lastHeard') and (now - node['lastHeard']) < threshold
    ]
    return direct


# Funkcja wywoływana po odebraniu wiadomości
def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            # Pobranie tekstu wiadomości
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"Odebrano: {message_string}\n> ", end="", flush=True)

            # Sprawdź słowa kluczowe i odpisz automatem
            if message_string.strip().lower() == "maszt_info":
                uptime_str = format_uptime(time.time() - start_time)
                reply = f"nazwa: Meshtastic Tower Bot\n" \
                        f"wersja: 1.0\n" \
                        f"uptime: {uptime_str}\n" \
                        f"autor: LSP\n" \
                        f"Lokalizacja: Opole "
                # Odpowiedz tylko nadawcy (private), jeśli masz jego fromId
                dest_id = packet.get("fromId")  # lub użyj broadcast jeśli zawsze public
                interface.sendText(reply, destinationId=dest_id)
            elif message_string.strip().lower() == "maszt_status":
                uptime_str = format_uptime(time.time() - start_time)
                node_count = len(interface.nodes)   # liczba widocznych wtedy węzłów
                reply = f"Maszt jest aktywny. Uptime: {uptime_str}. \n" \
                        f"Lokalizacja: JO80XQ42 \n" \
                        f"Węzły w zasięgu: {len(get_direct_neighbors(interface))} \n" \
                        f"Wszystich węzłów: {node_count} \n" 
                        
                dest_id = packet.get("fromId")
                interface.sendText(reply, destinationId=dest_id)

    except Exception as e:
        print(f"Błąd podczas obsługi pakietu: {e}")

# Subskrypcja zdarzenia odbioru wiadomości
pub.subscribe(onReceive, 'meshtastic.receive')

def send_message(message):
    interface.sendText(message)

# Główna pętla: dalej można pisać z klawiatury
while True:
    text = input("> ")
    send_message(text)

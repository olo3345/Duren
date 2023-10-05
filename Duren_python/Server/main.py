import socket, threading, datetime, json, random

with open(r"C:\Users\Ja\Desktop\moje_pliki\Programowanie\Duren\Duren_python\Server\config.json", "r") as json_config_file:
    data = dict(json.load(json_config_file))
    HOST = data.get("host")
    PORT = data.get("port")
    ADDR = (HOST, PORT)
    HEADER = data.get("header")
    FORMAT = data.get("format")
    CARDS = dict(data.get("cards"))
    CARD_TYPES = CARDS.get("types")
    CARD_VALUES = CARDS.get("values")
    DATE_TIME_FORMAT = data.get("date_time_format")
    DISCONNECT_MESSAGE = data.get("disconnect_message")
    UPDATE_MESSAGE = data.get("update_string")
    #HOST = socket.gethostbyname(socket.gethostname())
active_connections_list = []    
players_cards = {}
used_cards = []
turn = int()
formated_current_date_time = datetime.datetime.now().strftime(DATE_TIME_FORMAT)
server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def chekIfSpecificStrInDict(dict_to_be_checked : dict, target_string : str):
    for key, value in dict_to_be_checked.items():
        for item in value:
            if target_string in item:
                return True
    return False
def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b" "*(HEADER - len(send_lenght))
    conn.send(send_lenght)
    conn.send(message)
def deal_card(addres):
    while True:
        card_type = random.choice(CARD_TYPES)      
        card_value = random.choice(CARD_VALUES) 
        card = f'{card_type}_{card_value}'
        if not chekIfSpecificStrInDict(players_cards, card):
            if card not in used_cards:
                players_cards[addres].update({card : addres})
                return                    
def deal_cards():
    for i in range(len(active_connections_list)):
        for i2 in range(6):
            deal_card(active_connections_list[i])
def client_handlerer(conn, addr):
    global active_connections_list
    if len(active_connections_list) > 6:
        send(f'%{DISCONNECT_MESSAGE}', conn)
        active_connections_list.remove(addr)
        print(f'[{formated_current_date_time}][SERVER][INFO] Client {addr} connection rejected, connection limit')
        return
    else:
        send("hello", conn)
        print(f'[{formated_current_date_time}][SERVER][INFO] Client {addr} succesfully connected, now at {len(active_connections_list)} connections')
    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f'[{formated_current_date_time}][{addr}][INFO] Disconnnected')
                active_connections_list.remove(addr)
                break
            else:
                print(f'[{formated_current_date_time}][{addr}][MSG] {msg}')       
    conn.close()   
def start():
    print(f'[{formated_current_date_time}][SERVER][INFO] Starting...')
    print(f'[{formated_current_date_time}][SERVER][INFO] Using time stamp format {DATE_TIME_FORMAT}')
    global active_connections_list
    server.listen()
    print(f'[{formated_current_date_time}][SERVER][INFO][LISTENER] Listening on {HOST}:{PORT}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = client_handlerer, args = (conn, addr)) 
        active_connections_list.append(addr)
        thread.start()
        
def start_game():
    pass
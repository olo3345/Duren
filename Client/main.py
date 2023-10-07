import socket, datetime, json

class Player():
    def __init__(self):
        self.cards = list()
    def set_cards(self, cards : list = None):
        if cards != None:
            self.cards.clear()
            self.cards.extend(cards)
    @property
    def getCards(self):
        return self.cards


with open(r"/Client/config.json", "r") as f:
    data = dict(json.load(f))
    SERVER = data.get("default_server_ip")
    PORT = data.get("default_server_port")
    ADDR = (SERVER, PORT)
    HEADER = data.get("header")
    FORMAT = data.get("format")
    DISCONNECT_MESSAGE = data.get("disconnect_message")
    UPDATE_MESSAGE = data.get("update_string")
    DATE_TIME_FORMAT = data.get("date_time_format")
formated_current_date_time = datetime.datetime.now().strftime(DATE_TIME_FORMAT)

player = Player
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg : str):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b" "*(HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
def uptade_ping():
    global player
    send(UPDATE_MESSAGE)
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)
        data = dict(json.load(msg))
        player.set_cards(data["cards"])        
def connect(addres: tuple = ADDR):
    if addres == ADDR:
        print(f'[{formated_current_date_time}][Client][INFO] Connecting to the default server')
    else:
        print(f'[{formated_current_date_time}][Client][INFO] Connecting to {addres}')
    client.connect(ADDR)
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)
        if msg == f'${DISCONNECT_MESSAGE}':
            print(f'[{formated_current_date_time}][Client][Info] Got disconected by the server') 
            return
        else:
            print(f'[{formated_current_date_time}][Client][Info] Connected succesfully')                             
def disconnect():
    send(DISCONNECT_MESSAGE)

connect(ADDR)
send(input("send :"))
import socket, datetime, json

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

DEBUG = True
def do_print(print_args : tuple): # debugOnly_print
    if DEBUG == True:
        print(print_args)  
 
SERVER = "192.168.1.208"
PORT = 5000
ADDR = (SERVER, PORT)
HEADER = 4096
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "$DISCONNECT"
UPDATE_MESSAGE = "$UPDATE"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
formated_current_date_time = datetime.datetime.now().strftime(DATE_TIME_FORMAT)
player_cards = []
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def set_cards(cards : list = None):
    global player_cards
    if cards != None:
        player_cards.clear()
        player_cards.extend(cards)
def send(msg : str):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b" "*(HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
def uptade_ping():
    global player_cards
    send(UPDATE_MESSAGE)
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)
        data = dict(json.load(msg))
        set_cards(data["cards"])        
def connect(addres : tuple = ADDR, userName : dict = {"userName" : "p1"}):
    if addres == ADDR:
        do_print(f'[{formated_current_date_time}][Client][INFO] Connecting to the default server')
    else:
        do_print(f'[{formated_current_date_time}][Client][INFO] Connecting to {addres}')
    client.connect(ADDR)
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)
        if msg == f'${DISCONNECT_MESSAGE}':
            do_print(f'[{formated_current_date_time}][Client][Info] Got disconected by the server') 
            return
        else:
            do_print(f'[{formated_current_date_time}][Client][Info] Connected succesfully')
            send(json.dumps(userName))                           
def disconnect():
    send(DISCONNECT_MESSAGE)

kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()
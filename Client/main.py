import socket, datetime, json

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

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
USER_NAME_EXISTS_MSG = "$USERNAMEEXISTS"
CONNECTED: bool = False
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
    global CONNECTED
    try:
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
                CONNECTED = False
                return 
            else:
                do_print(f'[{formated_current_date_time}][Client][Info] Connected succesfully')
                send(json.dumps(userName))
                while True:
                    msg_lenght = client.recv(HEADER).decode(FORMAT)
                    if msg_lenght:
                        msg_lenght = int(msg_lenght)
                        msg = client.recv(msg_lenght).decode(FORMAT)
                        if msg != USER_NAME_EXISTS_MSG:
                            CONNECTED = True
                            return
    except:
        show_popup()
        return "Error"        
                        
                                    
def disconnect():
    send(DISCONNECT_MESSAGE)

class Widget(Widget):
    def btn(self):
        show_popup()
class P0(GridLayout):
    pass
class StartWindow(Screen):
    def next(_, ip: str, port: int, username:str):
        _Username = {"userName" : f"{username}"}
        connect((ip, port), _Username)
        return CONNECTED
        
class MainWindow(Screen):
    def disconnect(_):
        if CONNECTED:
            disconnect()
            
class HostYourOwn(Screen):
    pass
class WindowManager(ScreenManager):
    pass

def show_popup():
    show = P0()
    popupWindow = Popup(title = "Error", content = show)
    popupWindow.open()

kv = Builder.load_file("Duren.kv")

class DurenApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    DurenApp().run()
    input("Press enter to exit")
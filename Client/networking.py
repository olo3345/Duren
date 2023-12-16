from main import do_print, show_popup_0, set_cards
from datetime import datetime
import json

HEADER = 4096
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "$DISCONNECT"
UPDATE_MESSAGE = "$UPDATE"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
USER_NAME_EXISTS_MSG = "$USERNAMEEXISTS"
formated_current_date_time = datetime.now().strftime(DATE_TIME_FORMAT)
    
def send(client, msg : str):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b" "*(HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)

def uptade_ping(client):
    send(UPDATE_MESSAGE)
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = client.recv(msg_lenght).decode(FORMAT)
        data = dict(json.load(msg))
        set_cards(data["cards"])
       
def connect(client, addres : tuple, userName : dict = {"userName" : "p1"}):
    global CONNECTED
    try:
        do_print(f'[{formated_current_date_time}][Client][INFO] Connecting to {addres}')
        client.connect(addres)
        msg_lenght = client.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = client.recv(msg_lenght).decode(FORMAT)
            if msg == f'%{DISCONNECT_MESSAGE}':
                do_print(f'[{formated_current_date_time}][Client][Info] Got disconected by the server')
                CONNECTED = False
                return 
            else:
                do_print(f'[{formated_current_date_time}][Client][Info] Connected succesfully')
                i = 2
                send(json.dumps(userName))
                while True:
                    msg_lenght = client.recv(HEADER).decode(FORMAT)
                    if msg_lenght:
                        msg_lenght = int(msg_lenght)
                        msg = client.recv(msg_lenght).decode(FORMAT)
                        if msg != USER_NAME_EXISTS_MSG:
                            CONNECTED = True
                            return
                        else:
                            send(json.dumps(f'{userName}({i})'))
                    i += 1 
                
    except:
        show_popup_0()
        return "Error"        
                                        
def disconnect(client):
    global CONNECTED
    CONNECTED = False
    send(client, DISCONNECT_MESSAGE)
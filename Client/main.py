import socket, webbrowser
from networking import send, disconnect, connect

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

DEBUG = True
def do_print(print_args : tuple): # debugOnly_print
    if DEBUG == True:
        print(print_args)  
 
CONNECTED: bool = False
player_cards = []
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def set_cards(cards : list = None):
    global player_cards
    if cards != None:
        player_cards.clear()
        player_cards.extend(cards)
        
class StartWindow(Screen):
    def next(_, ip: str, port: int, username:str):
        if ip != "":
            if port != "": 
                _Username = {"userName" : f"{username}"}
                if _Username["userName"] == "":
                    connect(client, (ip, port))
                else:
                    connect(client, (ip, port), _Username)
                return CONNECTED
            else:
                show_popup_0()
        else:
            show_popup_0()
            
        
class MainWindow(Screen):
    def disconnect(_):
        if CONNECTED:
            disconnect(client)
            
class HostYourOwn(Screen):
    def displayWebsite(_):
        webbrowser.open("https://github.com/olo3345/Duren")
        # TODO: implement self hosting tutorial     
class WindowManager(ScreenManager):
    pass

def show_popup_0():
    btn = Button(text = "ok")
    content = GridLayout(cols = 1)
    content.add_widget(Label("The server addres is not correct or the server is offline."))
    content.add_widget(btn)
    popup = Popup(title = "Error", content = content, auto_dismiss = False)
    btn.bind(on_press=popup.dismiss)
    popup.open()

kv = Builder.load_file("Duren.kv")

class DurenApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    DurenApp().run()
    input("Press enter to exit")
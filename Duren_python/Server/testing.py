import random, json

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

players_cards = {}
used_cards  = []
active_connections_list = [("ip_addrres0", "port0"), ("ip_addrres1", "port1"), ("ip_addrres2", "port2"), ("ip_addrres3", "port3"), ("ip_addrres4", "port4"), ("ip_addrres5", "port5"),]

def chekIfSpecificStrInDict(dict_to_be_checked : dict, target_string : str):
    for key, value in dict_to_be_checked.items():
        for item in value:
            if target_string in item:
                return True
    return False
def deal_card(addres):
    while True:
        card_type = random.choice(CARD_TYPES)      
        card_value = random.choice(CARD_VALUES) 
        card = f'{card_type}_{card_value}'
        if not chekIfSpecificStrInDict(players_cards, card):
            if card not in used_cards:
                if addres in players_cards.keys():
                    addreses_cards = players_cards[addres]
                    addreses_cards.append(card)
                    return
                else:
                    players_cards.update({addres : [card]})
                    return                   
def deal_cards():
    for i in range(len(active_connections_list)):
        for i2 in range(6):
            deal_card(active_connections_list[i])

deal_cards()
print(players_cards)
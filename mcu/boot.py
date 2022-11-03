import gc
import ujson
import esp
import ubinascii
import machine
import network

from umqttsimple import MQTTClient

esp.osdebug(None)
gc.collect()

config = open("config.json").read()

ssid = config["ssid"]
ssid_password = config["ssid_password"]
mqtt_address = config["mqtt_address"]
mqtt_port = config["mqtt_port"]
mqtt_user = config["mqtt_user"]
mqtt_password = config["mqtt_password"]

client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = b"door/comandos"

last_msg = 0
message_interval = 1

try:
    print("Iniciando leitura...")
    
    arq = open("ID.json").read()
    
    print("Lista de IDs encontrada com sucesso!")

except:
    print("Nao foi possivel ler lista de IDs")
    print("Criando lista de IDs")
    
    arq = open("ID.json","w")
    
    print("Lista de IDs criada com sucesso!")
    
    arq.close()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():

    print("Conectando com o WIFI...")

    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        pass
    
    print("Rede conectada: ", wlan.ifconfig())

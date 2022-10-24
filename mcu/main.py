
from porteiro import RFiDPorteiro as rf
from database import Database as db

from machine import Pin
from umqttsimple import MQTTClient

import time
import network

configMode = False

ssid = "SSID_DA_REDE"
ssid_pw = "SENHA_DA_REDE"

mqtt_client = "Door"
mqtt_address = "MQTT_ADDRESS"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Conectando com o WIFI...")
    wlan.connect(ssid, ssid_pw)
    
    while not wlan.isconnected():
        pass
    
    print('Rede:', wlan.ifconfig())

mqtt_logs = "door/logs"
mqtt_heartbeat = "door/heartbeat"
mqtt_nomes = "door/nomes"

# Tópico do MQTT #

topics = [b"door/comandos", b"door/cadastro"]

mqtt_comandos = b"door/comandos"
mqtt_cadastro = b"door/cadastro"

client = MQTTClient(mqtt_client, mqtt_address)

def sub_cb(topic, msg):

    if topic == mqtt_comandos and msg == b'restart':
        print("Comando de restart recebido")

        time.sleep(20)

        machine.reset()
    
    if topic == mqtt_comandos and msg == b'keepalive':
        print("Comando de keep alive recebido")

        client.publish(mqtt_heartbeat, "Heartbeat: {}".format(time.time()))
    
    if topic == mqtt_comandos and msg == b'abrir':
        print("Comando de abrir porta recebido")

        rele.value(1)

        time.sleep_ms(3000)

        rele.value(0)
    
    if topic == mqtt_comandos and msg == b'fechar':
        print("Comando de fechar porta recebido")

        rele.value(0)
    
    if topic == mqtt_cadastro and msg == b'cadastro':
        print("Comando de requisicao de cadastro recebido")

        configMode = True

try:
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(topics)
except OSError as e:
    time.sleep(10)

    machine.reset()

client.publish(mqtt_logs, "Porta conectada em " + ssid + " com sucesso, servidor MQTT estabelecido!")

# Rele #

rele = Pin(2, Pin.OUT)

# Definindo #

db = db()
rf = rf()

def grant(delay, tag):
    
    rele.value(1)
    
    client.publish(mqtt_logs, "A porta foi aberta por " + tag + " com sucesso")
    
    time.sleep(delay)

def deny(tag):
    rele.value(0)
    
    client.publish(mqtt_logs, "O cartao de ID " + tag + " tentou entrar porem sem permissao")
    
    time.sleep(3)

while True:

    cardTag = str(rf.get())
    
    client.publish(mqtt_logs, "A porta foi fechada com sucesso!")
    client.publish(mqtt_heartbeat, "Heartbeat: {}".format(time.time()))

    while (cardTag == "SemTag"):
        
        rele.value(0)
            
        cardTag = str(rf.get())
    
    if configMode == True:
        
        if db.IsMaster(cardTag):
            print("Saindo do modo config!")
            
            client.publish(mqtt_logs, "Modo configuracao desabilitado!")
                
            configMode = False
            
        else:
            if db.findCard(cardTag)[0]:
                print("Cartao reconhecido, removendo...")
                
                client.publish(mqtt_logs, "Cartao " + cardTag + " removido da memoria!")
                
                db.removeCard(cardTag)
                
                time.sleep_ms(3000)
                
                print("Aproxime um cartao para adicionar ou remover")
                
            else:
                
                print("Cartao desconhecido, adicionando...")
                
                client.publish(mqtt_logs, "Cartao " + cardTag + " adicionado na memoria!")
                
                db.addCard(cardTag, input("Nome do holder "))
                
                time.sleep_ms(3000)
                
                print("Aproxime um cartao para adicionar ou remover")
    else:
        
        if db.IsMaster(cardTag):
            configMode = True
            
            print("Modo configuracao ativado")
            
            client.publish(mqtt_logs, "O modo de configuracao da porta foi habilitado!")
            
            time.sleep_ms(2000)
            
            amount = db.amount()
            
            print("Cartoes na memoria", amount, "!")
            
            client.publish(mqtt_logs, "Atualmente ha " + str(amount) + " cartoes registrados na memoria!")
            
            time.sleep_ms(1000)
            
            print("Leia um cartao para ADICIONAR ou REMOVER da memoria")
            
            client.publish(mqtt_logs, "A porta esta solicitando um cartao para ser ADICIONADO ou REMOVIDO")
            
        else:
            if db.findCard(cardTag)[0]:
                grant(3, cardTag)
            else:
                deny(cardTag)
    


    


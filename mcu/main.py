
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
    
client = MQTTClient(mqtt_client, mqtt_address)
client.connect()

client.publish(mqtt_logs, "Porta conectada em " + ssid + " com sucesso, servidor MQTT estabelecido!")

rele = Pin(2, Pin.OUT)

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

def current_milli_time():
    return round(time.time() * 1000)
    
while True:
    
    client.check_msg()
    
    cardTag = str(rf.get())
    
    client.publish(mqtt_logs, "A porta foi fechada com sucesso")
    
    while (cardTag == "SemTag"):
        
        client.publish(mqtt_heartbeat, "Heartbeat: {}".format(current_milli_time()))
        
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
            
            client.publish(mqtt_logs, "Modo de configuracao habilitado!")
            
            time.sleep_ms(2000)
            
            amount = db.amount()
            
            print("Cartoes na memoria", amount, "!")
            
            client.publish(mqtt_logs, "Cartoes que estao adicionados na memoria: " + str(amount) + "!")
            
            time.sleep_ms(1000)
            
            print("Modo de ADICIONAR ou REMOVER habilitado")
            
            client.publish(mqtt_logs, "Leia um cartao para ADICIONAR ou REMOVER da memoria")
            
        else:
            if db.findCard(cardTag)[0]:
                grant(3, cardTag)
            else:
                deny(cardTag)
    


    


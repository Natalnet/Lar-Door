
from porteiro import RFiDPorteiro as rf
from database import Database as db

from machine import Pin
from umqttsimple import MQTTClient

import time

configMode = False

global_contador = 0

mqtt_logs = b"door/logs"
mqtt_heartbeat = b"door/heartbeat"
mqtt_nomes = b"door/nomes"
mqtt_estado = b"door/estado"

def connect_and_subscribe():
    global client_id, mqtt_address, mqtt_port, topic_sub, ssid

    client = MQTTClient(client_id, mqtt_address, mqtt_port)

    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)

    client.publish(mqtt_logs, "Conectado do MQTT de IP " + mqtt_address + " com sucesso!")

    print("Conectado ao MQTT Broker de IP %s, lendo os topicos %s" % (mqtt_address, topic_sub))

    return client

def restart_and_reconnect():
    print("Ocorreu um erro ao se conectar com o broker, tentando reconexao.")

    time.sleep(10)

    machine.reset()

def sub_cb(topic, msg):
    global topic_sub

    if topic == topic_sub and msg == b'restart':
        print("Comando de restart recebido")

        client.publish(mqtt_logs, "Comando de restart recebido, reiniciando o ESP.")

        time.sleep(20)

        machine.reset()
    
    if topic == topic_sub and msg == b'keepalive':
        print("Comando de keep alive recebido")

        client.publish(mqtt_logs, "Comando de keep alive recebido, enviando ultimo heartbeat.")

        client.publish(mqtt_heartbeat, "Heartbeat: {}".format(time.time()))
    
    if topic == topic_sub and msg == b'abrir':
        print("Comando de abrir porta recebido")

        client.publish(mqtt_logs, "Comando de abrir porta recebido, porta foi aberta")

        client.publish(mqtt_estado, "aberta")

        rele.value(0)

        time.sleep(3)

        rele.value(1)

    if topic == topic_sub and msg == b'fechar':
        print("Comando de fechar porta recebido")

        client.publish(mqtt_logs, "Comando de fechar porta recebido, porta foi fechada")

        client.publish(mqtt_estado, "fechada")

        rele.value(1)
    
    if topic == topic_sub and msg == b'panic':
        print("Comando de panic recebido")

        client.publish(mqtt_logs, "Comando de panic mode recebido, a porta esta sendo desligada")

        client.publish(mqtt_estado, "panic mode")

        rele.value(0)

        time.sleep(9999)

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

rele = Pin(2, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP)

db = db()
rf = rf()

def grant(delay, name):
    
    rele.value(0)
    
    client.publish(mqtt_nomes, name)
    
    time.sleep(delay)

def deny(tag):
    rele.value(1)
    
    client.publish(mqtt_logs, "O cartao de ID " + tag + " tentou entrar porem sem permissao.")
    
    time.sleep(3)

def program():
    rele.value(0)

    client.publish(mqtt_estado, "configuracao")

def normal():
    rele.value(1)

    client.publish(mqtt_estado, "normal")

def keepalive():

    client.check_msg()
 
    if (time.time() - last_msg):
        client.publish(mqtt_heartbeat, f"Hearbeat: {global_contador}")
    
    last_msg = time.time()

    global_contador += 1

while True:

    cardTag = str(rf.get())
    
    client.publish(mqtt_estado, "fechada")

    while (cardTag == "SemTag"):

        keepalive()

        if configMode == True:
            program()
        else:
            normal()

        rele.value(1)
            
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
                
                time.sleep(3)
                
                print("Aproxime um cartao para adicionar ou remover.")
                
            else:
                
                print("Cartao desconhecido, adicionando...")

                db.addCard(cardTag, input("Nome do holder "))

                client.publish(mqtt_logs, "Cartao " + cardTag + " adicionado na memoria!")
                
                time.sleep(3)
                
                print("Aproxime um cartao para adicionar ou remover.")
    else:
        
        if db.IsMaster(cardTag):
            configMode = True
            
            print("Modo configuracao ativado.")
            
            client.publish(mqtt_logs, "O modo de configuracao da porta foi habilitado!")
            
            time.sleep(2)
            
            amount = db.amount()
            
            print("Cartoes na memoria", amount, "!")
            
            client.publish(mqtt_logs, "Atualmente ha " + str(amount) + " cartoes registrados na memoria!")
            
            time.sleep(1)
            
            print("Leia um cartao para ADICIONAR ou REMOVER da memoria")
            
            client.publish(mqtt_logs, "A porta esta solicitando um cartao para ser ADICIONADO ou REMOVIDO")
            
        else:
            if db.findCard(cardTag)[0]:
                name = db.findName(cardTag)
                
                grant(3, name)
            else:
                deny(cardTag)
    


    


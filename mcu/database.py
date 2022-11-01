from porteiro import RFiDPorteiro as rf

import ujson
import time

class Database:


    def __init__(self):
        print("Database iniciada com sucesso")
        
        
        try:
            arq = open("ID.json").read()
            
            arqload = ujson.loads(arq)
            arqload[0]["ID"]

        except:
            
            print("E necessario definir um cartao mestre, encoste o cartao: ")
            
            arq = open("ID.json","w")
            
            while(True):
                time.sleep_ms(100)
                IdMaster = str(rf.get())

                if IdMaster != "SemTag":
                    break

            data = [{"ID":IdMaster, "NOME":"Master"}]
            
            arq.write(ujson.dumps(data))
            arq.close()

    def findCard(self, tag):

        arq = open("ID.json").read()  
        arqload = ujson.loads(arq)  
        amount = int(len(arqload))

        findTag = tag
        
        for i in range (amount):
            
            if arqload[i]["ID"] == findTag:
                return (True,i)
            
        return (False,i)
    
    def findName(self, tag):

        arq = open("ID.json").read()
        arqload = ujson.loads(arq)
        amount = int(len(arqload))

        findTag = tag

        for i in range (amount):

            if arqload[i]["ID"] == findTag:
                name = arqload[i]["NOME"]
                
                return name

        return "SemTag"
    
    def addCard(self, tag, nome):
        if self.findCard(tag)[0] == False:
            
            arq = open("ID.json").read()
            
            arqload = ujson.loads(arq)
            newdata = {"ID":tag, "NOME":nome}
            
            arqload.append(newdata)
            
            arq = open("ID.json","w")
            arq.write(ujson.dumps(arqload)) 
            arq.close()
            
            print("Cartao cadastrado", tag, " com sucesso")
            
        else:
            
            print("Cartao ja esta cadastrado")

    
    def removeCard(self,tag):

        pos = int(self.findCard(tag)[1])
        
        arq = open("ID.json").read()
        
        arqload = ujson.loads(arq)
        arqload.pop(pos)
        
        arq = open("ID.json","w")
        
        arq.write(ujson.dumps(arqload))  
        arq.close()
        
        print("Cartao removido", tag, " com sucesso")

    def IsMaster(self,tag):

        arq = open("ID.json").read()
        arqload = ujson.loads(arq)
        print(arqload[0]["ID"])
        
        if arqload[0]["ID"] == tag:
            return True
        else:
            return False
        
    def amount(self):
        arq = open("ID.json").read()
        
        arqload = ujson.loads(arq)
        
        amount = int(len(arqload))
        
        return amount


import gc
import ujson

gc.collect()

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

import mfrc522

from machine import Pin
from machine import SPI

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()

rdr = mfrc522.MFRC522(spi=spi, gpioRst=4, gpioCs=5)

class RFiDPorteiro:

    def __init__(self):
        print ("RFiD Iniciado com sucesso.")

    def get(self):
        tag = "SemTag"
        
        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:

            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                print(str(raw_uid[0])+ str(raw_uid[1]) + str(raw_uid[2])+ str(raw_uid[3]))
                
                if rdr.select_tag(raw_uid) == rdr.OK:
                    tag = str(raw_uid[0])+ str(raw_uid[1]) + str(raw_uid[2])+ str(raw_uid[3])
                else:
                    return tag
        return tag


    def key(self,tags):
        try:
            tag = self.get()
        except KeyboardInterrupt:
            tag = '12345'
            
        if tag in tags:
            return True
        else:
            return False
         




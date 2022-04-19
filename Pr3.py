import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from multiprocessing import Lock,Condition, Manager
from multiprocessing import Value
from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array,
from monitor import Table
NPHIL = 5
Phil_names = [Sócrates, Platón, Tales, Heráclito, Aristóteles]
K = 100

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Philosofer")
client.connect(mqttBroker)

"""
while True:
    u = 2
    client.publish("Temperature",u)
    print("JUST PUBLISHED" + str(u) + "to Topic Temperature")
    time.sleep(1)
    
while True:
    manager = Manager()
    table = Table(NPHIL, manager)
    philosofers = [Process(target=philosopher_task, args=(i,table)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()
"""

def delay(n):
    time.sleep(random.random()/n)
    
def philosopher_task(num:int, table: Table):
    table.set_current_phil(num)
    topic = input("¿A qué mesa desea suscribirse? ")
    client.loop_start()
    client.subscribe(topic)
    client.on_message = on_message
    print(on_message)
    client.publish("Philosofer {Phil_names[num]} thinking")
    print (f"Philosofer {Phil_names[num]} thinking")
    client.publish("Philosofer {Phil_names[num]} wants to eat")
    #Falta publish en el canal de la mesa
    print (f"Philosofer {Phil_names[num]} wants to eat")
    if on_message == f"Philosofer {Phil_names[num]} eating":
        time.sleep(1)
    client.publish("Philosofer {Phil_names[num]} wants to stop eating")
    print (f"Philosofer {Phil_names[num]} wants to stop eating")
    
    
""" 
    while True:
        print (f"Philosofer {Phil_names[num]} thinking")
        print (f"Philosofer {Phil_names[num]} wants to eat")
        table.wants_eat(Phil_names[num])
        print (f"Philosofer {Phil_names[num]} eating")
        table.wants_think(Phil_names[num])
        print (f"Philosofer {Phil_names[num]} stops eating")
"""

class Table():
    def __init__(self, nphil, manager):
        self.mutex=Lock()
        self.manager = manager
        self.eaters = self.manager.list()
        self.nphil = nphil
        self.free_fork = Condition(self.mutex)
        self.eating = Value('i',0)

    def set_current_phil(self,value: int):
        self.set_current_phil = value
        
    def neaters(self):
        return self.eaters
        
    def free_sides(self):
        siguiente = (self.set_current_phil + 1)%self.nphil
        anterior = (self.set_current_phil - 1)%self.nphil
        return self.eaters.count(siguiente)==0 and self.eaters.count(anterior)==0
    
    def wants_eat(self,value:int):
        self.mutex.acquire()
        self.free_fork.wait_for(self.free_sides)
        self.eaters.append(value)
        self.mutex.release()
        
    def wants_think(self,value:int):
        self.mutex.acquire()
        self.eaters.remove(value)
        self.free_fork.notify_all()
        self.mutex.release()
from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Manager, Value
import time
import random
import paho.mqtt.client as mqtt


NPHIL = 5
Phil_names = ["Sócrates", "Platón", "Tales", "Heráclito", "Aristóteles"]
K = 100

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "mat.wild.ucm.es"
client = mqtt.Client("Mesa_filosofos")
client.connect(mqttBroker)


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
        
        
def delay(n):
    time.sleep(random.random()/n)
    
def philosopher_task(num:int, table: Table):
    table.set_current_phil(num)
    while True:
        client.publish("Mesa_filosofos", "Philosofer "+str(Phil_names[num])+" thinking")
        print (f"Philosofer {num} thinking")
        delay(6)
        client.publish("Mesa_filosofos", "Philosofer "+str(Phil_names[num])+" wants to eat")
        print (f"Philosofer {num} wants to eat")
        table.wants_eat(num)
        client.publish("Mesa_filosofos", "Philosofer "+str(Phil_names[num])+" eating")
        print (f"Philosofer {num} eating")
        table.wants_think(num)
        delay(6)
        client.publish("Mesa_filosofos", "Philosofer "+str(Phil_names[num])+" stops eating")
        print (f"Philosofer {num} stops eating")
        delay(6)
        
        
def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    philosofers = [Process(target=philosopher_task, args=(i,table)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()


        
if __name__ == '__main__':
    main()



from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Manager, Value
import time
import random
import paho.mqtt.client as mqtt


NPHIL = 5
Phil_names = ["Chomsky", "Butler", "Zizek", "Byung-Chul Han", "Hofstadter"]
K = 100

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = 'wild.mat.ucm.es'
client = mqtt.Client("Mesa_actualidad")
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
        client.publish("Mesa_actualidad", str(Phil_names[num])+" esta pensando")
        print (f"El filosofo {num} esta pensando")
        delay(6)
        client.publish("Mesa_actualidad", str(Phil_names[num])+" quiere comer")
        print (f"El filosofo {num}  quiere comer")
        table.wants_eat(num)
        client.publish("Mesa_actualidad", str(Phil_names[num])+" esta comiendo")
        print (f"El filosofo {num} esta comiendo")
        table.wants_think(num)
        delay(6)
        client.publish("Mesa_actualidad", str(Phil_names[num])+" para de comer")
        print (f"El filosofo {num}  para de comer")
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
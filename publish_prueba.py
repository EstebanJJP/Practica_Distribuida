
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client()
client.connect(mqttBroker)

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("Mesa_filosofos", randNumber)
    print("Just published " + str(randNumber) + " to Topic Mesa_filosofos")
    time.sleep(1)


import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client()
client.connect(mqttBroker)

client.loop_start()
topic = input("Mesas disponibles:\nMesa_antigua\nMesa_edad_moderna\nMesa_contemporanea\nMesa_actualidad\n¿A qué mesa desea suscribirse? ")
client.subscribe(topic)
client.on_message = on_message
time.sleep(30)
client.loop_stop()
print("Gracias por echar un vistazo a la "+str(topic)+". ¡Vuelve cuando quieras!")



import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "wild.mat.ucm.es"
client = mqtt.Client()
client.connect(mqttBroker)

client.loop_start()
topic = input("Mesas disponibles:\nMesa/edad_moderna\nMesa/contemporanea\nMesa/actualidad\n(Ponga Mesa/# para suscribirse a todas a la vez)\n¿A qué mesa desea suscribirse? ")
client.subscribe(topic)
client.on_message = on_message
time.sleep(20)
client.loop_stop()
print("Gracias por echar un vistazo a la "+str(topic)+". ¡Vuelve cuando quieras!")

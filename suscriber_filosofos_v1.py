import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "wild.mat.ucm.es"
client = mqtt.Client()
client.connect(mqttBroker)

client.loop_start()
client.subscribe("Mesa_filosofos")
client.on_message = on_message
time.sleep(30)
client.loop_stop()
print("Gracias por echar un vistazo a la mesa de los filósofos. ¡Vuelve cuando quieras!")

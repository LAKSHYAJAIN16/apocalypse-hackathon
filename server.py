import geopy.distance
import paho.mqtt.client as mqtt
from kmeans import kMeans
import matplotlib.pyplot as plt
import geopy
import time

# Database (with some testing values)
database = {
}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    if msg.topic == "geolocation":
        # filter out the data
        dat = str(msg.payload).split(",")
        lat = float(dat[0].split(":")[1])
        longi = float(dat[1].split(":")[1])
        id = dat[2].split(":")[1]
        database[id] = {
            "id" : id,
            "lat" : lat,
            "long" : longi
        }
        print(lat, longi, id)
        identify_horde(lat, longi, id)

#
def on_publish(client, userdata, mid):
    print(mid)
    print(client)
    print(userdata)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "fucking_hell_you_piece_of_shit")
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.connect('broker.hivemq.com', 1883)
client.subscribe('geolocation')

# Identify Horde algorithm
def identify_horde(lat, longi, id):
    # Convert the dictionary into a list of lists
    coordinates_list = [[value["lat"], value["long"]] for value in database.values()] + [[37.7749, -122.4194],
    [34.0522, -118.2437],
    [40.7128, -74.0060],
    [51.5074, -0.1278],
    [48.8566, 2.3522],
    [35.6895, 139.6917],
    [55.7558, 37.6173],
    [39.9042, 116.4074]]

    centers = kMeans(coordinates_list)
    best_center_dist = 18247923874923874923
    for center in list(centers):
        coords_1 = (center[0], center[1])
        coords_2 = (lat, longi)
        if(geopy.distance.geodesic(coords_1, coords_2).km < best_center_dist):
            best_center_dist = geopy.distance.geodesic(coords_1, coords_2).km
            

    pay = str(id+":"+str(int(best_center_dist))).replace("'","")
    print(pay)
    time.sleep(3)
    msg = client.publish("hordedetection88u8", pay)
    plt.show()
    msg.wait_for_publish()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
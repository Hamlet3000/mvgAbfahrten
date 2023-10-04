#############################################################################
#    Documentation see GitHub: https://github.com/mondbaron/mvg
#
#    TOPIC = mvg\Johanneskirchner_Straße
#    JSONPATH:$..Abfahrt0.info
#    JSONPATH:$..Abfahrt0.messages
#    JSONPATH:$..Abfahrt0.icon
#    JSONPATH:$..Abfahrt1.info
#    JSONPATH:$..Abfahrt2.info
#    JSONPATH:$..Abfahrt3.info
#
#
#
#############################################################################

import json
import datetime
import paho.mqtt.client as mqtt
from mvg import MvgApi

def get_departures(station_name):
    station_id = MvgApi.station(station_name)

    if station_id:
        mvg_api = MvgApi(station_id['id'])
        departures = mvg_api.departures(limit=5, offset=10)

        departure_data = {}

        for idx, item in enumerate(departures):
            time_readable = datetime.datetime.fromtimestamp(item.get('time')).strftime('%H:%M Uhr')
            info = f"{time_readable} {item['type']} {item['line']} von {station_name} -> {item['destination']} - CANCELLED" if item['cancelled'] else f"{time_readable} {item['type']} {item['line']} von {station_name} -> {item['destination']}"
            item['info'] = info
            departure_data[f"Abfahrt{idx}"] = item

        return departure_data
    else:
        return None

def publish_mqtt(data, subtopic):

    subtopic = subtopic.replace(" ","_")

    MQTT_HOST = "localhost"
    MQTT_TOPIC = f"mvg\\{subtopic}"
    MQTT_PORT = 1883
    MQTT_USER = ""
    MQTT_PW = ""

    MQTT_MSG = json.dumps(data)

    mqttc = mqtt.Client()
    mqttc.username_pw_set(MQTT_USER, MQTT_PW)

    try:
        mqttc.connect(MQTT_HOST, MQTT_PORT, 20)
        mqttc.publish(MQTT_TOPIC, MQTT_MSG)
        mqttc.disconnect()
        print(f"Published MQTT message to {MQTT_TOPIC}: {MQTT_MSG}")
    except Exception as e:
        print(f"Error publishing MQTT message: {str(e)}")

def main():
    station_list = ['Taimerhofstraße', 'Johanneskirchner Straße']

    for station_name in station_list:
        departure_data = get_departures(station_name)
        if departure_data:
            publish_mqtt(departure_data, station_name)

if __name__ == "__main__":
    main()

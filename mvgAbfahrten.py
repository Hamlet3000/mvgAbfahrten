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
import time
import datetime
from datetime import datetime
import paho.mqtt.client as mqtt
from mvg import MvgApi

def get_departures(station_name, destination_list):
    station_id = MvgApi.station(station_name)

    if station_id:
        mvg_api = MvgApi(station_id['id'])
        departures = mvg_api.departures(limit=20, offset=10)

        departure_data = {}

        idx = 0
        for item in departures:
            if item['destination'] in destination_list:
                time_readable = datetime.fromtimestamp(item.get('time')).strftime('%H:%M Uhr')
                akt_time = int(time.mktime(datetime.now().timetuple()))
                dif_in_min = int((item['time'] - akt_time) / 60)

                if item['cancelled']:
                    info = f"in {dif_in_min} Min. ({time_readable}) {item['type']} {item['line']} von {station_name} -> {item['destination']} - CANCELLED" 
                else:
                    info = f"in {dif_in_min} Min. ({time_readable}) {item['type']} {item['line']} von {station_name} -> {item['destination']}" 

                item['info'] = info
                departure_data[f"Abfahrt{idx}"] = item

                #print(item['info'])
                idx = idx+1

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
    station_list = ['Hauptbahnhof', 'Lehel']
    destination_list = ['Hauptbahnhof', 'Lehel', 'Max-Weber-Platz', 'Romanplatz']

    for station_name in station_list:
        departure_data = get_departures(station_name, destination_list)
        if departure_data:
            publish_mqtt(departure_data, station_name)

if __name__ == "__main__":
    main()

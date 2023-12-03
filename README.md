# mvgAbfahrten

The script uses the MvgApi to provide the departure times of a stop in the area of the Münchner Verkehrs Gesellschaft and publishes them via MQTT.
To do this, a list of stops (station_list in line 79) and destinations (destination_list in line 80) must be specified.

The result is returned as a separate topic with the name of the stop like:
mvg\Hauptbahnhof
mvg\Lehel

In the topic itself, the individual pieces of information can be displayed e.g. with

JSONPATH:$..Abfahrt0.info					(e.g. "in 16 Min. (11:37 Uhr) U-Bahn 4 von Lehel -> Arabellapark")

JSONPATH:$..Abfahrt0.time					(e.g. 1700999580)

JSONPATH:$..Abfahrt0.planned			(e.g. 1701599520)

JSONPATH:$..Abfahrt0.line					(e.g. 4) 

JSONPATH:$..Abfahrt0.destination	(e.g. "Arabellapark")

JSONPATH:$..Abfahrt0.type					(e.g. "U-Bahn")

JSONPATH:$..Abfahrt0.icon					(e.g. "mdi:ubahn")

JSONPATH:$..Abfahrt0.cancelled		(e.g. "false")

JSONPATH:$..Abfahrt0.messages			(e.g. [])

etc can be queried.



I call the script regularly every minute via cronjob:

\* \* \* \* \* python /usr/bin/mvgAbfahrten.py

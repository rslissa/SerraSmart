import json

PROJECT_PATH = None
ACQUISITION_POINT = None
SERIAL_PORTNAME = None
NOTIFICATION_ERROR_DELAY = None
NOTIFICATION_ADVISE_DELAY = None
TELEGRAM_USERS = []
MQTT_BROKER = None
MQTT_PORT = None
MQTT_TOPIC = None
MQTT_CLIENT_ID = None

# Opening JSON file
f = open('config.json', )

# returns JSON object as
# a dictionary
data = json.load(f)
try:
    PROJECT_PATH = str(data["PROJECT_PATH"])
except:
    print("field PROJECT_PATH missed or corrupt on config.json file")
try:
    ACQUISITION_POINT = str(data["ACQUISITION_POINT"])
except:
    print("field ACQUISITION_POINT missed or corrupt on config.json file")
try:
    SERIAL_PORTNAME = str(data["SERIAL_PORTNAME"])
except:
    print("field SERIAL_PORTNAME missed or corrupt on config.json file")
try:
    NOTIFICATION_ERROR_DELAY = int(data["NOTIFICATION_ERROR_DELAY"])
except:
    print("field NOTIFICATION_ERROR_DELAY missed or corrupt on config.json file")
try:
    NOTIFICATION_ADVISE_DELAY = int(data["NOTIFICATION_ADVISE_DELAY"])
except:
    print("field NOTIFICATION_ADVISE_DELAY missed or corrupt on config.json file")
try:
    TELEGRAM_USERS = data["TELEGRAM_USERS"]
except:
    print("field TELEGRAM_USERS missed or corrupt on config.json file")
try:
    MQTT_BROKER = str(data["MQTT_BROKER"])
except:
    print("field MQTT_BROKER missed or corrupt on config.json file")
try:
    MQTT_PORT = int(data["MQTT_PORT"])
except:
    print("field MQTT_PORT missed or corrupt on config.json file")
try:
    MQTT_TOPIC = str(data["MQTT_TOPIC"])
except:
    print("field MQTT_TOPIC missed or corrupt on config.json file")
try:
    MQTT_CLIENT_ID = str(data["MQTT_CLIENT_ID"])
except:
    print("field MQTT_CLIENT_ID missed or corrupt on config.json file")

# Closing file
f.close()

# Arduino analog pin range 0-1023
ANALOG_MIN = 0
ANALOG_MAX = 1023
# EC range 0-10000us/cm
EC_MIN = 0
EC_MAX = 10000
EC_THRESHOLD_MIN = 1500
EC_THRESHOLD_MAX = 6000
EC_ERROR_MIN = 500
EC_ERROR_MAX = 10000
# Water flow 0.3-6L/min
WF_MIN = 0.3
WF_MAX = 6
WF_THRESHOLD_MIN = 0.3
WF_THRESHOLD_MAX = 6
WF_ERROR_MIN = 0.3
WF_ERROR_MAX = 6
# Ground temperature range -55-125°C
GT_MIN = -55
GT_MAX = 125
GT_THRESHOLD_MIN = 7
GT_THRESHOLD_MAX = 35
GT_ERROR_MIN = -5
GT_ERROR_MAX = 50
# Ground humidity range 0-100%
GH_MIN = 0
GH_MAX = 100
GH_THRESHOLD_MIN = 70
GH_THRESHOLD_MAX = 100
GH_ERROR_MIN = 20
GH_ERROR_MAX = 100
# Air temperature range -40-80°C
AT_MIN = -40
AT_MAX = 80
AT_THRESHOLD_MIN = 3
AT_THRESHOLD_MAX = 40
AT_ERROR_MIN = 0
AT_ERROR_MAX = 60
# Air humidity range 0-100%
AH_MIN = 0
AH_MAX = 100
AH_THRESHOLD_MIN = 30
AH_THRESHOLD_MAX = 95
AH_ERROR_MIN = 0
AH_ERROR_MAX = 100

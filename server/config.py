#MQTT
BROKER = "broker.emqx.io"
#BROKER = 'broker.mqttdashboard.com'
PORT = 1883
TOPIC = "IOTProject"
client_id = "Pasquale-receiver"

#DB
acquisition_point_array = ['A01']
#parameter_array = ['water_flow']    #Ricordarsi di cambiare
parameter_array = ['ec', 'water_flow', 'ground_temperature', 'ground_humidity', 'air_temperature', 'air_humidity']

#THINGSBOARD
localhost = "http://localhost:9090"
TOKEN_SERRA = "i1ZtDfX4pnscmkLXcdEy"

#PREVISIONI
DATA_CSV = 'data.csv'
PERIODS = 7

#API
LOCALHOST_API = "http://127.0.0.1:10000"

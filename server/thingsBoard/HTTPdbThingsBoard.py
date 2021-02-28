'''from requests import post, get
import random
from datetime import datetime
import time
import communication.validation as val
from communication.dbAccess import DBconnection

db_util = DBconnection()

HOST_NAME = "http://localhost:9090"
TOKEN = "i1ZtDfX4pnscmkLXcdEy"
'''

#Caricamento su dashboard
'''while True:
    item = {
        "id": 0,
        "datetime": str(datetime.now()),
        "acquisition_point": "A01",
        "EC": random.uniform(0.0, 10000.0),
        "WF": random.uniform(0.3, 6),
        "GT": random.uniform(-55.0, 125.0),
        "GH": random.uniform(0.0, 100.0),
        "AT": random.uniform(-40.0, 80.0),
        "AH": random.uniform(0, 100)
    }
    print(item)
    #POST
    r = post(f"{HOST_NAME}/api/v1/{TOKEN}/telemetry", json=item)
    print(r.text, r.status_code)
    time.sleep(5)'''

'''
#Caricamento su db
id = 115  #ATTENZIONE A SELEZIONARE L'ULTIMO ID CARICATO SUL DB + 1
while True:
    json = {
        "message": {
            "id": id,
            "datetime": str(datetime.now()),
            "acquisition_point": "A01",
            "EC": round(random.uniform(0.0, 10.0), 2),
            "WF": round(random.uniform(0, 6), 2),
            "GT": round(random.uniform(60.0, 75.0), 2),
            "GH": round(random.uniform(0.0, 10.0), 2),
            "AT": round(random.uniform(60.0, 80.0), 2),
            "AH": round(random.uniform(0, 10), 2)
        }
    }
    r = val.validBody(json)
    if r is not None:
        db_util.insert_acquisition(json['message'])
        id = id + 1
    time.sleep(5)'''
'''    if id == 500:
        break'''




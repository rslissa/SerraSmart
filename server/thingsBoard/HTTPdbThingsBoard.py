from requests import post, get
import random
from datetime import datetime
import time

HOST_NAME = "http://localhost:9090"
TOKEN = "i1ZtDfX4pnscmkLXcdEy"


'''E' necessario distinguere la sorgente anche come acquisition_point'''

while True:
    item = {
        "id": 217,
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
    # POST
    #r = post(f"{HOST_NAME}/api/v1/{TOKEN}/telemetry", json=item)
    #print(r.text, r.status_code)
    #time.sleep(5)


import threading
import communication.mqttClient as to_client
from FbProphet.prevision import Previson

util_prevision = Previson()

if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=to_client.run())
        t2 = threading.Thread(target=util_prevision.prevision_flow())
        t1.start()
        t1.join()
        t2.start()
        t2.join()
    except:
        print('Error on starting!')


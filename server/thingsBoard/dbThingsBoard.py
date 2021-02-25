from requests import post
from communication import validation


class Dashboard:
    def __init__(self):
        self.HOST_NAME = "http://localhost:9090"
        self.TOKEN = "i1ZtDfX4pnscmkLXcdEy"

    def post_acquisition(self, acquisition):
        #Riceve un dict letto dal db (solo il message) e lo manda a thingsboard con una richiesta post
        if acquisition is None:
            print('Db acquisition empty!')
            return

        ret = validation.validBody(acquisition)
        if ret is None:
            print('Db acquisition not valid!')
            return

        r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=ret['message'])
        if r is None:
            print('POST error!')
            return

        print('Acquisition uploaded to Dashboard!')
        return

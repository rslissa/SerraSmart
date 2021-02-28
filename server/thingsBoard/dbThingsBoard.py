from requests import post
from communication import validation
import config

class Dashboard:
    def __init__(self):
        self.HOST_NAME = config.localhost
        self.TOKEN = config.TOKEN_SERRA
        self.ec = None
        self.wf = None
        self.gt = None
        self.gh = None
        self.at = None
        self.ah = None

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

    #Funzione per postare le previsioni di un intero ciclo
    def post_previsions(self, forecast_list):
        #forecast_list è una lista che contiene un intero ciclo di previsioni per un punto di acquisizione

        if forecast_list is None:
            print('No forecasts list found!')
            return

        acquisition_point = None
        parameter = None
        forecast = None

        #Siccome voglio caricare le previsioni per data, allora prendo prima l'array di date
        dates = []
        for i in range(config.PERIODS):
            dates.append(str(forecast_list[0]['dates']['ds'].values[i]))

        i = 0
        for date in dates:
            for item in forecast_list:
                if i > 7:
                    break
                acquisition_point = item['acquisition_point']
                parameter = item['parameter']
                forecast = item['forecast'] #contiene le previsioni per i 7 giorni successivi
                prevision = round(forecast['yhat'].head(i + 1).values[i], 2)

                if parameter == 'ec':
                    self.ec = prevision
                elif parameter == 'water_flow':
                    self.wf = prevision
                elif parameter == 'ground_temperature':
                    self.gt = prevision
                elif parameter == 'ground_humidity':
                    self.gh = prevision
                elif parameter == 'air_temperature':
                    self.at = prevision
                elif parameter == 'air_humidity':
                    self.ah = prevision
            #print('parametri alla data ', date, self.ec, self.wf, self.gt, self.gh, self.at, self.ah)
            i += 1

            #Costruisco l'item e lo carico sulla dashboard
            item = {
                'Datetime': str(date),
                'Acquisition_Point': acquisition_point,
                'ec': self.ec,
                'water_flow': self.wf,
                'ground_temperature': self.gt,
                'ground_humidity': self.gh,
                'air_temperature': self.at,
                'air_humidity': self.ah
            }

            r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=item)
            if r is None:
                print('Error in posting previsions!', r.status_code)

        print('Previsions uploaded to Dashboard!')
        return

    #Funzioni per postare una previsione alla volta
    def post_prevision(self, forecast, parameter, acquisition_point):
        # Prendo le utlime previsioni
        num_tot = len(forecast)
        num_f = 7   #uguale al numero di epoche che vogliamo prevedere
        for i in range(num_f):
            item = {
                'Datetime': str(forecast['ds'][num_tot - 7 + i]),
                parameter: round(forecast['yhat'][num_tot - 7 + i], 2),
                'Acquisition_Point': acquisition_point
            }
            #print(item, '\n')
            r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=item)
            if r is None:
                print('Error in posting prevision!')
                return

        print('Prevision uploaded to Dashboard!')
        return

    def post_roof(self, roof):
        if roof is not None:
            item = {
                'roof': roof
            }
            r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=item)
            if r is None:
                print('Error on actuate roof!')
                return

        return 'Roof uploaded to Dashboard!'

    def post_irrigation(self, irrigation):
        if irrigation is not None:
            item = {
                'irrigation': irrigation
            }
            r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=item)
            if r is None:
                print('Error on actuate irrigation!')
                return

        return 'Irrigation uploaded to Dashboard!'

    def post_roof_and_irrigation(self, roof, irrigation):
        if roof is not None and irrigation is not None:
            item = {
                'roof': roof,
                'irrigation': irrigation
            }
            r = None
            try:
                r = post(f"{self.HOST_NAME}/api/v1/{self.TOKEN}/telemetry", json=item)
            except:
                return r.status_code

        return

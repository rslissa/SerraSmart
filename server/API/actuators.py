from API.pushAPI import PushAPI
from thingsBoard.dbThingsBoard import Dashboard
import config

util_api = PushAPI()
util_dashboard = Dashboard()


class Actuator:
    def __init__(self):
        self.ec = None
        self.wf = None
        self.gt = 1
        self.gh = None
        self.at = 1
        self.ah = None

    def set_last_prevision(self, forecast_list):
        #forecast_list è una lista che contiene un intero ciclo di previsioni per un punto di acquisizione

        if forecast_list is None:
            print('No forecasts list found!')
            return

        acquisition_point = None
        parameter = None
        forecast = None

        for item in forecast_list:
            acquisition_point = item['acquisition_point']
            parameter = item['parameter']
            forecast = item['forecast']  # contiene le previsioni per i 7 giorni successivi
            prevision = round(forecast['yhat'].head(1).values[0], 2)    #valore dell'ultima previsione per lo specifico parametro

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

        #print(self.ec, self.wf, self.gt, self.gh, self.at, self.ah)

        self.actuate(acquisition_point)

        return

    def actuate(self, acquisition_point):
        all_open = 99
        medium_half_open = 80
        half_open = 50
        all_close = 0

        #Prendiamo i valori attuali dalla serra
        roof, irrigation = util_api.get_roof_and_irrigation(acquisition_point)

        #In fase di test senza api
        #roof = 0
        #irrigation = 0

        #Questa sezione può essere sviluppata in ogni momento con la possibilità di inserire altri controlli

        #In base alla temperatura di suolo e ambiente apro/chiudo il tetto
        if self.gt is not None and self.gt <= 10 and self.at is not None and self.at <= 15:
            if roof != all_open:
                roof = all_open
                try:
                    util_api.post_roof_and_irrigation(acquisition_point, roof, irrigation)
                    util_dashboard.post_roof_and_irrigation(roof, irrigation)
                except:
                    print('Not uploaded!')
        elif self.gt is not None and 10 <= self.gt <= 20 and self.at is not None and 15 <= self.at <= 20:
            if roof <= medium_half_open:
                roof = medium_half_open
                util_api.post_roof_and_irrigation(acquisition_point, roof, irrigation)
                util_dashboard.post_roof_and_irrigation(roof, irrigation)

        #In base all'umidità di suolo e ambiente apro/chiudo l'irrigazione
        if self.gh is not None and self.gh <= 70 and self.ah is not None and self.ah <= 30:
            if irrigation != all_open:
                irrigation = all_open
                util_api.post_roof_and_irrigation(acquisition_point, roof, irrigation)
                util_dashboard.post_roof_and_irrigation(roof, irrigation)
        elif self.gh is not None and 70 < self.gh <= 85 and self.ah is not None and 30 < self.ah <= 60:
            if irrigation <= half_open:
                irrigation = half_open
                util_api.post_roof_and_irrigation(acquisition_point, roof, irrigation)
                util_dashboard.post_roof_and_irrigation(roof, irrigation)

        return


if __name__ == '__main__':
    Actuator().actuate('A01')




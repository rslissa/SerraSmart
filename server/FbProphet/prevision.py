from datetime import datetime
from FbProphet.forecast import Forecast
from thingsBoard.dbThingsBoard import Dashboard
import config
import time
from API.actuators import Actuator

util_forecast = Forecast()
util_dashboard = Dashboard()
util_actuator = Actuator()


class Previson:
    def __init__(self):
        self.last_hour = datetime.now().hour + 1
        self.acquisition_point_array = config.acquisition_point_array
        self.parameter_array = config.parameter_array

    def prevision_flow(self):
        forecast_list = []
        try:
            while True:
                # Questo codice lo devo eseguire in loop
                # Faccio le previsioni ogni ora
                if self.last_hour != datetime.now().hour:
                    # Per ogni punto di acquisizione e per ogni parametro faccio le previsioni e carico sulla dashboard
                    for point in self.acquisition_point_array:
                        for parameter in self.parameter_array:
                            start = time.time() #START del ciclo delle previsioni

                            #Faccio la previsione
                            forecast = util_forecast.predict(point, parameter)
                            if forecast is not None:
                                # Metto quelle dei 7 giorni successivi in un dict
                                forecast_step = {
                                    'acquisition_point': point,
                                    'parameter': parameter,
                                    'dates': forecast[['ds']].tail(7),
                                    'forecast': forecast[['yhat']].tail(7)
                                }

                                # Accumulo i dict in una lista
                                forecast_list.append(forecast_step)

                            #Per caricare una previsione alla volta
                            #util_dashboard.post_prevision(forecast, parameter, point)

                            stop = time.time()  #STOP del ciclo delle previsioni
                            print(f'CORRECTLY PROVISIONED! {point}, {parameter} in {stop - start}')

                        #Carico la lista delle previsioni
                        util_dashboard.post_previsions(forecast_list)

                        # Qua devo mandare le previsioni alla funzione che fa le attuazioni, le devo mandare per ogni acquisition point
                        util_actuator.set_last_prevision(forecast_list)
                self.last_hour = datetime.now().hour
                #Per evitare il polling continuo sul while, si potrebbe stimare il tempo di calcolo delle previsioni ed aspettare
                #un determinato periodo (es: 10 min) prima di riverificare la condizione
                #else:
                #    time.sleep(600)
        except:
            print('Provision flow unexpected exit!')

'''
if __name__ == '__main__':
    p = Previson()
    p.prevision_flow()'''

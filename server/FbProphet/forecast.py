#Installazione FBprophet: https://github.com/facebook/prophet

import pandas as pd
from fbprophet import Prophet
from communication.dbAccess import DBconnection
import config

db_util = DBconnection()


class Forecast:
    def __init__(self):
        self.file_name = config.DATA_CSV
        self.m = None

    def build_model(self, parameter):
        m = None
        try:
            df = pd.read_csv(self.file_name)
            df = df.rename(columns={'datetime': 'ds',
                                    parameter: 'y'})
            #print(df.head(5))

            m = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True, changepoint_prior_scale=0.5, interval_width=0.90)
            #weekly_seasonality=True
            #yearly_seasonality=True
            #interval_width=0.95
            #changepoint_prior_scale=0.8
            #interval_width=0.90
            m.fit(df)

        except:
            print('Problem in loading file data on prophet!')

        return m

    def predict(self, acquisition_point, parameter):
        #Faccio l'export degli ultimi dati su data.csv
        db_util.export_csv(acquisition_point, parameter)

        #Costruisco il modello
        self.m = self.build_model(parameter)

        # Creo il dataframe per contenere le predizioni
        future = self.m.make_future_dataframe(periods=config.PERIODS)  # periods è in giorni il tempo che vogliamo predire es: 7 -> prediciamo i valori per i 7 giorni consecutivi

        # Calcolo le predizioni
        forecast = self.m.predict(future)
        # print('Forecasting\n', forecast)
        print(forecast[['ds', 'yhat']].tail(7))
        #print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(1))

        return forecast






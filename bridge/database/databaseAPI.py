#!/usr/bin/python
from datetime import datetime
import psycopg2
from database.configuration import config
from model.acquisition import Acquisition


class DatabaseAPI:
    def __init__(self):
        self.conn = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            cur = self.conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def closeconnection(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def insertacquisition(self, acquisition):
        acquisitionid = None
        try:
            sql = """INSERT INTO public.acquisition(
                                    datetime, 
                                    acquisition_point,
                                    ec, 
                                    water_flow, 
                                    ground_temperature, 
                                    ground_humidity, 
                                    air_temperature, 
                                    air_humidity)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s) 
                        RETURNING id;"""

            # create a cursor
            cur = self.conn.cursor()

            cur.execute(sql, (acquisition.datetime,
                              acquisition.acquisition_point,
                              acquisition.EC,
                              acquisition.WF,
                              acquisition.GT,
                              acquisition.GH,
                              acquisition.AT,
                              acquisition.AH))
            # get the generated id back
            acquisitionid = cur.fetchone()[0]

            # commit the changes to the database
            self.conn.commit()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return acquisitionid

    def get_acquisitions(self, dt):
        try:
            cur = self.conn.cursor()
            sql = "SELECT acquisition.id, datetime, ec, water_flow, ground_temperature, ground_humidity, " \
                  "air_temperature, air_humidity, acquisition_point FROM public.acquisition "

            if dt is None or not isinstance(dt, datetime):
                whereclause = "WHERE 1=1;"
            else:
                if isinstance(dt, datetime):
                    whereclause = "WHERE acquisition.datetime >= '%s';" % dt

            cur.execute(sql + whereclause)
            print("The number of rows: ", cur.rowcount)
            row = cur.fetchone()

            acquisitions = []
            while row is not None:
                #print(row)
                acquisition = Acquisition(row[0], row[1], row[8], row[2], row[3], row[4], row[5], row[6], row[7])
                acquisitions.append(acquisition)
                row = cur.fetchone()
            cur.close()
            print(acquisitions)
            return acquisitions
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == '__main__':
    db = DatabaseAPI()
    db.connect()
    db.get_acquisitions(datetime.now())
    db.closeconnection()

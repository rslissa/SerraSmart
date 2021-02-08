#!/usr/bin/python
import psycopg2
from datetime import datetime
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
                                    ec, 
                                    water_flow, 
                                    ground_temperature, 
                                    ground_humidity, 
                                    air_temperature, 
                                    air_humidity)
                        VALUES(%s,%s,%s,%s,%s,%s,%s) 
                        RETURNING id;"""

            # create a cursor
            cur = self.conn.cursor()

            cur.execute(sql, (datetime.now(),
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


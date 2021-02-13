#!/usr/bin/python
import os
from datetime import datetime
import psycopg2
from database.configuration import config
from model.acquisition import Acquisition
from tools.staticvar import PROJECT_PATH


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

    def get_number_acquisition_points(self, ap):
        try:
            cur = self.conn.cursor()
            sql = "SElECT COUNT (*) FROM acquisition_point "
            if ap is None or not isinstance(ap, str):
                whereclause = "WHERE 1=1;"
            else:
                whereclause = "WHERE code like '%s';" %ap

            cur.execute(sql + whereclause)
            print("The number of rows: ", cur.rowcount)
            row = cur.fetchone()
            ap_number = None
            while row is not None:
                ap_number = row[0]
                row = cur.fetchone()
            cur.close()
            # print(acquisitions)
            return ap_number

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_last_acquisition(self, ap):
        try:
            cur = self.conn.cursor()
            sql = "SELECT * FROM acquisition WHERE datetime = (SELECT MAX(datetime) FROM acquisition) and " \
                  "acquisition_point like '%s' " %ap
            cur.execute(sql)
            row = cur.fetchone()
            acquisition = None
            while row is not None:
                # print(row)
                acquisition = Acquisition(row[0], row[1], row[8], row[2], row[3], row[4], row[5], row[6], row[7])
                row = cur.fetchone()
            cur.close()
            # print(acquisitions)
            return acquisition
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

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
                # print(row)
                acquisition = Acquisition(row[0], row[1], row[8], row[2], row[3], row[4], row[5], row[6], row[7])
                acquisitions.append(acquisition)
                row = cur.fetchone()
            cur.close()
            # print(acquisitions)
            return acquisitions
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def export_acquisition(self):
        try:
            sql = "SELECT * FROM public.acquisition"
            cur = self.conn.cursor()
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql)
            path = PROJECT_PATH + "database\\export\\acquisizioni.csv"
            with open(path, 'w') as f:
                cur.copy_expert(outputquery, f)
            cur.close()
            return path
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def export_acquisition_point(self):
        try:
            sql = "SELECT * FROM public.acquisition_point"
            cur = self.conn.cursor()
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql)
            path = PROJECT_PATH + "database\\export\\punti_raccolta.csv"
            with open(path, 'w') as f:
                cur.copy_expert(outputquery, f)
            cur.close()
            return path
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def list_acquisition_points(self):
        try:
            cur = self.conn.cursor()
            sql = "SELECT acquisition_point.code FROM public.acquisition_point"
            cur.execute(sql)
            row = cur.fetchone()
            acquisition_points = []
            while row is not None:
                acquisition_points.append(row[0])
                row = cur.fetchone()
            cur.close()
            # print(acquisitions)
            return acquisition_points
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == '__main__':
    db = DatabaseAPI()
    db.connect()
    db.export_acquisition_point()
    db.delete_acquisition_point_csv()
    db.closeconnection()

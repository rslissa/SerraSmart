#!/usr/bin/python
import os
from datetime import datetime
import psycopg2
from configuration import config


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

    def insert_or_update_actuator(self, code, values):
        try:
            sql = "INSERT INTO actuator (code, roof, irrigation) "\
                    "VALUES (%s, %s, %s) "\
                    "ON CONFLICT (code) DO UPDATE "\
                    "SET roof = %s, irrigation = %s" \
                    "RETURNING code; "

            # create a cursor
            cur = self.conn.cursor()

            cur.execute(sql, (code,
                              values["roof"],
                              values["irrigation"],
                              values["roof"],
                              values["irrigation"]))

            # get the generated id back
            code = cur.fetchone()[0]

            # commit the changes to the database
            self.conn.commit()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return code

    def insert_or_update_actuator(self, code, values):
        try:
            sql = "INSERT INTO actuator (code, roof, irrigation) "\
                    "VALUES (%s, %s, %s) "\
                    "ON CONFLICT (code) DO UPDATE "\
                    "SET roof = %s, irrigation = %s" \
                    "RETURNING code; "

            # create a cursor
            cur = self.conn.cursor()

            cur.execute(sql, (code,
                              values["roof"],
                              values["irrigation"],
                              values["roof"],
                              values["irrigation"]))

            # get the generated id back
            code = cur.fetchone()[0]

            # commit the changes to the database
            self.conn.commit()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return code

    def get_actuator(self, code):
        try:
            cur = self.conn.cursor()
            sql = "SElECT * FROM actuator "
            if code is None or not isinstance(code, str):
                whereclause = "WHERE 1=1;"
            else:
                whereclause = "WHERE code like '%s';" %code

            cur.execute(sql + whereclause)
            print("The number of rows: ", cur.rowcount)
            row = cur.fetchone()
            # ES: {A01:{roof:25,irrigation:45}}
            actuator = {row[0]: {"roof": row[1], "irrigation": row[2]}}

            cur.close()
            # print(acquisitions)
            return actuator

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == '__main__':
    db = DatabaseAPI()
    db.connect()
    db.insert_or_update_actuator('A03', {"roof": 50, "irrigation": 30})
    print(db.get_actuator("A02"))
    db.closeconnection()

import psycopg2
import psycopg2.extras
from configparser import ConfigParser
from communication.Utils import Formatter

util = Formatter()

class DBconnection:
    def __init__(self):
        self.conn = None
        self.cur = None

    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section) :
            params = parser.items(section)
            for param in params :
                db[param[0]] = param[1]
        else :
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def get_connection(self):
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            '''# create a cursor
            self.cur = self.conn.cursor()

            self.cur.close()'''
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def insert_acquisition(self, acquisition):
        acquisitionid = None
        try:
            self.get_connection()
            sql = "INSERT INTO public.acquisition (id, datetime, ec, water_flow, ground_temperature, ground_humidity," \
                  "air_temperature, air_humidity, acquisition_point) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"

            cur = self.conn.cursor()

            cur.execute(sql, (acquisition['id'],
                              acquisition['datetime'],
                              acquisition['EC'],
                              acquisition['WF'],
                              acquisition['GT'],
                              acquisition['GH'],
                              acquisition['AT'],
                              acquisition['AH'],
                              acquisition['acquisition_point']))

            acquisitionid = cur.fetchone()[0]

            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.close_connection()

        return acquisitionid

    def retrieve_acquisition(self):
        acquired = None
        casted = None
        try:
            sql = "SELECT * FROM public.acquisition ORDER BY id DESC limit 1;"
            self.get_connection()

            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute(sql)

            acquired = cur.fetchone()
            #print('Acquired:\n', acquired)

            casted = util.message_formatting(acquired)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.close_connection()

        return casted

    def export_csv(self, acquisition_point, parameter):
        path1 = "C:\\Users\\Pc_User\\Desktop\\ProgettoSerraSmart\\SerraSmart\\server\\FbProphet\\data.csv"
        path2 = "C:\\Users\\Pc_User\\Desktop\\ProgettoSerraSmart\\SerraSmart\\server\\data.csv"
        try:
            #risolvere il problema dell'uguaglianza per l'acquisition point
            sql = f"SELECT datetime,{parameter} FROM public.acquisition WHERE {parameter} IS NOT NULL AND acquisition_point='{acquisition_point}'"

            self.get_connection()
            cur = self.conn.cursor()

            SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql)

            with open(path1, 'w') as f_output:
                cur.copy_expert(SQL_for_file_output, f_output)

            with open(path2, 'w') as f_output:
                cur.copy_expert(SQL_for_file_output, f_output)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.close_connection()

        return


'''if __name__ == '__main__':
    c = DBconnection()
    c.get_connection()
    c.close_connection()'''







# python mysql db

import pymysql

class DB:

    __conn :pymysql
    __cursor :pymysql.cursors.DictCursor

    def get_conn(self):
        self.__conn = pymysql.connect(
            host='janieto2.com',
            user='jose',
            password='Cabral.35!',
            db='msv',
            charset='utf8'
        )

    def get_cursor(self):
        self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
        

    def get_all_data(self):
        self.__cursor.execute("SELECT * FROM submission")
        return self.__cursor.fetchall()

    def fetch_one(self, id):
        self.__cursor.execute("SELECT * FROM submission WHERE id = %s", (id))
        return self.__cursor.fetchone()
    
    def get_all_by_provider(self, provider):
        self.__cursor.execute("SELECT * FROM submission WHERE provider = %s", (provider))
        return self.__cursor.fetchall()
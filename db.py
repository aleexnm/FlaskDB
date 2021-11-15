# python mysql db

import pymysql


class DB:
    __conn: pymysql
    __cursor: pymysql.cursors.DictCursor

    def get_conn(self):
        self.__conn = pymysql.connect(
            host='10.101.20.33',
            user='EPPCSTAFF',
            password='@3215Gateway',
            db='eppcADB',
            charset='utf8'
        )

    def get_cursor(self):
        self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)

    def get_all_data(self):
        self.__cursor.execute("SELECT * FROM InventoryOutOfStockDates")
        return self.__cursor.fetchall()

    def fetch_one(self, id):
        self.__cursor.execute("SELECT * FROM InventoryOutOfStockDates WHERE id = %s", id)
        return self.__cursor.fetchone()

    def get_all_by_facilities(self, facility):
        self.__cursor.execute("SELECT * FROM InventoryOutOfStockDates WHERE Facility = %s", facility)
        return self.__cursor.fetchall()

    def get_all_products(self, facility):
        self.__cursor.execute("SELECT * FROM CustomScheduleAll WHERE VisitCode = '415' AND Facility= %s LIMIT 50", facility)
        return self.__cursor.fetchall()

    def get_all_note(self, facility):
        self.__cursor.execute("SELECT * FROM CustomScheduleAll INNER JOIN kvVisitStatusCode ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode WHERE kvVisitStatusCode.ManagerPendingInclude Is True AND Facility= %s", facility)
        return self.__cursor.fetchall()

    def get_all_clinics(self, facility):
        self.__cursor.execute("SELECT * FROM InventoryOutOfStockDates WHERE Facility = %s LIMIT 1", facility)
        return self.__cursor.fetchall()

    def get_facility_list(self):
        self.__cursor.execute("SELECT ShortName, FacilityName FROM kvFacility WHERE status = 'Active' ORDER BY FacilityName")
        return self.__cursor.fetchall()
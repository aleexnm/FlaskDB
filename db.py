# python mysql db
import sys
import pymysql

class Database:
    """Database Connection Class"""

    def __init__(self, config):
        self.host = config.db_host
        self.username = config.db_user
        self.password = config.db_password
        self.dbname = config.db_name
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    db=self.dbname,
                    connect_timeout=5
                )
        except pymysql.MySQLError as e:
            sys.exit()
        finally:
            return None

    def run_query(self, query):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor(pymysql.cursors.DictCursor) as cur:
                if 'SELECT' in query:
                    cur.execute(query)
                    result = cur.fetchall()
                    cur.close()
                    return result
                result = cur.execute(query)
                self.conn.commit()
                affected = f"{cur.rowcount} rows affected."
                cur.close()
                return affected
        except pymysql.MySQLError as e:
            logger.error(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

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
        self.__cursor.execute("SELECT DATE_FORMAT(ApptDate, '%%m/%%d/%%Y') as ApptDate, MRN, PtName, VisitType, VisitCode "
                              "FROM CustomScheduleAll WHERE VisitCode = '415' AND Facility= %s LIMIT 50", facility)
        return self.__cursor.fetchall()

    def get_all_note(self, facility):
        self.__cursor.execute(("SELECT DATE_FORMAT(CustomScheduleAll.ApptDate, '%%m/%%d/%%Y') as ApptDate, CustomScheduleAll.MRN, CustomScheduleAll.PtName, "
                               "CustomScheduleAll.VisitType, CustomScheduleAll.VisitCode, "
                               "kvVisitStatusCode.VisitStatusDesc FROM CustomScheduleAll INNER JOIN kvVisitStatusCode "
                               "ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode "
                               "WHERE CustomScheduleAll.MRN NOT LIKE ('TestP%%') AND "
                               "kvVisitStatusCode.ManagerPendingInclude Is True AND Facility= %s"), facility)
        return self.__cursor.fetchall()

    def get_all_clinics(self, facility):
        self.__cursor.execute("SELECT * FROM InventoryOutOfStockDates WHERE Facility = %s LIMIT 1", facility)
        return self.__cursor.fetchall()

    def get_facility_list(self):
        self.__cursor.execute("SELECT ShortName, FacilityName FROM kvFacility WHERE status = 'Active' ORDER BY FacilityName")
        return self.__cursor.fetchall()

    def get_visit_types(self):
        self.__cursor.execute("SELECT id, VisitTypeCode FROM kvVisitTypeCode WHERE Status='Active' ORDER BY VisitTypeCode")
        return self.__cursor.fetchall()

    def get_facilities(self):
        self.__cursor.execute("SELECT FacilityName FROM kvFacility WHERE status = 'Active' ORDER BY FacilityName")
        return self.__cursor.fetchall()

    def get_providers(self):
        self.__cursor.execute("SELECT provFullName FROM kvProviderInfo WHERE provStatus = 'Active' ORDER BY provFullName")
        return self.__cursor.fetchall()

    def get_cs_data(self, start_date, end_date, visit_type, visit_type_selection, visit_category, provider_all, provider, facility_all, facility, visit_status_category):

        #Set up the provider and facility filter strings to add to the queries
        if provider_all.data:
            provider_filter = ""
        else:
            provider_filter = " AND ApptProvider = '" + provider.data + "'"

        if facility_all.data:
            facility_filter = ""
        else:
            facility_filter = " AND Facility = '" + facility.data + "'"


        if visit_type_selection == "Select Single Visit Type": # Single visit type, include in query

            if visit_status_category == "All": # Do not need to join visit status table
                sql_string = ("SELECT * FROM CustomScheduleAll WHERE ApptDate >= '{}' AND ApptDate <= '{}' AND VisitType = '{}' {} {} ORDER BY ApptDate, ApptTime")\
                            .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), visit_type, provider_filter, facility_filter)
            else: #Need to join visit status table and add filter
                if visit_status_category == "Seen/Scheduled":
                    include_status = "Yes"
                else:
                    include_status = "No"

                sql_string = ("SELECT * FROM CustomScheduleAll INNER JOIN kvVisitStatusCode "
                              "ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode "
                              "WHERE CustomScheduleAll.ApptDate >= '{}' AND CustomScheduleAll.ApptDate <= '{}' AND kvVisitStatusCode.VisitCountInclude = '{}' AND VisitType = '{}' {} {} ORDER BY ApptDate, ApptTime") \
                            .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), include_status, visit_type, provider_filter, facility_filter)

            self.__cursor.execute(sql_string)
            return self.__cursor.fetchall()

        else:  #Category Selected

            if visit_category == "All": #No need to join visit type table since it is all

                if visit_status_category == "All": #No need to join visit status table
                    sql_string = ("SELECT * FROM CustomScheduleAll WHERE ApptDate >= '{}' AND ApptDate <= '{}' {} {} ORDER BY ApptDate, ApptTime")\
                                .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), provider_filter, facility_filter)
                else: #Need to join visit status table
                    if visit_status_category == "Seen/Scheduled":
                        include_status = "Yes"
                    else:
                        include_status = "No"

                    sql_string = ("SELECT * FROM CustomScheduleAll INNER JOIN kvVisitStatusCode "
                                  "ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode "
                                  "WHERE ApptDate >= '{}' AND ApptDate <= '{}' AND kvVisitStatusCode.VisitCountInclude = '{}' {} {} ORDER BY ApptDate, ApptTime")\
                                .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), include_status, provider_filter, facility_filter)


            else:  # Need to join kvVisitTypeCode to get the encWoClaimsTgtGroup
                if visit_category == "Procedure": #Get both Inj and Level3 groups
                    category_filter = "AND (kvVisitTypeCode.EncWoClaimsTgtGroup = 'Inj' OR kvVisitTypeCode.EncWoClaimsTgtGroup = 'Inj')"
                else:
                    category_filter = "AND kvVisitTypeCode.EncWoClaimsTgtGroup = '{}'".format(visit_category)

                if visit_status_category == "All": #No need to join visit status table
                    sql_string = ("SELECT * FROM CustomScheduleAll INNER JOIN kvVisitTypeCode "
                                  "ON kvVisitTypeCode.VisitTypeCode = CustomScheduleAll.VisitType "
                                  "WHERE CustomScheduleAll.ApptDate >= '{}' AND CustomScheduleAll.ApptDate <= '{}' {} {} {} ORDER BY ApptDate, ApptTime")\
                                .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), category_filter, provider_filter, facility_filter)
                else: # Need to join visit status table
                    if visit_status_category == "Seen/Scheduled":
                        include_status = "Yes"
                    else:
                        include_status = "No"

                    sql_string = ("SELECT * FROM CustomScheduleAll LEFT JOIN kvVisitTypeCode "
                                  "ON kvVisitTypeCode.VisitTypeCode = CustomScheduleAll.VisitType "
                                  "LEFT JOIN kvVisitStatusCode ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode "
                                  "WHERE CustomScheduleAll.ApptDate >= '{}' AND CustomScheduleAll.ApptDate <= '{}' AND kvVisitStatusCode.VisitCountInclude = '{}' {} {} {}} ORDER BY ApptDate, ApptTime") \
                                .format(start_date.data.strftime("%Y-%m-%d"), end_date.data.strftime("%Y-%m-%d"), include_status, category_filter, provider_filter, facility_filter)

            self.__cursor.execute(sql_string)
            return self.__cursor.fetchall()
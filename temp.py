def get_all_products(self, facility):
    self.__cursor.execute("SELECT * FROM CustomScheduleAll \
                               INNER JOIN kvVisitStatusCode ON kvVisitStatusCode.VisitStatus = CustomScheduleAll.VisitCode \
                               WHERE kvVisitStatusCode.ManagerPendingInclude Is True AND Facility= %s", facility)
    return self.__cursor.fetchall()
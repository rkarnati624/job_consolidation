import mysql.connector


def db_conn():
    cnx = mysql.connector.connect(user='jobsapp', password='jobsapp',
                                  host='ortest02.ydesigngroup.net ',
                                  database='jobsdb')
    jobsdb_cursor = cnx.cursor()


class Jobsappdb:

    def insert_scc_query(self):
        cnx = mysql.connector.connect(user='jobsapp', password='jobsapp',
                                      host='ortest02.ydesigngroup.net ',
                                      database='jobsdb')
        jobsdb_cursor = cnx.cursor()
        sql_scc = """INSERT INTO jobsdb.job_monitoring_log (`source_type`,`Job_name`,`status`,`status_code`,
        `job_starttime`,`job_endtime`) VALUES(%s,%s,%s,%s,%s,%s) """
        jobsdb_cursor.execute(sql_scc)
        cnx.commit()

    def insert_rundeck_query(self):
        sql_rundeck = """INSERT INTO jobsdb.job_monitoring_log (`source_type`,`Job_name`,`status`,`status_code`,
        `job_starttime`,`job_endtime`) VALUES(%s,%s,%s,%s,%s,%s) """
        cnx = mysql.connector.connect(user='jobsapp', password='jobsapp',
                                      host='ortest02.ydesigngroup.net ',
                                      database='jobsdb')
        jobsdb_cursor = cnx.cursor()
        jobsdb_cursor.execute(sql_rundeck)


if __name__ == '__main__':
    n = Jobsappdb()

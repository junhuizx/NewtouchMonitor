import MySQLdb

class Syslog(object):
    def __init__(self, syslog):
        self.id = syslog[0]
        self.received_time = syslog[2]
        self.priority = syslog[5]
        self.message = syslog[7]
        self.syslog_tag = syslog[20]

def get_syslog_message(mysql_host, mysql_db_name, mysql_db_user, mysql_db_password, syslog_tag):
    syslogs = []
    syslogdb = MySQLdb.connect(mysql_host,
                               mysql_db_user,
                               mysql_db_password,
                               mysql_db_name)
    cursor = syslogdb.cursor()

    sql = "SELECT * FROM SystemEvents WHERE SysLogTag = %s%s%s ORDER BY id DESC limit 1000" % ('"', syslog_tag, '"')
    row = cursor.execute(sql)

    results = cursor.fetchmany(row)

    for syslog in results:
        syslog = Syslog(syslog)
        syslogs.append(syslog)

    cursor.close()
    syslogdb.close()

    return syslogs
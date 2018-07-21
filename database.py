import mysql.connector
import dateutil.parser
from mysql.connector import errorcode


DB_NAME = 'vuln_scans'
DB_USER = 'root'
DB_PASSWORD = 'my-secret-pw'
DB_HOST = '127.0.0.1'
DB_PORT = '3310'

config = {
  'user': DB_USER,
  'password': DB_PASSWORD,
  'host': DB_HOST,
  'port': DB_PORT,
  'database': DB_NAME,
  'raise_on_warnings': True,
}

test_config = dict(config)
test_config['database'] = "test_vuln_scans"


def get_report(report_id,date,configure=test_config):
    try:
        cnx = mysql.connector.connect(**configure)
        cursor = cnx.cursor()
        param1 = (report_id,date)
        query = ("SELECT host, description, report_id, date from reports where report_id = %s and date = %s")
        cursor.execute(query, param1)
        data_dict = [{"description": row[1], "host": row[0], "report_id": row[2], "date": row[3]} for row in cursor.fetchall()]
        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)
        return
    return data_dict


def store_report(host, jsonstring, report_id, date, configure=test_config):
    try:
        cnx = mysql.connector.connect(**configure)
        jsonstring = str(jsonstring)
        cursor = cnx.cursor()
        conv_date = dateutil.parser.parse(date).date()
        param1 = (host, jsonstring, report_id, conv_date)
        query = ("INSERT into reports (host,description,report_id,date) VALUES (%s, %s, %s, %s)")
        cursor.execute(query, param1)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)
    return


def create_table(configure=test_config):
    cnx = mysql.connector.connect(**configure)
    cursor = cnx.cursor()
    query = ("CREATE TABLE IF NOT EXISTS `reports`( `id` int(11) NOT NULL AUTO_INCREMENT,`host` varchar(25), `description` longtext,`report_id` varchar(110), `date` date, primary key (`id`))")
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table Exists")
        else:
            print(err.msg)
        return
    else:
        print("OK")
        cnx.commit()
        cursor.close()
        cnx.close()
        return


def drop_table(configure=test_config):
    cnx = mysql.connector.connect(**configure)
    cursor = cnx.cursor()
    query = ("DROP Table reports")
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err.message)
    cnx.commit()
    cursor.close()
    cnx.close()
    return




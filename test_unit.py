import database
import unittest
from json import dumps
from requests import head
from openvas_lib import VulnscanManager


class flask_app_test(unittest.TestCase):

    DB_NAME = 'test_vuln_scans'
    DB_USER = 'root'
    DB_PASSWORD = 'my-secret-pw'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3310'

    test_config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'port': DB_PORT,
        'database': DB_NAME,
        'raise_on_warnings': True,
    }

    def setUp(self):
        database.create_table()
        database.store_report("Testhost",str(dumps({"keyfield1":"valuefield1","keyfield2":"valuefield2"})),"12345","2018-07-20", self.test_config)

    def tearDown(self):
        database.drop_table()

    def test_get_report_by_reportid(self):
        report = database.get_report("12345", "2018-07-20",self.test_config)
        self.assertEqual("Testhost",report[0]['host'])

    def test_non_existing_report(self):
        report = database.get_report("Non-Existing-Id", "2018-07-20", self.test_config)
        self.assertEqual(report,[])

    def test_endpoint_valid_url(self):
        response = head('http://localhost:5000/reports/12345/2018-07-20')
        self.assertNotEqual(response.status_code,400)

    def test_endpoint_invalid_url(self):
        response = head("http://localhost:5000/reports/123456/2018-07-201")
        self.assertEqual(response.status_code,400)

    def test_app_running(self):
        response = head("http://localhost:5000/")
        self.assertEqual(response.status_code,200)

    def test_app_error_handler(self):
        response = head("http://localhost:5000/non-existing-url")
        self.assertEqual(response.status_code,200)

    def test_openvas_manager_init(self):
        manager = VulnscanManager("localhost","admin", "admin")
        self.assertIsInstance(manager, VulnscanManager)


app_instance = flask_app_test()
app_instance.setUp()
app_instance.test_get_report_by_reportid()
app_instance.test_non_existing_report()
app_instance.test_endpoint_valid_url()
app_instance.test_endpoint_invalid_url()
app_instance.test_app_running()
app_instance.test_app_error_handler()
app_instance.test_openvas_manager_init()
app_instance.tearDown()




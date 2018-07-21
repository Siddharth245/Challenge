import vlnerability_scan
import urllib2
import datetime
import database
import test_unit


class integration_tests():

    report_id = ""
    test_config = ""

    def setUp(self):
        fat = test_unit.flask_app_test()
        fat.setUp()
        self.test_config = database.test_config

    def tearDown(self):
        fat = test_unit.flask_app_test()
        fat.tearDown()
        self.test_config = ""

    def test_check_store_data(self):
        self.report_id = vlnerability_scan.start_scan("192.168.0.32",self.test_config)
        if self.report_id:
            print"Store Data Successful"
        else:
            print"Unable to store the report"

    def test_retrieve_data(self):
        request_url = "http://localhost:5000/reports/"+self.report_id+"/"+datetime.date.today().isoformat()
        try:
            report = urllib2.urlopen(request_url)
            if report:
                print"Retrieve Data Successful"
            else:
                print"Unable to retrieve the report"
        except urllib2.HTTPError as e:
            print(e)

    def test_storage_retrieval(self):
        report_id = vlnerability_scan.start_scan("192.168.0.32",self.test_config)
        try:
            report = urllib2.urlopen("http://localhost:5000/reports/"+report_id+"/"+datetime.date.today().isoformat())
            if report:
                print"Data Storage and Retrieval Confirmed"
            else:
                print"Failed: Test individual integrations to diagnose"
        except urllib2.HTTPError as e:
            print(e)


app_instance = integration_tests()
app_instance.setUp()
app_instance.test_check_store_data()
app_instance.test_retrieve_data()
app_instance.test_storage_retrieval()
app_instance.tearDown()
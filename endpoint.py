from flask_restful import Resource
import database
import json
import datetime as dt


class reports(Resource):

    def get(self, report_id, date, config=database.test_config):
        try:
            if self.check_valid(report_id, date):
                result = database.get_report(report_id,date,config)
                if result:
                    jsondict = json.loads(result[0]['description'])
                    result[0]['description'] = jsondict
                    result[0]['date'] = str(result[0]['date'])
                    for target in result:
                        if target['report_id']==report_id and target['date']==str(date):
                            return target, 200
                else:
                    return "You have either requested invalid parameters or a non-existent report", 404
        except Exception as e:
            print(e)
            return "Bad Request", 400

    @staticmethod
    def check_valid(report_id, date):
            dt.datetime.strptime(date,"%Y-%m-%d")
            report_id = report_id.replace("-","")
            if report_id.isalnum():
                return True
            else:
                return False


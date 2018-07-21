from flask import Flask
from flask_restful import Api
from endpoint import reports
app = Flask(__name__)
api = Api(app)


@app.route('/')
def api_usage():
    return 'To use the api follow the url - http://server-ip-address/reports/<report-id>/<date(YYYY-MM-DD)>'


api.add_resource(reports, "/reports/<string:report_id>/<string:date>")


@app.errorhandler(404)
def error_not_found(e):
    return "To use the api follow the url - http://server-ip-address/reports/{report-id}/{date(YYYY-MM-DD)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

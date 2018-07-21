from __future__ import print_function
from openvas_lib import VulnscanManager
from threading import Semaphore
from functools import partial
from xml.etree import ElementTree
import sys
import json
import xmltodict
import database
import datetime


def my_print_status(i):
    print(str(i)),\
    sys.stdout.flush()


def run(manager, host,config):
    sem = Semaphore(0)
    scan_id, target_id = manager.launch_scan(
        target=host,
        profile="Full and fast",
        callback_end=partial(lambda x: x.release(), sem),
        callback_progress=my_print_status
    )
    sem.acquire()
    report_id = manager.get_report_id(scan_id)
    store_report(manager, report_id, host,config)
    return report_id


def store_report(manager, report_id, ip,config):
    try:
        report = manager.get_report_xml(report_id)
        report_xml = ElementTree.tostring(report, encoding='utf-8', method='xml')
        json_string = json.dumps(xmltodict.parse(report_xml), indent=4)
        report_date = datetime.date.today().isoformat()
        database.store_report(ip,json_string,report_id,report_date,config)
    except Exception as e:
        print("There was an exception: "+str(e))
        return


def start_scan(ip="104.25.81.107",config=database.config):
    try:
        scanner = VulnscanManager("localhost","admin","admin")
        report_id = run(scanner, ip,config)
    except Exception as e:
        print("Error:" + "\n" + str(e))
        return
    return report_id


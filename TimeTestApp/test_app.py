import json
import logging
import sched
import sys
import time
import timeit
from urllib.request import urlopen
from datetime import datetime

import requests

WEB_ADDRESS = sys.argv[1]
no_of_calls = sys.argv[2]
scheduler = sched.scheduler(time.time, time.sleep)
status_list = []


def site_status():
    last_byte_time = 'N/A'
    connect = 'failure'
    status_code = 'N/A'

    try:
        response = requests.get(WEB_ADDRESS, verify=False, timeout=15)
        logging.debug(response)
        if not response.raise_for_status():
            start_time = timeit.default_timer()
            with urlopen(WEB_ADDRESS) as http:
                http.read()
            last_byte_time = timeit.default_timer() - start_time
            connect = 'success'
            status_code = response.status_code
    except requests.exceptions.RequestException as req:
        logging.debug(req)

    _package_data(last_byte=last_byte_time, connect=connect, response_code=status_code)


def _package_data(last_byte, connect, response_code):
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    data = {'time_to_last_byte': last_byte,
            'connection_status': connect,
            'response_status_code': response_code,
            'time_of_log': now}

    status_list.append(data)


def _cycler(calls_per_second, callback, *args, **kw):
    period = 1.0 / calls_per_second

    def reload():
        callback(*args, **kw)
        scheduler.enter(period, 0, reload, ())

    scheduler.enter(period, 0, reload, ())


def _json_to_file(data):
    filename = _create_json_filename()

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)
    json_file.close()


def _create_json_filename():
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    logging.debug('filename is %s.json', now)
    return f'{now}.json'


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        while True:
            _cycler(int(no_of_calls), site_status)
            logging.debug('Running cycler')
            scheduler.run()
    except KeyboardInterrupt:
        logging.info('Cycle interrupted by user')
    finally:
        logging.debug('json logs saving to file')
        _json_to_file(status_list)


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        raise e

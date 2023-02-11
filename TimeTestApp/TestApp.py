import json
import logging
import sched
import sys
import time
import timeit
import urllib
from datetime import datetime

import keyboard
import requests

web_address = sys.argv[1]
no_of_calls = sys.argv[2]
scheduler = sched.scheduler(time.time, time.sleep)
status_list = []


def site_status():
    response = requests.get(web_address)
    logging.debug(response)

    if not response.raise_for_status():
        try:
            start_time = timeit.default_timer()
            http = urllib.request.urlopen(web_address)
            http.read()
            last_byte_time = timeit.default_timer() - start_time
            connect = 'success'
        except Exception as err:
            errno, errstr = err
            raise OSError('An error occurred: {}'.format(errstr))
    else:
        last_byte_time = 'N/A'
        connect = 'failure'

    _package_data(last_byte=last_byte_time, connect=connect, response_code=response.status_code)


def _package_data(last_byte, connect, response_code):
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    data = {'time_to_last_byte': last_byte,
            'connection_status': connect,
            'response_status_code': response_code,
            'time_of_log': now}
    logging.debug(data)

    status_list.append(data)


def _cycler(calls_per_second, callback, *args, **kw):
    period = 1.0 / calls_per_second

    def reload():
        callback(*args, **kw)
        scheduler.enter(period, 0, reload, ())

    scheduler.enter(period, 0, reload, ())


def _json_to_file(data):
    filename = _create_json_filename()

    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    json_file.close()


def _create_json_filename():
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    logging.debug(f'filename is {now}.json')
    return f'{now}.json'


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        while True:
            _cycler(int(no_of_calls), site_status)
            logging.debug("Running cycler")
            scheduler.run()
    except KeyboardInterrupt or keyboard.is_pressed('q'):
        _json_to_file(status_list)


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        raise e
    except Exception as ex:
        logging.info(str(ex))
        sys.exit(1)

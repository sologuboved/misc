import csv
from functools import wraps
import json
import os
import re
import sys
import time


class Singleton(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CsvWriter:
    def __init__(self, csv_filename, headers=None, as_dict=False):
        print(f"Downloading {csv_filename}...")
        self._csv_filename = csv_filename
        self._headers = headers
        self._as_dict = as_dict
        self._count = 0
        self._writer = self.csv_writer()
        next(self._writer)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def bulk(self, bulk):
        self._count += len(bulk)
        for row in bulk:
            self._writer.send(row)

    def write(self, row):
        self._count += 1
        self._writer.send(row)

    def close(self):
        self._writer.close()
        print(f"\nTotal: {self._count} row(s)")

    def csv_writer(self):
        with open(self._csv_filename, 'w', newline='', encoding='utf-8') as handler:
            if self._as_dict:
                first_row = yield
                if not self._headers:
                    self._headers = sorted(first_row.keys())
                writer = csv.DictWriter(handler, fieldnames=self._headers, restval=None)
                writer.writeheader()
                writer.writerow(first_row)
            else:
                writer = csv.writer(handler)
                if self._headers:
                    writer.writerow(self._headers)
            while True:
                writer.writerow((yield))


def which_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        def report_time():
            print("'{}' took {}".format(
                func.__name__,
                time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - start)),
            ))

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except BaseException as e:
            raise e
        else:
            return result
        finally:
            report_time()

    return wrapper


def dump_utf_json(entries, json_file):
    num_entries = len(entries)
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)
    print(f"Dumped {num_entries} entry/ies to {json_file}")


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def read_csv(csv_fname, as_dict=False, delimiter=',', has_headers=True):
    with open(csv_fname, newline=str()) as handler:
        if as_dict:
            assert has_headers, "Doesn't have headers"
            for row in csv.DictReader(handler, delimiter=delimiter):
                yield row
        else:
            reader = csv.reader(handler, delimiter=delimiter)
            if has_headers:
                next(reader)
            for row in reader:
                yield row


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname):
    return os.path.join(get_base_dir(), fname)


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = get_abs_path('{}_{}.pid'.format(prefix, str(os.getpid())))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir(get_base_dir()):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return get_abs_path(fname)

import argparse
import os
import re
import sys
from datetime import datetime

from boto.s3.connection import S3Connection
from celery import shared_task, Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('open_fmri')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# copied from http://blog.kowalczyk.info/article/a1e/Parsing-s3-log-files-in-python.html - START
s3_line_logpats  = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) ' \
           r'(\S+) (\S+) (\S+) "([^"]+)" ' \
           r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) ' \
           r'"([^"]+)" "([^"]+)"'
s3_line_logpat = re.compile(s3_line_logpats)

s3_names = ("bucket_owner", "bucket", "datetime", "ip", "requestor_id", 
"request_id", "operation", "key", "http_method_uri_proto", "http_status", 
"s3_error", "bytes_sent", "object_size", "total_time", "turn_around_time",
"referer", "user_agent")
# END

AWS_ACCESS_KEY = os.environ.get('S3_LOG_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('S3_LOG_SECRET_KEY')
BUCKET_NAME = os.environ.get('S3_LOG_BUCKET')
PREFIX = os.environ.get('S3_LOG_PREFIX')
PARSED_FILES = os.environ.get('S3_LOG_PARSED_FILES')
OUT_DIR = os.environ.get('S3_LOG_PARSE_OUT_DIR')

@app.task(name='test_parse')
def test_parse():
    parse_log_files()

def parse_log_files():
    """Parse S3 log files that reside in an S3 bucket

    The contents of BUCKET_NAME are iterated over. Already parsed files have 
    their filename added to PARSED_FILES to prevent duplicate parsing.
    """
    parsed_files = open(PARSED_FILES, 'r+')
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    for key in bucket.list(prefix=PREFIX):
        parsed = False
        for line in parsed_files:
            if key.key in line:
                parsed = True
                break
        
        if not parsed:
            print(key.key)
            contents = str(key.get_contents_as_string())
            print(contents)
            parse_str(contents)
            parsed_files.write(key.key + key.size + '\n')


def parse_str(contents):
    """Writes the download count for a file referenced in an S3 log to a file
    
    Iterates through the contents of a log file. Each unique filename has a 
    count for each time its seen. For each filename that is seen a local file 
    with the same name is created and the download count stored in it.

    We ignore entries where no actual bytes are transferred.
    """
    parsed_data = {}
    for log_line in contents.splitlines():
        match = s3_line_logpat.match(log_line)
        if match is not None:
            parsed_line = [match.group(1+n) for n in range(17)]
            is_get_request = False
            is_valid_file = False
            filename = ''
            for (name, val) in zip(s3_names, parsed_line):
                if name == 'operation' and val == 'REST.GET.OBJECT':
                    print(val)
                    is_get_request = True
                elif name == 'key' and val is not '-' and val[-1:] is not '/' and is_get_request:
                    print(val)
                    filename = val
                    is_valid_file = True
                elif name == 'bytes_sent' and val is '-':
                    print(val)
                    is_valid_file = False
                else:
                    pass
            if is_valid_file:
                try:
                    parsed_data[filename] += 1
                except KeyError:
                    parsed_data[filename] = 1
    
    for filename in parsed_data:
        out_file = os.path.join(OUT_DIR, filename)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        if os.path.exists(out_file):
            out_fp = open(out_file, 'r+')
            count = int(out_fp.read())
            count += parsed_data[filename]
            out_fp.seek(0)
            out_fp.write(str(count))
            out_fp.close()
        else:
            out_fp = open(out_file, 'w')
            out_fp.write(str(parsed_data[filename]))
            out_fp.close()


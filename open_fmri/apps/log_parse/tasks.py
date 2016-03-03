import argparse
from datetime import datetime
import json
import os
import re
import sys

from boto.s3.connection import S3Connection
from celery import Celery, task, shared_task
from celery.utils.log import get_task_logger
import requests

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from log_parse.models import LogFile, S3File

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

def log_to_endpoint(message):
    if not settings.LOG_ENDPOINT:
        return
    try:
        payload = {'text': message}
        requests.post(settings.LOG_ENDPOINT, data=json.dumps(payload))
    except:
        pass
    return
    

@app.task(name='log_parse_task')
def log_parse_task():
    
    lock_id = "parse_log_files"    
    acquire_lock = lambda: cache.add(lock_id, 'true')
    release_lock = lambda: cache.delete(lock_id)
    
    if acquire_lock():
        try:
            log_to_endpoint("Lock acquired, starting parse task")
            parse_log_files()
            log_to_endpoint("Exiting parse task")
        finally:
            release_lock()
    
    return
 
def parse_log_files():
    """Parse S3 log files that reside in an S3 bucket

    The contents of BUCKET_NAME are iterated over. Already parsed files have 
    their filename added to PARSED_FILES to prevent duplicate parsing.
    """
       
    aws_access_key = os.environ.get('S3_LOG_ACCESS_KEY')
    aws_secret_key = os.environ.get('S3_LOG_SECRET_KEY')
    bucket_name = os.environ.get('S3_LOG_BUCKET')
    prefix = os.environ.get('S3_LOG_PREFIX')
    
    conn = S3Connection(aws_access_key, aws_secret_key)
    bucket = conn.get_bucket(bucket_name)
    file_count = 0
    for key in bucket.list(prefix=prefix):
        try:
            log_file = LogFile.objects.get(key=key.key)
            if (log_file.parsed is False) and (log_file.lock is False):
                log_file.lock = True
                log_file.save()
            else:
                continue
        except ObjectDoesNotExist:
            log_file = LogFile(key=key.key, parsed=False, lock=True)
            log_file.save()
        
        contents = str(key.get_contents_as_string())
        parse_str(contents)
        
        log_file.parsed = True
        log_file.lock = False
        log_file.save()
        
def parse_log_files_locally(path_to_logs):
    """Parse S3 log files that are local

    Intended to be run manually, has no provisions for locking that the 
    normal task has.
    """
    for log in os.listdir(path_to_logs):
        try:
            key = "logs/" + log
            log_file = LogFile.objects.get(key=key)
        except ObjectDoesNotExist:
            contents = open(path_to_logs + log, 'r').read()
            key = "logs/" + log
            print(key)
            parse_str(contents)
            log_file = LogFile(key=key, parsed=True, lock=False)
            log_file.save()
    

def parse_str(contents):
    """Writes the download count for a file referenced in an S3 log to database
    
    Iterates through the contents of a log file. Each unique filename has a 
    count for each time its seen. For each filename that is seen an entry in 
    the database is created and count stored.    
    
    We ignore entries where no bytes are transferred, any response other than 
    a 200 was seen, if it wasn't a GET OBJECT, or the filename is blank 
    """
    parsed_data = {}
    for log_line in contents.splitlines():
        match = s3_line_logpat.match(log_line)
        if match is not None:
            parsed_line = [match.group(1+n) for n in range(17)]
            is_get_request = True
            is_valid_file = False
            count_flag = True
            filename = ''
            for (name, val) in zip(s3_names, parsed_line):
                if name == 'operation' and val != 'REST.GET.OBJECT':
                    count_flag = False
                else:
                    pass
                if name == 'http_status' and val != '200':
                   count_flag = False 
                if name == 'key':
                    filename = val
                if name == 'key' and val is '-':
                    count_flag = False
                if name == 'bytes_sent' and val is '-':
                    count_flag = False
            if count_flag:
                try:
                    parsed_data[filename] += 1
                except KeyError:
                    parsed_data[filename] = 1
    
    for filename in parsed_data:
        try:
            s3_file = S3File.objects.get(filename=filename)
            s3_file.count += parsed_data[filename]
            s3_file.save()
        except ObjectDoesNotExist:
            s3_file = S3File(filename=filename, count=parsed_data[filename])
            s3_file.save()

# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
from uspto.pbd.tasks import download

def download_single(query):

    # 1. synchronously
    #result = download(query)
    #print result.get()

    # 2. asynchronously
    # http://docs.celeryproject.org/en/latest/userguide/calling.html
    result = download.delay(query_real)
    print result.get_leaf()

def download_multi(queries):
    # https://celery.readthedocs.io/en/latest/userguide/canvas.html#map-starmap
    results = ~download.map(queries)
    print 'results:', results
    for result in results:
        print result.get()

if __name__ == '__main__':
    #download_single('hello world')
    download_multi(['hello world', 'foo bar', 'baz qux'])

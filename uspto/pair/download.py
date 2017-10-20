# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>
import time
import json
import logging
from uspto.pair.tasks import download

logger = logging.getLogger(__name__)

def download_single(query):

    # http://docs.celeryproject.org/en/latest/userguide/calling.html
    logger.info('Starting download of "%s"', query)
    task = download(query)
    logger.info('Task id is "%s"', task.id)
    try:
        while not task.ready():
            logger.info('Task %s in state %s', task.id, task.state)
            time.sleep(1)

        result = task.get()
        logger.info('Download succeeded')
        print(json.dumps(result, indent=4))

    except Exception as ex:
        logger.error('Download failed with exception: "%s"', ex)

def download_multi(queries):
    # https://celery.readthedocs.io/en/latest/userguide/canvas.html#map-starmap

    tasks = ~download.map(queries)

    logger.info('Starting download of "%s"', queries)

    while tasks:

        for task in tasks:

            if task.ready():
                logger.info('Task %s in state %s.', task.id, task.state)

                try:
                    result = task.get()
                    logger.info('Download succeeded')
                    print(json.dumps(result, indent=4))

                except Exception as ex:
                    logger.error('Download failed with exception: "%s"', ex)

                tasks.remove(task)

            else:
                logger.info('Task %s in state %s. Metadata: %s', task.id, task.state, task.info)

        time.sleep(1)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    #download_single({'patent': '11673'})
    #download_single({'patent': 'PP28532'})
    download_multi([{'patent': 'PP28532'}, {'publication': '11673'}])
    #download_multi([{'patent': 'PP28532'}, {'publication': '2017-0293197'}, {'publication': '11673'}, {'patent': 'PP28532'}])


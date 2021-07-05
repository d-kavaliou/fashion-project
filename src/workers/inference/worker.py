import os
import s3fs
import traceback

from celery import Celery, states
from celery.exceptions import Ignore
from celery.utils.log import get_logger
from typing import Any, Dict

BUCKET_NAME = os.getenv("BUCKET_NAME")
DATA_FOLDER = os.getenv("DATA_FOLDER")

logger = get_logger(__name__)
imagery = Celery("inference", broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))


@imagery.task(bind=True, name="inference")
def inference_task(self, previous_task, **kwargs) -> Dict[str, Any]:
    logger.info(f'Start executing task {kwargs}')

    s3_target = f's3://{BUCKET_NAME}/{previous_task.id}'
    s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': f'http://{os.getenv("S3_HOST")}:4566'})

    try:
       files = s3.ls(f'{s3_target}/images')
    except Exception as e:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(e).__name__,
                'exc_message': str(e),
                'traceback': traceback.format_exc().split('\n')
            }
        )
        raise Ignore()

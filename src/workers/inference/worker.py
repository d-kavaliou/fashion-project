import os
import s3fs
import json
import traceback
import yaml

from celery import Celery, states
from celery.exceptions import Ignore
from celery.utils.log import get_logger
from typing import Any, Dict

from engine import FashionInference

logger = get_logger(__name__)
inference = Celery("inference", broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))

with open("config.yml", "r") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)
inference_engine = FashionInference(CONFIG['model'])


@inference.task(bind=True, name="model")
def inference_task(self, task_output) -> Dict[str, Any]:
    logger.info(f'Start executing task on {task_output}')

    s3_target = task_output['s3_target']
    s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': f'http://{os.getenv("S3_HOST")}:4566'})

    try:
        image_names = list(map(os.path.basename, s3.ls(f'{s3_target}/images')))
        results = inference_engine.predict(image_names)
        logger.info(len(results))
        if results:
            dump_result = f'{s3_target}/predictions.json'
            with s3.open(dump_result, 'w') as dump_f:
                json.dump(results, dump_f)

            return {'s3_target': s3_target}
        else:
            raise ValueError('Cannot generate predictions: empty predictions result.')
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


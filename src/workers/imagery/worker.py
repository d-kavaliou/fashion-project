from celery.utils.log import get_logger
from typing import Any, Dict
import traceback
import s3fs
import os
import json
import yaml

from app.database import filter_products
from app.augmentation import Transformer

from celery import Celery, states
from celery.exceptions import Ignore


logger = get_logger(__name__)
imagery = Celery("imagery", broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))

with open("config.yml", "r") as f:
    worker_config = yaml.load(f, Loader=yaml.FullLoader)

BUCKET_NAME = os.getenv("BUCKET_NAME")
DATA_FOLDER = os.getenv("DATA_FOLDER")


@imagery.task(bind=True, name="filter")
def filter_task(self, **kwargs) -> Dict[str, Any]:
    logger.info(f'Start executing task {kwargs}')

    s3_target = f's3://{BUCKET_NAME}/{self.request.id}'
    s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': f'http://{os.getenv("S3_HOST")}:4566'})

    try:
        products = filter_products(self.request.kwargs)

        if products:
            result = list(map(dict, products))

            with s3.open(f'{s3_target}/metadata.json', 'w') as f:
                json.dump(result, f)

            for product in result:
                image_name = f"{product['image_id']}.jpg"
                s3.upload(os.path.join(DATA_FOLDER, image_name), f'{s3_target}/images/{image_name}')

            if kwargs['apply_augmentation']:
                logger.info(f'Applying augmentation')
                transformer = Transformer(worker_config['albumentation'], DATA_FOLDER)

                for image_name, image_aug in transformer.apply(result):
                    with s3.open(f'{s3_target}/augmentation/{image_name}', 'wb') as f:
                        f.write(image_aug)

        return {
            's3_target': s3_target
        }
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

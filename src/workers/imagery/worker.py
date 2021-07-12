import os
import json
import s3fs
import traceback
import yaml

from celery import Celery, states
from celery.exceptions import Ignore
from celery.utils.log import get_logger
from typing import Any, Dict

from app.database import filter_products
from app.augmentation import Transformer
from app.uploader import Uploader

BUCKET_NAME = os.getenv("BUCKET_NAME")
DATA_FOLDER = os.getenv("DATA_FOLDER")

with open("config.yml", "r") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)

logger = get_logger(__name__)
imagery = Celery("imagery", broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))


@imagery.task(bind=True, name="filter")
def filter_task(self, **kwargs) -> Dict[str, Any]:
    logger.info(f'Start executing task {kwargs}')

    s3_target = f's3://{BUCKET_NAME}/{self.request.id}'
    s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': f'http://{os.getenv("S3_HOST")}:4566'})

    try:
        products = filter_products(self.request.kwargs)

        if products:
            result = list(map(dict, products))

            with s3.open(f'{s3_target}/metadata.json', 'w') as meta_f:
                json.dump(result, meta_f)

            uploader = Uploader(DATA_FOLDER, f'{s3_target}/images')
            uploader.upload(map(lambda product: f"{product['image_id']}.jpg", result))

            if kwargs['apply_augmentation']:
                logger.info(f'Applying augmentation')
                transformer = Transformer(CONFIG['albumentation'], DATA_FOLDER, logger)

                for image_name, image_aug in transformer.apply(map(lambda row: row['image_id'], result)):
                    with s3.open(f'{s3_target}/augmentation/{image_name}', 'wb') as aug_f:
                        aug_f.write(image_aug)

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


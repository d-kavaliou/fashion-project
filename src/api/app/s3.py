import json
import localstack_client.session as boto3

from fastapi.logger import logger

BUCKET_NAME = 'fashion-tasks'

s3_client = boto3.client('s3')


def upload_result(data, path):
    try:
        s3_client.put_object(
            Body=json.dumps(data),
            Bucket=BUCKET_NAME,
            Key=path
        )
    except Exception as ex:
        logger.error(ex)
        raise Exception(f"Couldn't upload resulting json file: {ex}")

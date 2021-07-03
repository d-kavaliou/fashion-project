import json
import os
import aiobotocore

from fastapi import HTTPException
from fastapi.logger import logger

BUCKET_NAME = 'fashion-tasks'
S3_HOST = os.getenv("S3_HOST")
S3_PORT = '4566'

session = aiobotocore.get_session()


async def upload_result(data, path):
    try:
        async with session.create_client('s3', endpoint_url=f'http://{S3_HOST}:{S3_PORT}') as client:
            await client.put_object(Body=json.dumps(data), Bucket=BUCKET_NAME, Key=path)

        return f's3://{BUCKET_NAME}/{path}'
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(detail=f"Couldn't upload resulting json file: {ex}", status_code=500)

import os
import s3fs

from multiprocessing.pool import ThreadPool
from typing import Any, List


class Uploader:
    """
    A class for multi threading uploading of the files to s3.
    Use ThreadPool, because I/O bunch of work(s3 uploading)
    """
    def __init__(self, imagery_folder: str, target_folder: str):
        """
        :param imagery_folder:
            Source path for imagery data in filesystem
        :param target_folder:
            Target S3 path for imagery data
        """
        self._s3 = s3fs.S3FileSystem(client_kwargs={'endpoint_url': f'http://{os.getenv("S3_HOST")}:4566'})
        self._imagery_folder = imagery_folder
        self._target_folder = target_folder

    def upload(self, images: List[Any]) -> None:
        with ThreadPool() as pool:
            params = [(os.path.join(self._imagery_folder, image), f'{self._target_folder}/{image}') for image in images]
            # lambda is used to unpack params for s3fs upload function
            pool.map(lambda item: self._s3.upload(item[0], item[1]), params)
        pool.join()

import os
import cv2
import albumentations as A

from multiprocessing import Pool
from typing import Any, Tuple, List

class Transformer:
    """
    A class to perform imagery transforms on the provided imagery.
    Use Pool to perform CPU bound actions on several cores
    """
    def __init__(self, config, imagery_folder, logger):
        """
        :param config:
            Yaml config for albumentation actions
        :param imagery_folder:
            A path to imagery folder
        :param logger:
            A logger to be shared across processes
        """
        self._config = config
        self._imagery_folder = imagery_folder
        self._transforms = self._buil_aug(config)
        self._logger = logger

    def _buil_aug(self, config: dict) -> Any:
        """
        Build albumentation composed action based on the provided config
        :param config:
            Specific albumentation config
        :return:
        """
        image_config = config['input_image']
        w2h_ratio = image_config['width'] / image_config['height']

        return A.Compose([
            A.RandomSizedCrop((config['cropping']['height']['min'], config['cropping']['height']['max']),
                              config['resize']['height'], config['resize']['width'],
                              w2h_ratio=w2h_ratio, always_apply=True)
        ])

    def worker_func(self, image_id: str) -> Tuple[str, Any]:
        """
        Worker function that reads an image and apply transforms on it. Returns tuple withe the name and imagery bytes
        :param image_id:
        :return:
        """
        try:
            file_name = f"{image_id}.jpg"

            # read in BGR format
            image = cv2.imread(os.path.join(self._imagery_folder, file_name))
            augmented = self._transforms(image=image)

            # convert to bytes and RGB format
            _, image_buffer = cv2.imencode(".jpg", augmented['image'])

            return file_name, image_buffer
        except Exception as ex:
            self._logger.error(f"Couldn't transform an image {image_id} due to {ex}")
            return None

    def apply(self, image_ids: List[str]) -> Tuple[str, Any]:
        """
        A generator function to return image_name and transformed image to the main process
        :param image_ids:
            List of image ids to be transformed
        :return:
        """
        with Pool() as pool:
            for result in pool.map(self.worker_func, image_ids):
                if result:
                    yield result[0], result[1]

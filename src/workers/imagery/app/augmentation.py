import os
import cv2
import albumentations as A


class Transformer:
    def __init__(self, config, imagery_folder):
        self.config = config
        self.imagery_folder = imagery_folder
        self.transforms = self._buil_aug(config)

    def _buil_aug(self, config):
        image_config = config['input_image']
        w2h_ratio = image_config['width'] / image_config['height']

        return A.Compose([
            A.RandomSizedCrop((config['cropping']['height']['min'], config['cropping']['height']['max']),
                              config['resize']['height'], config['resize']['width'],
                              w2h_ratio=w2h_ratio, always_apply=True)
        ])

    def apply(self, products):
        for item in products:
            file_name = f"{item['image_id']}.jpg"

            # read in BGR format
            image = cv2.imread(os.path.join(self.imagery_folder, file_name))

            augmented = self.transforms(image=image)

            # convert to bytes and RGB format
            _, image_buffer = cv2.imencode(".jpg", augmented['image'])

            yield file_name, image_buffer

from typing import Any, List

import cv2
import numpy as np
import pandas as pd
import s3fs
from torch.utils.data import Dataset


class ImagesDataset(Dataset):
    def __init__(self, images: List[str], transforms: Any = None):
        self._images = images
        self._transforms = transforms

    def __len__(self) -> int:
        return len(self._images)

    def __getitem__(self, idx: int) -> dict:
        image_name = self._images[idx]

        #TODO: Read image

        if self._transforms:
            data = self._transforms(**data)

        return data

import os
import torch
import albumentations as A

from typing import List
from torch.utils.data import DataLoader
from albumentations.pytorch.transforms import ToTensorV2

from model.deepfashion import FashionNetVgg16NoBn
from utils.dataset import ImagesDataset

DATA_FOLDER = os.getenv("DATA_FOLDER")


class FashionInference:
    def __init__(self, config):
        self._device = os.getenv("INFERENCE_DEVICE")
        self._batch_size = int(os.getenv("BATCH_SIZE"))
        self._num_workers = int(os.getenv("NUM_WORKERS"))
        self._transforms = FashionInference._build_transforms(config['preprocessing'])

        self._model = FashionNetVgg16NoBn().to(self._device)
        self._model.eval()

    @staticmethod
    def _build_transforms(config):
        return A.Compose([
            A.Resize(width=config['resize']['width'], height=config['resize']['height']),
            A.Normalize(),
            ToTensorV2()
        ])

    def predict(self, images: List[str]) -> List[dict]:
        """
        Apply model inference to the provided imagery collection
        :param images:
            List of image names
        :return:
            List of dict predicted attributes
        """

        dataset = ImagesDataset(images, DATA_FOLDER, self._transforms, self._device)
        loader = DataLoader(dataset, batch_size=self._batch_size, num_workers=self._num_workers)

        pred_massive_attr, pred_categories = [], []
        with torch.no_grad():
            for batch in loader:
                prediction = self._model(batch)
                pred_massive_attr.extend(prediction[0])
                pred_categories.extend(prediction[1])

        results = []
        for image_id, massive_attr, categories in zip(images, pred_massive_attr, pred_categories):
            results.append({
                'image_id': image_id,
                'massive_attr': massive_attr.numpy().tolist(),
                'categories': categories.numpy().tolist()
            })

        return results

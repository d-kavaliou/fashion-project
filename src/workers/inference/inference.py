import torch

from typing import List
from torch.utils.data import DataLoader

from model.deepfashion import FashionNetVgg16NoBn
from utils.dataset import

class FashionInference:
    def __init__(self, device, batch_size, num_workers):
        self._device = device
        self._batch_size = batch_size
        self._num_workers = num_workers

        self._model = FashionNetVgg16NoBn().to(device)
        self._transform = None

    def predict(self, images: List[str]) -> List[dict]:
        """
        Apply model inference to the provided imagery collection
        :param images:
            List of image names
        :return:
            List of dict predicted attributes
        """

        dataset = ImagesDataset(images, self._transform)
        loader = DataLoader(dataset, batch_size=self._batch_size, num_workers=self._num_workers)

        results = []
        with torch.no_grad():
            for batch in loader:
                batch = [img.to(self._device) for img in batch]
                prediction = self._model(batch)
                results.extend(prediction)

        return results

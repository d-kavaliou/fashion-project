import os
import logging
import argparse
import numpy as np
import pandas as pd

from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', type=str, required=True, help='Path to the dataset (should be extracted)')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to dump prepared dataset')

    args = parser.parse_args()
    data = pd.read_csv(os.path.join(args.dataset, 'styles.csv'), error_bad_lines=False)

    # get images from folder to leave records with existed image id
    images = [Path(file_name).stem for file_name in os.listdir(os.path.join(args.dataset, 'images'))]

    data = data[data['id'].isin(images)]
    data['year'] = data['year'].apply(lambda y: str(int(y)) if not np.isnan(y) else "null")

    if not os.path.exists(args.output):
        os.makedirs(Path(args.output).parent)

    data.to_csv(args.output, header=False)


if __name__ == "__main__":
    main()

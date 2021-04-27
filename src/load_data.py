import os
from src.get_data import get_data, read_params, get_base_dir

import argparse


def load_and_save(config_path):
    config = read_params(config_path=config_path)
    df = get_data(config_path)
    new_cols = [col.replace(" ", "_") for col in df.columns]
    df.columns = new_cols
    raw_data_path = os.path.join(config['load_data']['raw_dataset_csv'])
    #raw_data_path = raw_data_path
    df.to_csv(raw_data_path, index=False)
    print(raw_data_path)
    print(new_cols)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)

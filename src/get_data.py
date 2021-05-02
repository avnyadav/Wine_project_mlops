## read the paramters

## process

## return the data frame

import os
import yaml
import pandas as pd
import argparse


# checking

def read_params(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config


def get_base_dir():
    base = os.getcwd()
    base = base[::-1]
    idx = base.find("\\")
    base = base[idx:]
    base = base[::-1]
    return base


def get_data(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["s3_source"]
    # base=get_base_dir()
    df = pd.read_csv(os.path.join(data_path))
    print(df.head())
    return df


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    get_data(parsed_args.config)

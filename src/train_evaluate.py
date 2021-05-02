import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error \
    , mean_absolute_error, r2_score

from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
from get_data import read_params
import argparse
import joblib
import json


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    model_dir = config['model_dir']
    random_state = config["base"]["random_state"]

    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    target_column = config['base']['target_col']
    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    train = pd.read_csv(train_data_path)
    test = pd.read_csv(test_data_path)

    train_y = train[target_column]
    test_y = test[target_column]

    train_x = train.drop(target_column, axis=1)
    test_x = test.drop(target_column, axis=1)

    lr = ElasticNet(
        alpha=alpha,
        l1_ratio=l1_ratio,
        random_state=random_state)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print(f"Elasticnet model (alpha={alpha},l1_ration={l1_ratio}):")
    print(f"RMSE: {rmse}")
    print(f"MAE: {mae}")
    print(f"R2: {r2}")

    with open(scores_file, "w") as file:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, file, indent=4)
    with open(params_file,"w") as file:
        params={
            "alpha":alpha,
            "l1_ratio":l1_ratio
        }
        json.dump(params,file,indent=4)
    os.makedirs(model_dir, exist_ok=True)
    model_dir = os.path.join(model_dir, "model.joblib")
    joblib.dump(lr, model_dir)

    # with open('scores_file',"w") as f:
    # pass


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)

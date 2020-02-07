from read import read_data, count_missing
from model import train_model_dnn  # , load_model_dnn
# import numpy as np
# import pandas as pd


def main():
    train = read_data("train")
    print(train.columns)
    count_missing(train)
    df_train_Y = train[["isFraud"]]
    df_train_X = train.drop(["isFraud"], axis=1)
    train_Y = df_train_Y.to_numpy()
    train_X = df_train_X.to_numpy()
    train_model_dnn(train_X, train_Y)


if __name__ == "__main__":
    main()

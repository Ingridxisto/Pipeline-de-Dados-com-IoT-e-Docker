import pandas as pd


def load_csv(file_path='csv/IOT-temp.csv'):
    data = pd.read_csv(file_path)
    return data

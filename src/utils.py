import pandas as pd


def get_data_df(path: str) -> pd.DataFrame:
    """Функция получения датафрейма из файла operations.csv"""

    df = pd.read_csv(path)
    return df

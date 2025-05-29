import pandas as pd


def get_data_df(path: str) -> pd.DataFrame:
    """Функция получения датафрейма из файла operations.csv"""

    df = pd.read_csv(path)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].str.replace(",", ".")
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].astype('float')
    return df

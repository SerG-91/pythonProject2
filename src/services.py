import pandas as pd


def search_tel(df: pd.DataFrame) -> list:
    pattern = r'\b \W+7\W\d{3}\W\d{3}-\d{2}-\d{2}'
    filtered_data = df[df['Описание'].str.contains(pattern, na=False)]
    return filtered_data.to_json(orient='records', force_ascii=False, indent=4)


def search_name(df: pd.DataFrame) -> list:
    pattern = r'\b\D* \D\.$'
    filtered_data = df[df['Описание'].str.contains(pattern, na=False)]
    return filtered_data.to_json(orient='records', force_ascii=False, indent=4)


# if __name__ == "__main__":
#     path_csv = os.path.join(DATA_DIR, "operations.csv")
#     df_load = get_data_df(path_csv)
#
#     print(search_name(df_load[:6]))

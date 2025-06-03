import logging
from typing import Any

import pandas as pd

from config import LOGS_DIR

logger = logging.getLogger("services")
logger.setLevel("INFO")
file_handler = logging.FileHandler(f"{LOGS_DIR}/services.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_tel(df: pd.DataFrame) -> Any:
    pattern = r"\b \W+7\W\d{3}\W\d{3}-\d{2}-\d{2}"
    filtered_data = df[df["Описание"].str.contains(pattern, na=False)]
    logger.info("Функция search_tel возвращает отредактированный список согласно паттерна")
    return filtered_data.to_json(orient="records", force_ascii=False, indent=4)


def search_name(df: pd.DataFrame) -> Any:
    pattern = r"\b\D* \D\.$"
    filtered_data = df[df["Описание"].str.contains(pattern)]
    logger.info("Функция search_name возвращает отредактированный список согласно паттерна")
    return filtered_data.to_json(orient="records", force_ascii=False, indent=4)

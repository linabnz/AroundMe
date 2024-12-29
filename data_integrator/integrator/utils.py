import pandas as pd
import json
import re
from pathlib import Path
from unidecode import unidecode

def normalize_adress(s):
    if pd.isna(s):
        return ""
    s = unidecode(s)  
    s = re.sub(r'[^\w]', '', s)
    s = s.lower()
    replacements = {
        "de": "",
        "av": "avenue",
        "bd": "boulevard",
        "pl": "place"
    }
    for key, value in replacements.items():
        s = s.replace(key, value)
    return s

def fill_string_not_specified(data):
    category_columns = data.select_dtypes(include=["object"]).columns
    data[category_columns] = data[category_columns].fillna("not specified")
    return data

def get_data_path(data_name, stage="raw"):
    base_path = Path("../../data")
    return base_path / f"{data_name}_data_{stage}.{'csv' if stage != 'raw' else 'json' if data_name in ['museum', 'sports'] else 'csv'}"

def load_json_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
from core.normalizer import Normalizer
from core.reader import Reader
from pathlib import Path
import pandas as pd
from config import OUTPUT_PATH
import os
from util.xlsx_functions import get_available_path
from tkinter import messagebox

class Updater():
    def consolidate_sells(self, path: Path, normalizer:Normalizer, name = f"OUTPUT.xlsx") -> None:
        try:
            df_list = normalizer.read(path)
            df_list = [normalizer.normalize_sells(df) for df in df_list]
            result_df = pd.concat(df_list)
            if not os.path.exists(OUTPUT_PATH):
                os.makedirs(OUTPUT_PATH)
            path = path.joinpath(OUTPUT_PATH, name)
            path = get_available_path(path)
            result_df.to_excel(path, index=False)
            return path
        except Exception as e:
            print(e)
            messagebox.Message("Algo fue mal")

    def create_stock(self, path: Path, normalizer:Normalizer, name = f"STOCK-OUTPUT.xlsx") -> None:
        try:
            df = normalizer.read_stock(path)
            df_result = normalizer.normalize_stock(df)
            if not os.path.exists(OUTPUT_PATH):
                os.makedirs(OUTPUT_PATH)
            path = path.joinpath(OUTPUT_PATH, name)
            path = get_available_path(path)
            df_result.to_excel(path, index=False)
            return path
        except Exception as e:
            print(e)
            messagebox.ERROR("Algo fue mal")
        


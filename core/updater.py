from core.normalizer import Normalizer
from core.reader import Reader
from pathlib import Path
import pandas as pd
from config import OUTPUT_PATH
import os

class Updater():
    def consolidate_sells(self, path: Path, normalizer:Normalizer) -> None:
        df_list = normalizer.read(path)
        df_list = [normalizer.normalize_sells(df) for df in df_list]
        result_df = pd.concat(df_list)
        name = f"OUTPUT-{normalizer}.xlsx"
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

        result_df.to_excel(path.joinpath(OUTPUT_PATH, name), index=False)

    def create_stock(self, path: Path, normalizer:Normalizer) -> None:
        df = normalizer.read_stock(path)
        df_result = normalizer.normalize_stock(df)
        name = f"STOCK-OUTPUT-{normalizer}.xlsx"
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        df_result.to_excel(path.joinpath(OUTPUT_PATH, name), index=False)
        


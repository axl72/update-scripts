from core.normalizer import Normalizer
from core.reader import Reader
from pathlib import Path
import pandas as pd

class Updater():
    def consolidate(self, path: Path, normalizer:Normalizer) -> None:
        df_list = normalizer.read(path)
        df_list = [normalizer.normalize_sells(df) for df in df_list]
        result_df = pd.concat(df_list)
        name = f"OUTPUT-{normalizer}.xlsx"
        result_df.to_excel(name, index=False)



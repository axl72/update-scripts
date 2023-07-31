import pandas as pd
from pathlib import Path
from util.whateveryouchooser import Chooser
from util.xlsx_functions import get_stock, read_csv_oeschle_stock
from util.conexiones import IntekConnector
from core.stock_normalizers import oechsle_stock_normalizer


def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    chooser = Chooser()
    filename = Path(chooser.select_file())
    df = get_stock(filename, read_csv_oeschle_stock, oechsle_stock_normalizer, export=False)
    df.to_sql('stock_oechsle', engine, index=False, if_exists='append')
    print("uploaded data")   




if __name__ == "__main__":
    update()
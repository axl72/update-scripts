import pandas as pd
from pathlib import Path
from util.whateveryouchooser import Chooser
from util.xlsx_functions import get_stock, read_csv_tottus
from util.conexiones import IntekConnector
from core.stock_normalizers import tottus_stock_normalizer

def validar_path(path:Path):
    filenames = [len(file.name.split('.')[0]) for file in path.iterdir()]
    filtered_list = list(filter(lambda x: x!= 8, filenames))
    if len(filtered_list) > 0:
        print("Uno de los archivos no tiene el tamaño de nombre correcto")
        return False
    filtered_list = list(filter(lambda x: type(x) is int, filenames))
    if len(filtered_list) < len(filenames):
        print("Uno de los archivos no tiene un titulo numerico")
        return False
    return True

def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    chooser = Chooser()
    filename = Path(chooser.select_file())
    df = get_stock(filename, read_csv_tottus, tottus_stock_normalizer, export=False)
    df.to_sql('stock_tottus', engine, index=False, if_exists='append')
    print("uploaded data")   




if __name__ == "__main__":
    update()
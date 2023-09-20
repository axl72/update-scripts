import pandas as pd
from pathlib import Path
from util.whateveryouchooser import Chooser
from util.xlsx_functions import consolidate, read_csv_tottus
from util.conexiones import IntekConnector
from core.normalizers import tottus_normalizer

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
    directory = Path(chooser.select_directory())
    df = consolidate(directory, read_csv_tottus, tottus_normalizer, export=False)
    df.to_excel("C:\\Users\\abernabel\\Desktop\\Update\\output-ventas-tottus.xlsx", index=False)
    # df.to_sql('ventas_tottus', engine, index=False, if_exists='append')
    # print("data de ventas tottus cargada")   
    print("Consolidado de ventas Tottus generado")




if __name__ == "__main__":
    update()



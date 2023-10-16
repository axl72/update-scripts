import config
from pathlib import Path


from util.xlsx_functions import consolidate, read_csv
from core.normalizers import oeschle_normalizer
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector



def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    directory = Path(Chooser().select_directory())
    df = consolidate(directory, read_csv, oeschle_normalizer)
    df.to_sql('ventas_oechsle', engine, index=False, if_exists='append')
    print("Data de ventas de Oechsle cargada")

if __name__ == "__main__":
    update()



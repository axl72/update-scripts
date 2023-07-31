import config
from pathlib import Path


from util.xlsx_functions import consolidate, read_excel
from core.normalizers import ripley_normalizer
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector



def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    directory = Path(Chooser().select_directory())
    df = consolidate(directory, read_excel, ripley_normalizer)
    df.to_sql('ventas_ripley', engine, index=False, if_exists='append')
    print("uploaded data")

if __name__ == "__main__":
    update()
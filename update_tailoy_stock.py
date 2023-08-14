import config
from pathlib import Path
from util.xlsx_functions import consolidate, read_excel
from core.normalizers import tailoy_normalizer
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector

def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    directory = Path(Chooser().select_directory())
    print(f"Directorio seleccionado {directory}")
    df = consolidate(directory, read_excel, tailoy_normalizer)
    df.to_sql('stock_tailoy', engine, index=False, if_exists='append')
    print("uploaded data")

if __name__ == "__main__":
    update()
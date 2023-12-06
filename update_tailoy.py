import config
from pathlib import Path
from util.xlsx_functions import consolidate, read_excel
from core.normalizers import tailoy_normalizer
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector
import logging

def update():
    connector = IntekConnector()
    engine = connector.create_engine()

    selected_directory = Chooser().select_directory()
    if selected_directory == "":
        print("Ningun directorio seleccionado")
        return
    directory = Path(selected_directory)
    
    print(f"Directorio seleccionado {directory}")
    df = consolidate(directory, read_excel, tailoy_normalizer)
    df.to_excel("C:\\Users\\abernabel\\Desktop\\Update\\output-ventas-tailoy.xlsx", index=False)
    print("Data de ventas Tailoy generada")

if __name__ == "__main__":
    update()
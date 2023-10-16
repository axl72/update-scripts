import config
from pathlib import Path
import os
from util.xlsx_functions import consolidate
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector



def update(reader:None, normalizer:None, pathfile:Path, funcion,outputfilename:str='output.xlsx',connector:IntekConnector=None, tablename:None=str):

    df = funcion(pathfile, reader, normalizer)
    output_path = os.path.join(config.OUTPUT_PATH, outputfilename)
    df.to_excel(output_path, index=False)
    print(f"Archivo {output_path} generado")

    if connector != None:

        engine = connector.create_engine()
        df.to_sql(tablename, engine, index=False, if_exists='append')
        print("Data de ventas de Oechsle cargada")

if __name__ == "__main__":
    update()


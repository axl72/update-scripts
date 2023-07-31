import pandas as pd
from util.conexiones import IntekConnector
from util.whateveryouchooser import Chooser
from pathlib import Path


file = Path(Chooser().select_file())

# ventas_tottus = pd.read_excel(file.absolute(), sheet_name='ventas_tottus')
# cod_local = pd.read_excel(file.absolute(), sheet_name='cod_local')
sku_tottus = pd.read_excel(file.absolute(), sheet_name='update')
# print(cod_local.head())
engine = IntekConnector().create_engine()

sku_tottus.to_sql('sku_tottus', engine, if_exists='append', index=False)
# cod_local.to_sql('locales_tottus', engine, if_exists='append', index=False)
# ventas_tottus.to_sql('ventas_tottus', engine, if_exists='append', index=False)

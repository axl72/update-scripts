import config
from pathlib import Path
from util.xlsx_functions import get_stock, read_excel
from core.stock_normalizers import tailoy_stock_normalizer
from util.whateveryouchooser import Chooser
from util.conexiones import IntekConnector

def update():
    connector = IntekConnector()
    engine = connector.create_engine()
    selected_directory = Chooser().select_file()
    if selected_directory == "":
        return
    file = Path(selected_directory)
    print(f"Excel de stock seleccionado {file}")
    df = get_stock(file, read_excel, tailoy_stock_normalizer)
    print(df.columns)
    df.to_excel("C:\\Users\\abernabel\\Desktop\\Update\\output-stock-tailoy.xlsx", index=False)
    print("Stock Tai Loy generado con exito")

if __name__ == "__main__":
    update()
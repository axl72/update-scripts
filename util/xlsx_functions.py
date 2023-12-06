import pandas as pd
import pathlib
import os
import util.whateveryouchooser as wyc
import warnings

def read_excel(path):
    warnings.filterwarnings("ignore")
    print(f"Leyendo archivo {path}")
    df = pd.read_excel(path, header=None)
    warnings.filterwarnings("default") 
    return df

def read_csv(path):
    warnings.filterwarnings("ignore")
    print(f"Leyendo archivo {path}")
    return pd.read_csv(path, sep=',', encoding='latin1')
    warnings.filterwarnings("default") 

def read_csv_saga_falabella(path):
    return pd.read_csv(path, sep='|', encoding='latin1')

def read_csv_oeschle_stock(path:str):
    warnings.filterwarnings("ignore")
    print(f"Leyendo archivo {path}")
    df = pd.read_csv(path, sep=',', encoding='latin1')
    df['fecha'] = str(path).split('\\')[-1].split('.')[0]
    return df

def read_xlsx_tailoy_stock(path:str):
    df = pd.read_excel(path, header=None)
    df = df.drop(range(7))
    df.columns = df.iloc[0]
    df = df[1:]
    df['FECHA'] = str(path).split('\\')[-1].split('.')[0]
    return df

def read_csv_tottus(path:str):
    warnings.filterwarnings("ignore")
    print(f"Leyendo archivo {path}")
    df =  pd.read_csv(path, sep=',', encoding='latin1')
    df['fecha'] = str(path).split('\\')[-1].split('.')[0]
    warnings.filterwarnings("default") 
    return df

def get_stock(filename, read_file=pd.read_excel, normalizer=None, export=False):
    df = read_file(filename)
    print("Files read successfully")
    if normalizer:
        df = normalizer(df)
    if export:
        chooser = wyc.Chooser()
        directory = pathlib.Path(chooser.select_directory())
        name = str(pd.to_datetime('now'))
        name = name.replace(':', '')
        name =  name + '.xlsx'
        path = os.path.join(directory, name)
        df.to_excel(path, index=False, engine='openpyxl')
    return df

def consolidate(files:pathlib.Path, read_file=read_excel, normalizer=None, export=False):
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
    dataframe_list = [read_file(path) for path in files.iterdir()]
    print("Files read successfully")
    if normalizer:
        dataframe_list = [normalizer(df) for df in dataframe_list]
    merge_df = pd.concat(dataframe_list)
    merge_df.reset_index(drop=True, inplace=True)
    if export:
        chooser = wyc.Chooser()
        directory = pathlib.Path(chooser.select_directory())
        name = str(pd.to_datetime('now'))
        name = name.replace(':', '')
        name =  name + '.xlsx'
        path = os.path.join(directory, name)
        merge_df.to_excel(path, index=False, engine='openpyxl')
    print("completed consolidation")
    return merge_df
    
if __name__ == "__main__":
    file_to_update = pathlib.Path(wyc.Chooser().select_directory())
    consolidate(file_to_update, export=True)
    
    
import pandas as pd
import warnings
import datetime
from core.normalizer import Normalizer
from pathlib import Path
from pandas import DataFrame
from datetime import datetime, timedelta
from pandas._libs.tslibs.timestamps import Timestamp
from zipfile import ZipFile
from io import BytesIO
import numpy as np

class SagaNormalizer(Normalizer):
    def read(self, pathdir:Path):
        pass
    def normalize_sells(self, df:DataFrame):
        pass

    def normalize_stock(self, df:DataFrame):
        pass

class EstilosNormalizer(Normalizer):
    def read(self, pathdir:Path):
        df_list = []
        for path in pathdir.iterdir():

            df = pd.read_excel(path, skiprows=4, usecols=range(22))
            df_list.append(df)
        return df_list
    
    def normalize_sells(self, df:DataFrame):
        columnas_a_eliminar = [1, 2, 4, 5, 6, 8, 9, 11, 12, 14, 15, 16, 18, 19, 21]

        df = df.drop(df.columns[columnas_a_eliminar], axis=1)

        df['Division'] = df['Division'].str.upper()
        df = df[~df['Division'].str.contains('TOTAL', case=False, na=False)]
        df['Division'] = df['Division'].ffill()
        
        df['Fecha'] = df['Fecha'].astype(str)
        df['Fecha'] = df['Fecha'].str.upper()
        df = df[~df['Fecha'].str.contains('TOTAL')]
        df['Fecha'] = df['Fecha'].replace('NAN', np.nan)
        df['Fecha'] = df['Fecha'].ffill()
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        df['Tienda'] = df['Tienda'].str.upper()
        df = df[~df['Tienda'].str.contains('TOTAL', case=False, na=False)]
        df['Tienda'] = df['Tienda'].ffill()
        
        df['Sku'] = df['Sku'].astype(int).astype(str).apply(lambda x: "00" + x)
        df['Sku'] = df['Sku'].ffill()
        
        df = df.drop(['Division'], axis=1)
        return df
    
    def normalize_stock(self, df:DataFrame):
        pass
    
    def __str__(self):
        return "ESTILOS"

class OechsleNormalizer(Normalizer):
    def read(self, pathdir:Path):
        df_list = []
        for path in pathdir.iterdir():
            with ZipFile(path, 'r') as zip_file:
                nombre_archivo = zip_file.namelist()[0]
                contenido_csv = BytesIO(zip_file.read(nombre_archivo))
                df = pd.read_csv(contenido_csv, sep=',', encoding='latin1') 
                df_list.append(df)
        return df_list

    def normalize_sells(self, df:DataFrame):
        df = df.rename(columns={'PERIODO': 'FECHA'})
        df['FECHA'] = pd.to_datetime(df['FECHA'])
        df = df[df['VTA_PERIODO_UNID'] != 0]
        df['COSTO_UNITARIO'] = None
        df['COSTO_TOTAL'] = None
        return df

    def __str__(self):
        return 'OECHSLE'
    
    def normalize_stock(self, df:DataFrame):
        pass

class RipleyNormalizer(Normalizer):
    def read(self, pathdir:Path):
        return  [pd.read_excel(path, header=None) for path in pathdir.iterdir() if str(path.absolute()).endswith('.xlsx')]

    def normalize_sells(self, df:DataFrame):
        """Funcion que sirve para normalizar un dataframe de Ripley. Normalizar implica que el archivo descargado del B2B de ripley quede en forma normal para el análisis."""
        target_columns = ["Fecha","Codigo Sucursal", "Codigo Modelo", "Venta S/.", "Venta Unid.", "Costo Venta Actual"]
        extrae = lambda x, y: df.iloc[x, y]
        lista_campos = {extrae(i,0) if i == 0 else extrae(i, 0):extrae(i, 1) for i in range(5)}
        temp = df.drop(index=range(8))
        # Establecer la primera fila como columnas
        temp.columns = temp.iloc[0]
        temp = temp[1:]

        temp.reset_index(drop=True, inplace=True)

        for campo, valor in lista_campos.items():
            temp[campo] = valor    

        temp["Fecha"] = pd.to_datetime(temp["Fecha"], format="%d-%m-%Y")
        temp = temp[temp['Venta Unid.'] != 0]

        nuevas_columnas = ["fecha", "codigo_sucursal", "sku", "venta_soles", "venta_unidades", "costo_venta"]
        renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
        temp.rename(columns=renombre, inplace=True)
        # Corregir esto, puede ser algo como return temp[nuevas_columas] if complete else temp
        return temp[nuevas_columnas]
    
    def __str__(self):
        return "RIPLEY"
    
    def normalize_stock(self, df:DataFrame):
        pass

class TaiLoyNormalizer(Normalizer):
    def obtenerSemanaComercial(self, fecha_inicio:Timestamp):

        # Definir el rango de fechas
        inicio_rango = fecha_inicio

        # Encontrar el primer lunes del año
        primer_lunes = datetime(inicio_rango.year, 1, 1)
        while primer_lunes.weekday() != 0:  # 0 representa lunes en Python
            primer_lunes += timedelta(days=1)

        # Determinar el número de semanas transcurridas desde el primer lunes del año hasta la fecha de inicio
        numero_semanas = ((inicio_rango - primer_lunes).days // 7) + 1
        return numero_semanas


    def read(self, pathdir:Path):
        df_list = []
        for path in pathdir.iterdir():
            df =  pd.read_excel(path)
            df_list.append(df)
        return df_list

    def normalize_sells(self, df:DataFrame):
        result = df.iloc[6:]
        result.columns = result.iloc[0]
        result.reset_index(drop=True, inplace=True)
        result = result[1:]
        columnas_a_eliminar = ['GRUPO', 'CATEGORÍA', 'UNIDAD BASE', 'ESTADO', 'TOTAL VENTAS']
        
        result = result.drop(columnas_a_eliminar, axis=1)
        result = pd.melt(result, id_vars=['FECHA INICIAL', 'FECHA FINAL', 'CÓDIGO AS400', 'CÓDIGO SAP', 'DESCRIPCIÓN'], var_name='TIENDA', value_name='UNIDADES', col_level=0)
        result = result[result['UNIDADES'] != 0]
        result.reset_index(drop=True, inplace=True)
        result['FECHA INICIAL'] = result['FECHA INICIAL'].str.strip()
        result['FECHA FINAL'] = result['FECHA FINAL'].str.strip()
        result['FECHA INICIAL'] = pd.to_datetime(result['FECHA INICIAL'], format='%Y%m%d')
        result['FECHA FINAL'] = pd.to_datetime(result['FECHA FINAL'], format='%Y%m%d')  


        result['CÓDIGO AS400'] = result['CÓDIGO AS400'].apply(lambda x: int(x))
        result['CÓDIGO SAP'] = result['CÓDIGO SAP'].apply(lambda x: int(x))
        result['SEMANA'] = self.obtenerSemanaComercial(result['FECHA INICIAL'].iloc[0])
        
        return result
    
    def __str__(self):
        return "TAI LOY"
    
    def normalize_stock(self, df:DataFrame):
        pass

class TottusNormalizer(Normalizer):
    def read(self, pathdir:Path) -> list[DataFrame]:
        df_list = []
        for path in pathdir.iterdir():
            df =  pd.read_csv(path, sep=',', encoding='latin1')
            df['fecha'] = str(path).split('\\')[-1].split('.')[0]
            df_list.append(df)
        return df_list

    def normalize_sells(self, df:DataFrame) -> DataFrame:
        target_columns = ['fecha', 'Upc',' Sku', 'Estilo', 'Descripción del Producto', 'Marca', 'Modelo', 'Estado', 'Umb', 'Surtido', 'N° Local', 'Nombre Local','Venta(u)', 'Venta al publico(C/IVA)', 'Venta en Costo(S/IVA)']
        df = df[target_columns]
        nuevas_columnas = ['fecha', 'upc','sku', 'estilo', 'descripcion_producto', 'marca', 'modelo', 'estado', 'umb','surtido', 'cod_local', 'local', 'venta_unidades', 'venta_publico_igv', 'venta_costo']
        renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
        df.rename(columns=renombre, inplace=True)
        df['fecha'] = pd.to_datetime(df['fecha'], format="%Y%m%d")
        df = df[df["venta_unidades"] != 0]
        return df
    
    def normalize_stock(self, df:DataFrame) -> DataFrame:
        pass
    
    def __str__(self):
        return 'TOTTUS'

    def normalize_stock(df:DataFrame):
        pass

def ripley_normalizer(df:pd.DataFrame):
    """Funcion que sirve para normalizar un dataframe de Ripley. Normalizar implica que el archivo descargado del B2B de ripley quede en forma normal para el análisis."""
    target_columns = ["Fecha","Codigo Sucursal", "Codigo Modelo", "Venta S/.", "Venta Unid.", "Costo Venta Actual"]
    extrae = lambda x, y: df.iloc[x, y]
    lista_campos = {extrae(i,0) if i == 0 else extrae(i, 0):extrae(i, 1) for i in range(5)}
    temp = df.drop(index=range(8))
    # Establecer la primera fila como columnas
    temp.columns = temp.iloc[0]
    temp = temp[1:]

    temp.reset_index(drop=True, inplace=True)

    for campo, valor in lista_campos.items():
        temp[campo] = valor    

    temp["Fecha"] = pd.to_datetime(temp["Fecha"], format="%d-%m-%Y")
    temp = temp[temp['Venta Unid.'] != 0]

    nuevas_columnas = ["fecha", "codigo_sucursal", "sku", "venta_soles", "venta_unidades", "costo_venta"]
    renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
    temp.rename(columns=renombre, inplace=True)
    # Corregir esto, puede ser algo como return temp[nuevas_columas] if complete else temp
    return temp[nuevas_columnas]

def oeschle_normalizer(df:pd.DataFrame):
    target_columns = ["PERIODO", "COD_OECHSLE", "COD_LOCAL", "VTA_PERIODO_S", "VTA_PERIODO_UNID"]
    df = df[target_columns]
    df = df[df["VTA_PERIODO_UNID"] != 0]
    df["PERIODO"] = pd.to_datetime(df["PERIODO"], format="%Y-%m-%d")
    nuevas_columnas = ["fecha", "sku", "cod_local", "venta_soles", "venta_unidades"]
    renombre = {clave:valor for clave, valor in zip(target_columns, nuevas_columnas)}
    df.rename(columns=renombre, inplace=True)
    return df

def tottus_normalizer(df:pd.DataFrame):
    target_columns = ['fecha', 'Upc',' Sku', 'Estilo', 'Descripción del Producto', 'Marca', 'Modelo', 'Estado', 'Umb', 'Surtido', 'N° Local', 'Nombre Local','Venta(u)', 'Venta al publico(C/IVA)', 'Venta en Costo(S/IVA)']
    df = df[target_columns]
    nuevas_columnas = ['fecha', 'upc','sku', 'estilo', 'descripcion_producto', 'marca', 'modelo', 'estado', 'umb','surtido', 'cod_local', 'local', 'venta_unidades', 'venta_publico_igv', 'venta_costo']
    renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
    df.rename(columns=renombre, inplace=True)
    df['fecha'] = pd.to_datetime(df['fecha'], format="%Y%m%d")
    df = df[df["venta_unidades"] != 0]
    return df


def saga_normalizer(df:pd.DataFrame):
    def normalizar_fecha(date:str) -> str:
        dia_semana, fecha = date.split('_')
        dia, mes = fecha.split('-')
        año_actual = datetime.now().year
        return f"{dia}/{mes}/{año_actual}" 
    df = df.iloc[:, :-6]
    target_columns = ["UPC", "SKU", "ESTILO", "DESCRIPCION_LARGA", "SUBCLASE", "DESC_SUBCLASE", "MARCA", "MODELO", "NRO_LOCAL", "LOCAL"]
    df = df.melt(id_vars=target_columns, var_name='FECHA', value_name='UNIDADES')
    df["FECHA"] = df["FECHA"].apply(normalizar_fecha)
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y")
    df = df[df["UNIDADES"] != 0]


    
if __name__ == "__main__":
    pass
import pandas as pd
import warnings
import datetime

def tailoy_normalizer(df:pd.DataFrame):
    """Funcion que sirve para normalizar un dataframe de Tai Loy"""
    target_columns = ["FECHA INICIAL", "FECHA FINAL", "GRUPO", "CATEGORÍA", "CÓDIGO SAP", "CÓDIGO AS400", "DESCRIPCIÓN", "UNIDAD BASE", "ESTADO"]
    df = df.drop(index=range(7))
    df.columns = df.iloc[0]
    df = df[1:]
    df.pop('TOTAL VENTAS')
    df.reset_index()
    df['FECHA INICIAL'] = pd.to_datetime(df['FECHA INICIAL'], format='%Y%m%d  ')
    df['FECHA FINAL'] = pd.to_datetime(df['FECHA FINAL'], format='%Y%m%d  ')
    df['CÓDIGO SAP'] = df['CÓDIGO SAP'].astype(float)
    df['CÓDIGO AS400'] = df['CÓDIGO AS400'].astype(float)
    df = df.melt(id_vars=target_columns, var_name='LOCAL', value_name='UNIDADES')
    df = df[df['UNIDADES'] != 0]
    target_columns = [*target_columns, "LOCAL", "UNIDADES"]
    # new_columns = ["fecha_inicial", "fecha_final", "codigo_sap", "codigo_as400", "descripcion", "local", "unidades"]
    # renombre = {clave: valor for clave, valor in zip(target_columns, new_columns)}
    # df.rename(columns=renombre, inplace=True)
    return df



def ripley_normalizer(df:pd.DataFrame):
    """Funcion que sirve para normalizar un dataframe de Ripley. Normalizar implica que el archivo descargado del B2B de ripley quede en forma normal para el análisis."""
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
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
    df = pd.read_excel('C:\\Users\\abernabel\\Desktop\\BASE_DATOS\\DATA\\Tai Loy\\31.xlsx')
    df = tailoy_normalizer(df)
    df.to_excel('output.xlsx', index=False)
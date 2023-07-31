import pandas as pd


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
    target_columns = ['fecha',' Sku', 'Surtido', 'N° Local', 'Venta(u)', 'Venta al publico(C/IVA)', 'Venta en Costo(S/IVA)']
    df = df[target_columns]
    nuevas_columnas = ['fecha', 'sku', 'surtido', 'cod_local', 'venta_unidades', 'venta_publico_igv', 'venta_costo']
    renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
    df.rename(columns=renombre, inplace=True)
    df['fecha'] = pd.to_datetime(df['fecha'], format="%Y%m%d")
    df = df[df["venta_unidades"] != 0]
    return df


def saga_normalizer(df:pd.DataFrame):
    pass

def tailoy_normalizer(df:pd.DataFrame):
    pass


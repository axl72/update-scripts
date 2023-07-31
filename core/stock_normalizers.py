import pandas as pd

def oechsle_stock_normalizer(df:pd.DataFrame) -> pd.DataFrame:
    target_columns = ["fecha", "COD_OECHSLE", "COD_LOCAL", "STOCK(U)", "TRANSITO(U)", "STOCKNODISP.(U)", "ASIGNADO(U)"]
    df = df[target_columns]
    nuevas_columnas = ["fecha", "sku", "cod_local", "stock", "transito", "stock_no_disponible", "asignado"]
    renombre = {clave:valor for clave, valor in zip(target_columns, nuevas_columnas)}
    df.rename(columns=renombre, inplace=True)

    df["stock"] = df["stock"].apply(lambda x: x if x > 0 else 0)
    df["transito"] = df["transito"].apply(lambda x: x if x > 0 else 0)
    df["stock_no_disponible"] = df["stock_no_disponible"].apply(lambda x: x if x > 0 else 0)
    df["asignado"] = df["asignado"].apply(lambda x: x if x > 0 else 0)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y%m%d")
    df["stock_total"] = df["stock"] + df["transito"] + df["stock_no_disponible"] + df["asignado"]
    return df

def tottus_stock_normalizer(df:pd.DataFrame) -> pd.DataFrame:
    target_columns = ["fecha"," Sku", "N° Local", "Inventario en Locales(U)", "Tránsito(U)", "Inv a Costo(S/IVA)"]
    df = df[target_columns]
    nuevas_columnas = ["fecha","sku", "cod_local", "stock_locales", "stock_transito", "stock_costo"]
    renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
    df.rename(columns=renombre, inplace=True)

    df["stock_locales"] = df["stock_locales"].apply(lambda x: x if x > 0 else 0)
    df["stock_transito"] = df["stock_transito"].apply(lambda x: x if x > 0 else 0)
    df["stock_costo"] = df["stock_costo"].apply(lambda x: x if x > 0 else 0)
    df["stock_total"] = df["stock_locales"] + df["stock_transito"]
    df.reset_index(drop=True, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y%m%d")
    return df

def ripley_stock_normalizer(df:pd.DataFrame) -> pd.DataFrame:
    """Funcion que sirve para normalizar un dataframe de Ripley. Normalizar implica que el archivo descargado del B2B de ripley quede en forma normal para el análisis."""

    target_columns = ["Fecha","Codigo Sucursal", "Codigo Modelo", "Stock S/.", "Stock Und."]
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

    nuevas_columnas = ["fecha", "codigo_sucursal", "sku", "stock_soles", "stock_unidades"]
    renombre = {clave: valor for clave, valor in zip(target_columns, nuevas_columnas)}
    temp.rename(columns=renombre, inplace=True)

    return temp[nuevas_columnas]

from sqlalchemy import create_engine

class IntekConnector:
    def __init__(self):
        self.usuario = 'intekcomercial'
        self.contraseña = 'Ve4c5i-2Z3?J'
        self.servidor = 'den1.mssql7.gear.host'
        self.base_datos = 'intekcomercial' 
        self.cadena_conexion = f"mssql+pyodbc://{self.usuario}:{self.contraseña}@{self.servidor}/{self.base_datos}?driver=ODBC+Driver+17+for+SQL+Server"
    
    def create_engine(self):
        engine = create_engine(self.cadena_conexion)
        return engine
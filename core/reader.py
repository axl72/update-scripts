from abc import ABC, abstractclassmethod
from pathlib import Path
from pandas import DataFrame

class Reader(ABC):
    @abstractclassmethod
    def read(self, path:Path) -> DataFrame:
        pass
from abc import abstractclassmethod, ABC
from pandas import DataFrame
from pathlib import Path

class Normalizer(ABC):

    @abstractclassmethod
    def normalize_sells(self, df:DataFrame) -> DataFrame:
        pass

    @abstractclassmethod
    def read(self, pathdir:Path) -> list[DataFrame]:
        pass

    @abstractclassmethod
    def normalize_stock(self, df:DataFrame) -> DataFrame:
        pass


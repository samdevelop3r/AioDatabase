import aiomysql

from .table import Table
from .sql_request import SQLRequests


class AioDatabase:
    _pool: aiomysql.Pool = None
    _requests: SQLRequests = SQLRequests()
    _data_types = {
        "str": " TEXT ",
        "int": " INTEGER ",
        "bool": " BOOLEAN "
    }

    @classmethod
    def _table_parameter_converter(cls, parameter: str, is_key: bool = False) -> str:
        sorted_parameter = parameter.split(" ")[0] + cls._data_types[parameter.split(" ")[1]]
        if is_key is True:
            sorted_parameter += " PRIMARY KEY AUTOINCREMENT"
            return sorted_parameter
        return sorted_parameter

    @classmethod
    async def create_table(cls, name: str, primary_key: str | int = None, **kwargs) -> None:
        request_query = f"CREATE TABLE IF NOT EXISTS {name} ("
        if primary_key:
            request_query += cls._table_parameter_converter(parameter=primary_key, is_key=True) + ", "
        for key, value in kwargs.items():
            request_query += cls._table_parameter_converter(parameter=f"{key} {value}") + ", "
        request_query = request_query[:-2]
        request_query += ")"
        await cls._requests.send(request_query)

    @classmethod
    def table(cls, name: str):
        return Table(name=name, requests=cls._requests)

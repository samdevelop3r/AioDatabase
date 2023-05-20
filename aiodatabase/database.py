from .table import Table
from .sql_request import SQLRequests
from .configs.converters import Url


class AioDatabase:
    _requests: SQLRequests = SQLRequests()
    _data_types = {
        "str": " TEXT ",
        "int": " INTEGER ",
        "bool": " BOOLEAN "
    }

    def __init__(self, url: str):
        self._converted_url = Url.convert(url)

    def _table_parameter_converter(self, parameter: str, is_key: bool = False) -> str:
        sorted_parameter = parameter.split(" ")[0] + self._data_types[parameter.split(" ")[1]]
        if is_key is True:
            sorted_parameter += " PRIMARY KEY AUTOINCREMENT"
            return sorted_parameter
        return sorted_parameter

    async def create_table(self, name: str, primary_key: str | int = None, **kwargs) -> None:
        request_query = f"CREATE TABLE IF NOT EXISTS {name} ("
        if primary_key:
            request_query += self._table_parameter_converter(parameter=primary_key, is_key=True) + ", "
        for key, value in kwargs.items():
            request_query += self._table_parameter_converter(parameter=f"{key} {value}") + ", "
        request_query = request_query[:-2]
        request_query += ")"
        await self._requests.send(converted_url=self._converted_url, query=request_query)

    def table(self, name: str):
        return Table(name=name, requests=self._requests, converted_url=self._converted_url)
    

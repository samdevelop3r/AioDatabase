from typing import List

from .sql_request import SQLRequests
from .configs.models import ConvertedUrl


class Table:
    def __init__(self, name: str, requests: SQLRequests, converted_url: ConvertedUrl):
        self._name = name
        self._requests: SQLRequests = requests
        self._converted_url = converted_url

    @classmethod
    def _query_parameters_converter(cls, raw_queries: str | List[str]):
        def sort_queries(raw_query: str) -> int | str | bool:
            if isinstance(raw_query, str):
                return f"'{raw_query}'"
            else:
                return raw_query

        if isinstance(raw_queries, list):
            new_queries = []
            for query in raw_queries:
                new_queries.append(sort_queries(query))
        elif isinstance(raw_queries, str):
            return sort_queries(raw_queries)
        return raw_queries

    async def insert_value(self, **kwargs):
        request_query = f"INSERT INTO {self._name} ("
        for key in kwargs.keys():
            request_query += f"{str(key)}, "
        request_query = request_query[:-2] + ") VALUES ("
        for value in kwargs.values():
            request_query += f"{self._query_parameters_converter(value)}, "
        request_query = request_query[:-2] + ")"
        await self._requests.send(converted_url=self._converted_url, query=request_query)

    async def update_value(self, values: List[dict], **kwargs):
        request_query = f"UPDATE {self._name} SET "
        for row in values:
            for key, value in row.items():
                request_query += f"{key} = {self._query_parameters_converter(value)}, "
        request_query = request_query[:-2] + " "
        if kwargs:
            request_query += "WHERE "
            for key, value in kwargs.items():
                request_query += f"{key} = {self._query_parameters_converter(value)} AND "
        request_query = request_query[:-5]
        print(request_query)
        await self._requests.send(converted_url=self._converted_url, query=request_query)

    async def delete_value(self, **kwargs):
        request_query = f"DELETE FROM {self._name} "
        if kwargs:
            request_query += "WHERE "
            for key, value in kwargs.items():
                request_query += f"{key} = {self._query_parameters_converter(value)} AND "
            request_query = request_query[:-5]
        await self._requests.send(converted_url=self._converted_url, query=request_query)

    async def select_values(self, values: str | List[str], order_by: str = None, **kwargs):
        request_query = f"SELECT "
        if isinstance(values, str) and values == "all":
            request_query += "*"
        else:
            request_query += ", ".join(values)
        request_query += f" FROM {self._name}"
        if kwargs:
            request_query += " WHERE "
            for key, value in kwargs.items():
                request_query += f"{key} = {self._query_parameters_converter(value)} AND "
            request_query = request_query[:-5]
        if order_by:
            request_query += f" ORDER BY {order_by} DESC"
        return await self._requests.send(converted_url=self._converted_url, query=request_query)

import asyncio
import aiomysql
import ujson


class SQLRequests:
    with open("dbconfig.json", "r", encoding="utf-8") as _file:
        _database_data = ujson.load(_file)

    @classmethod
    async def send(cls, query: str) -> None | tuple:
        pool = await aiomysql.create_pool(
            host=cls._database_data["hostname"],
            port=cls._database_data["port"],
            user=cls._database_data["user"],
            password=cls._database_data["password"],
            db=cls._database_data["db"], loop=asyncio.get_event_loop()
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                await conn.commit()
                pool.close()

                return (await cur.fetchall())

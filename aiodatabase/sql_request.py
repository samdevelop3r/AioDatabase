import asyncio
import aiomysql

from .configs.models import ConvertedUrl


class SQLRequests:
    @classmethod
    async def send(cls, converted_url: ConvertedUrl, query: str) -> None | tuple:
        pool = await aiomysql.create_pool(
            host=converted_url.hostname,
            port=converted_url.port,
            user=converted_url.user,
            password=converted_url.password,
            db=converted_url.db, loop=asyncio.get_event_loop()
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                await conn.commit()
                pool.close()

                return (await cur.fetchall())

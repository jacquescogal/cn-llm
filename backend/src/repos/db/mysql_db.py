import asyncio
import aiomysql
import os
from src.config.configuration import Config

class Database:
    instance = None
    def __init__(self):
        self.pool = None
        self.config = Config()

    async def _create_pool(self):
        self.pool = await aiomysql.create_pool(
            host=self.config.db_host,
            port=int(self.config.db_port),
            user=self.config.db_user,
            password=self.config.db_password,
            db=self.config.db_name,
            charset='utf8mb4', # utf8mb4 is the default for MySQL
            autocommit=False # transactions are default
        )

    async def get_conn(self) -> aiomysql.Connection:
        if self.pool is None:
            await self._create_pool()
        return await self.pool.acquire()
    
    async def release_connection(self, conn):
        self.pool.release(conn)

    async def close_pool(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
import asyncpg

DATABASE_URL = "postgresql://postgres:senha@localhost/biblioteca"

async def conectar():
    return await asyncpg.connect(DATABASE_URL)
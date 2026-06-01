import asyncpg

async def conectar():
    print("Conectando no banco...")
    return await asyncpg.connect(
        user="postgres",
        password="082008",
        database="Biblioteca",
        host="localhost",
        port=5432
    )
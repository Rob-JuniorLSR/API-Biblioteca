from fastapi import FastAPI, HTTPException
from database import conectar
from model import Item

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await conectar()


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


# CREATE
@app.post("/items")
async def criar(item: Item):
    result = await app.state.db.fetchrow(
        """
        INSERT INTO livros (titulo, autor, genero, ano, quantidade)
        VALUES ($1,$2,$3,$4,$5)
        RETURNING *
        """,
        item.titulo,
        item.autor,
        item.genero,
        item.ano,
        item.quantidade
    )
    return dict(result)


# READ ALL
@app.get("/items")
async def listar():
    result = await app.state.db.fetch("SELECT * FROM livros")
    return [dict(r) for r in result]


# READ BY ID
@app.get("/items/{id}")
async def buscar(id: int):
    result = await app.state.db.fetchrow(
        "SELECT * FROM livros WHERE id=$1",
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    return dict(result)


# UPDATE
@app.put("/items/{id}")
async def atualizar(id: int, item: Item):
    result = await app.state.db.fetchrow(
        """
        UPDATE livros
        SET titulo=$1, autor=$2, genero=$3, ano=$4, quantidade=$5
        WHERE id=$6
        RETURNING *
        """,
        item.titulo,
        item.autor,
        item.genero,
        item.ano,
        item.quantidade,
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    return dict(result)


# DELETE
@app.delete("/items/{id}")
async def deletar(id: int):
    result = await app.state.db.fetchrow(
        "DELETE FROM livros WHERE id=$1 RETURNING *",
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    return {"message": "Deletado com sucesso"}
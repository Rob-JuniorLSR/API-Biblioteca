from fastapi import FastAPI, HTTPException
from database import conectar
from models import Livro

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await conectar()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


# CREATE
@app.post("/items")
async def criar_livro(livro: Livro):
    query = """
    INSERT INTO livros
    (titulo, autor, genero, ano_publicacao, quantidade)
    VALUES ($1,$2,$3,$4,$5)
    RETURNING *
    """

    resultado = await app.state.db.fetchrow(
        query,
        livro.titulo,
        livro.autor,
        livro.genero,
        livro.ano_publicacao,
        livro.quantidade
    )

    return dict(resultado)


# READ LISTA
@app.get("/items")
async def listar_livros():
    resultado = await app.state.db.fetch(
        "SELECT * FROM livros"
    )

    return [dict(r) for r in resultado]


# READ ÚNICO
@app.get("/items/{id}")
async def buscar_livro(id: int):
    resultado = await app.state.db.fetchrow(
        "SELECT * FROM livros WHERE id=$1",
        id
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return dict(resultado)


# UPDATE
@app.put("/items/{id}")
async def atualizar_livro(id: int, livro: Livro):

    resultado = await app.state.db.fetchrow(
        """
        UPDATE livros
        SET titulo=$1,
            autor=$2,
            genero=$3,
            ano_publicacao=$4,
            quantidade=$5
        WHERE id=$6
        RETURNING *
        """,
        livro.titulo,
        livro.autor,
        livro.genero,
        livro.ano_publicacao,
        livro.quantidade,
        id
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return dict(resultado)


# DELETE
@app.delete("/items/{id}")
async def deletar_livro(id: int):

    resultado = await app.state.db.fetchrow(
        "DELETE FROM livros WHERE id=$1 RETURNING *",
        id
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return {"mensagem": "Livro removido com sucesso"}
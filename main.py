from fastapi import FastAPI, HTTPException
from database import conectar
from model import Livro

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

    resultado = await app.state.db.fetchrow(
        """
        INSERT INTO livros
        (titulo, genero, ano_publicacao, quantidade, autor_id)
        VALUES ($1,$2,$3,$4,$5)
        RETURNING *
        """,
        livro.titulo,
        livro.genero,
        livro.ano_publicacao,
        livro.quantidade,
        livro.autor_id
    )

    return dict(resultado)


# READ LISTA
@app.get("/items")
async def listar_livros():

    resultado = await app.state.db.fetch(
        """
        SELECT
            livros.id,
            livros.titulo,
            autores.nome AS autor,
            livros.genero,
            livros.ano_publicacao,
            livros.quantidade
        FROM livros
        JOIN autores
        ON livros.autor_id = autores.id
        ORDER BY livros.id
        """
    )

    return [dict(r) for r in resultado]


# READ ÚNICO
@app.get("/items/{id}")
async def buscar_livro(id: int):

    resultado = await app.state.db.fetchrow(
        """
        SELECT
            livros.id,
            livros.titulo,
            autores.nome AS autor,
            livros.genero,
            livros.ano_publicacao,
            livros.quantidade
        FROM livros
        JOIN autores
        ON livros.autor_id = autores.id
        WHERE livros.id = $1
        """,
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
        SET
            titulo=$1,
            genero=$2,
            ano_publicacao=$3,
            quantidade=$4,
            autor_id=$5
        WHERE id=$6
        RETURNING *
        """,
        livro.titulo,
        livro.genero,
        livro.ano_publicacao,
        livro.quantidade,
        livro.autor_id,
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
        """
        DELETE FROM livros
        WHERE id=$1
        RETURNING *
        """,
        id
    )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return {"mensagem": "Livro removido com sucesso"}

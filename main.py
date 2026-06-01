import asyncpg
from fastapi import FastAPI, HTTPException
from model import livro
from model import autores

app = FastAPI()

async def conectar():
    print("Conectando no banco...")
    return await asyncpg.connect(
        user="postgres",
        password="082008",
        database="Biblioteca",
        host="localhost",
        port=5432
    )

# CREATE
@app.post("/items")
async def criar(livro: livro):

    conn = await conectar()
    autor = await conn.fetchrow(
        """
        INSERT INTO autores(nome)
        VALUES($1)
        RETURNING id, nome
        """, 
        livro.autor
    )

    livro = await conn.fetchrow(
        """
        INSERT INTO livros (titulo, autor_id, genero, ano_publicacao, quantidade)
        VALUES ($1,$2,$3,$4,$5)
        RETURNING *
        """,
        
        livro.titulo,
        autor["id"],
        livro.genero,
        livro.ano,
        livro.quantidade
    )

    conn.close()
    return dict(livro)



# READ ALL
@app.get("/items")
async def listar():

    conn = await conectar()

    result = await conn.fetch("SELECT * FROM livros")

    conn.close()

    return [dict(r) for r in result]


# READ BY ID
@app.get("/items/{id}")
async def buscar(id: int):

    conn = await conectar()

    result = await conn.fetchrow(
        "SELECT * FROM livros WHERE id=$1",
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    conn.close()

    return dict(result)
    

# UPDATE
@app.put("/items/{id}")
async def atualizar_livros(id: int, livro: livro):
    conn = await conectar()
    result = await conn.fetchrow(
        """
        UPDATE livros
        SET titulo=$1, autor=$2, genero=$3, ano=$4, quantidade=$5
        WHERE id=$6
        RETURNING *
        """,
        livro.titulo,
        livro.genero,
        livro.ano,
        livro.quantidade,
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    conn.close()

    return dict(result)


# DELETE
@app.delete("/items/{id}")
async def deletar(id: int):
    conn = await conectar()
    result = await conn.fetchrow(
        "DELETE FROM livros WHERE id=$1 RETURNING *",
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")
    
    conn.close()

    return {"message": "Deletado com sucesso"}

#AUTORES

#CREATE
@app.post("/autores")
async def criar(autor: autores):

    conn = await conectar()
    autor = await conn.fetchrow(
        """
        INSERT INTO autores(nome)
        VALUES($1)
        RETURNING id, nome
        """, 
        autor.autor
    )

    conn.close()
    return dict(livro)

#READ
@app.get("/listar_autores")
async def listar():

    conn = await conectar()

    result = await conn.fetch("SELECT * FROM autores")

    conn.close()

    return [dict(r) for r in result]

#UPDATE
@app.put("/update_autores/{id}")
async def atualizar_autores(id: int, autor: autores):
    conn = await conectar()
    result = await conn.fetchrow(
        """
        UPDATE autores
        autor=$1,
        WHERE id=$1
        RETURNING *
        """,
        autor.autor,
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")

    conn.close()

    return dict(result)

#DELETE
@app.delete("/Deletar_autores/{id}")
async def deletar_autores(id: int):
    conn = await conectar()
    result = await conn.fetchrow(
        "DELETE FROM autores WHERE id=$1 RETURNING *",
        id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Não encontrado")
    
    conn.close()

    return {"message": "Deletado com sucesso"}
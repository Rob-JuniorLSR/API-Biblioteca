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
@app.post("/Criar_livros")
async def criar_livros(livro: livro):

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
@app.get("/Listar_livros")
async def listar_livros():

    conn = await conectar()

    result = await conn.fetch("SELECT * FROM livros")

    conn.close()

    return [dict(r) for r in result]


# READ BY ID
@app.get("/Buscar_livros/{id}")
async def buscar_livros(id: int):

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
@app.put("/Atualizar_livros/{id}")
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
@app.delete("/Deletar_livros/{id}")
async def Deletar_livros(id: int):
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
@app.post("/Criar Autores")
async def criar_autores(autor: autores):

    conn = await conectar()

    novo_autor = await conn.fetchrow(
        """
        INSERT INTO autores(nome)
        VALUES($1)
        RETURNING *
        """,
        autor.autor
    )

    await conn.close()

    return dict(novo_autor)

#READ
@app.get("/Listar_autores")
async def listar_autores():

    conn = await conectar()

    result = await conn.fetch("SELECT * FROM autores")

    conn.close()

    return [dict(r) for r in result]

#UPDATE
@app.put("/Update_autores/{id}")
async def atualizar_autores(id: int, autor: autores):
    conn = await conectar()
    result = await conn.fetchrow(
        """
        UPDATE autores
        SET nome = $1
        WHERE id = $2
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
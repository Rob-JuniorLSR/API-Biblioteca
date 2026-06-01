from pydantic import BaseModel

class autores(BaseModel):
    autor: str

class livro(BaseModel):
    titulo: str
    autor: str
    genero: str
    ano: int
    quantidade: int

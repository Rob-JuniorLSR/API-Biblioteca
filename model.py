from pydantic import BaseModel

class Livro(BaseModel):
    titulo: str
    autor: str
    genero: str
    ano_publicacao: int
    quantidade: int
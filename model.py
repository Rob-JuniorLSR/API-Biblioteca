from pydantic import BaseModel

class Item(BaseModel):
    titulo: str
    autor: str
    genero: str
    ano: int
    quantidade: int
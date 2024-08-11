from pydantic import BaseModel

class ItemSchema(BaseModel):
    bookid: int
    quantity: int
from pydantic import BaseModel,Field

class BookSchema(BaseModel):
    title:str 
    author:str
    price:int
    quantity:int
    userid: int

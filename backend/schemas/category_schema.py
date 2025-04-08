from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    skills: list[int] = []  # Assuming skills is a list of skill IDs

    class Config:
        orm_mode = True  # Enable ORM mode to read data as attributes
        arbitrary_types_allowed = True


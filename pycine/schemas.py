from pydantic import BaseModel

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class FavoriteBase(BaseModel):
    idMovie: int
    idUser: int

class Favorites(FavoriteBase):
    id: int

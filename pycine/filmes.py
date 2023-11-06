from fastapi import FastAPI, Query
from typing import List
import json
import request
import uvicorn

app = FastAPI()

from fastapi.middleware.cors import (
     CORSMiddleware
)
# habilita CORS (permite que o Svelte acesse o fastapi)
origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#region ------- CRUD USERS -------

@app.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.check_for_existing_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
        

@app.delete("/user", response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    return crud.del_users(db=db, id=id)

@app.get("/user", response_model=list[schemas.User])
def read_all_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_users = crud.get_users(db, skip=skip, limit=limit)
    return all_users

@app.get("/user/getUserByEmail", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db=db, email=email)

#endregion

#region ------- CRUD FAVORITOS -------

@app.post("/favorite", response_model=schemas.Favorites)
def favorite_movie(favorite: schemas.FavoriteBase, db: Session = Depends(get_db)):
    return crud.favorite_movies(db=db, idUser=favorite.idUser, idMovie=favorite.idMovie)

@app.get("/favorite", response_model=list[schemas.Favorites])
def get_favorite_movies(db: Session = Depends(get_db), email = str):
    return crud.get_favorite_movies(db=db, email=email)

@app.delete("/favorite", response_model=schemas.Favorites)
def delete_favorite_movie(favorite: schemas.FavoriteBase, db: Session = Depends(get_db)):
    return crud.delete_favorite_movie(db=db, idUser=favorite.idUser, idMovie=favorite.idMovie)

#endregion

#region ------- COISA NORMAL -------

@app.get("/filmes/getMoviesById")
def getMovieById(ids: list[int] = Query(None)):
    teste = request.getMovieById(ids)
    return teste

# - endpoint que retorna 5 filmes recomendados da semana (definidos em uma lista no python)
@app.get("/filmes/top5melhoresSemana")
def getTop5melhoresSemana():
    json = request.getTop5TrendingMovies()
    filmes = []
    for filme in json:
        filmes.append(filme['original_title'])
    
    return filmes

@app.get("/filmes/getMovieInfo")
def getMovieInfo():
    json = request.getMovieInfo()
    
    return json

@app.get("/filmes/getMovieByNameAndSortByPopular/{name}")
def getMovieByNameAndSortByPopular(name: str):
    json = request.getMovieByNameAndSortByPopular(name)
    
    return json

@app.get("/atores/getFilmesAtor/{id}")
def getFilmesAtor(id: int):
    json = request.getMoviesFromPeople(id)
    return json

@app.get("/atores/{id}")
def getAtor(id: str):
    json = request.getPeopleByIdJson(id)
    return json
#endregion
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

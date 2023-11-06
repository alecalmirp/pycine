import requests

URL_MOVIES = "https://api.themoviedb.org/3/discover/movie"
URL_GENRES = "https://api.themoviedb.org/3/genre/movie/list?language=en"
URL_MOVIE_BY_NAME = "https://api.themoviedb.org/3/search/movie?query="
URL_PEOPLE = "https://api.themoviedb.org/3/search/person"
URL_PEOPLE_BY_ID = "https://api.themoviedb.org/3/person/"
URL_PEOPLE_MOVIES_BY_ID1 = "https://api.themoviedb.org/3/person/"
URL_PEOPLE_MOVIES_BY_ID2 = "/movie_credits?language=en-US"
URL_TRENDING_WEEK_MOVIES = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
URL_MOVIE_BY_ID = "https://api.themoviedb.org/3/movie/"
PARAMS = "?sort_by=vote_count.desc"
API_KEY = "3e101e8fbfa869feea82a31a551e6354"

def getPopularsJson():
    endpoint = URL_MOVIES + PARAMS + "&api_key=" + API_KEY
    headers = {"accept": "application/json"}
    response = requests.get(endpoint, headers=headers)

    return response.json()

def getTrendingMoviesJson():
    endpoint = URL_TRENDING_WEEK_MOVIES + "&api_key=" + API_KEY
    response = requests.get(endpoint)

    return response.json()

def getGenresJson():
    genresEndpoint = URL_GENRES + "&api_key=" + API_KEY
    headers = {"accept": "application/json"}
    response = requests.get(genresEndpoint, headers=headers)

    return response.json()

def getPeopleJson(name):
    peopleEndpoint = URL_PEOPLE + "?api_key=" + API_KEY + "&query=" + name
    headers = {"accept": "application/json"}
    response = requests.get(peopleEndpoint, headers=headers)

    return response.json()

def getPeopleByIdJson(id: str):
    endpoint = URL_PEOPLE_BY_ID + id + "?api_key=" + API_KEY
    response = requests.get(endpoint)

    return response.json()

def getPeopleMoviesByIdJson(id):
    endpoint = URL_PEOPLE_MOVIES_BY_ID1 + id + URL_PEOPLE_MOVIES_BY_ID2 + "&api_key=" + API_KEY
    response = requests.get(endpoint)

    return response.json()

def findGenre(generos_filme, generos):
    Lista_generos = []
    for generoF in generos_filme:
        for genero in generos:
            if generoF == genero['id']:
                Lista_generos.append(genero['name'])
    return Lista_generos

def findGenre2(generos_filme, generos):
    Lista_generos = []
    for generoF in generos_filme:
        for genero in generos:
            if generoF == genero['id']:
                Lista_generos.append(genero['name'])
    return Lista_generos

def getMovieInfo():
    filmes = getPopularsJson()['results']
    generos = getGenresJson()['genres']
    retorno = []
    for item in filmes:
        json = {}
        json['nome'] = item['original_title']
        json['id'] = item['id']
        json['generos'] = findGenre(item['genre_ids'], generos)
        json['imagem'] = f"https://image.tmdb.org/t/p/w185{item['poster_path']}"
        retorno.append(json)

    return retorno
# - busca nome do gênero fornecido o id
def getGenreById(id):
    generos = getGenresJson()['genres']
    for genero in generos:
        if genero['id'] == id:
            return genero['name']
    return "Gênero não encontrado."

# - busca um filme pelo título
def getMovieByName(name):
    return requests.get(URL_MOVIE_BY_NAME + name + "&api_key=" + API_KEY).json()

# - busca artista pelo nome.
def getPeopleByName(name):
    return getPeopleJson(name)['results']

def getTop5TrendingMovies():
    json = getTrendingMoviesJson()['results']
    filmes = []
    for i in range(5):
        filmes.append(json[i])

    return filmes

def getPeopleOrderedByPopularity(name):
    json = getPeopleJson(name)['results']
    populares = []
    for person in json:
        populares.append({
            'id': person['id'],
            'name': person['name'],
            'rank': person['popularity']
        })
    
    populares.sort(reverse=True, key=lambda person:person['rank'])
    return populares

def getMovieByNameAndSortByPopular(name):
    json = getMovieByName(name)['results']
    populares = []
    for filme in json:
        populares.append({
            'id': filme['id'],
            'nome': filme['original_title'],
            'popularidade': filme['popularity']
        })
    
    populares.sort(reverse=True, key=lambda filme:filme['popularidade'])
    return populares

def getMoviesFromPeople(id):
    idAtor = str(id)
    filmes = getPeopleMoviesByIdJson(idAtor)#['cast']

    return filmes
    ator = getPeopleByIdJson(idAutor)
    generos = getGenresJson()
    info = {
        'id': ator['id'],
        'nome': ator['name'],
        'popularidade': ator['popularity'],
        'aniversario': ator['birthday'],
        'biografia': ator['biography'],
        'filmes': []
    }
    for filme in filmes:
        info['filmes'].append({
            'nome_filme': filme['original_title'],
            'generos': findGenre(filme['genre_ids'], generos),
            'resumo': filme['overview']
        })
    
    return info

def getMovieById(ids):
    generos = getGenresJson()['genres']
    movies = []
    for id in ids:
        temp = requests.get(URL_MOVIE_BY_ID + str(id) + "?api_key=" + API_KEY).json()
        json = {}
        json['nome'] = temp['original_title']
        json['id'] = temp['id']
        json['generos'] = findGenre2(temp['genres'], generos)
        json['imagem'] = f"https://image.tmdb.org/t/p/w185{temp['poster_path']}"
        movies.append(json)
    return movies



if __name__ == "__main__":
    print(getPeopleByName("Arnold"))

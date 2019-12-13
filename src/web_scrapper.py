import requests
from bs4 import BeautifulSoup
import json

def wiki_scraper():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_Disney_animated_universe_characters"
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
        r=requests.get(url,headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,'lxml')
            a = soup.findAll("table",{"class":"wikitable sortable"})
            # a = soup.findAll("table",{"class":"wikitable sortable"})[0].find("tbody")
            character_movie = {}
        #     char_count = 0
            for i in range(len(a)):
                b = a[i].find("tbody")
                count = 0
                for k in b.findAll("tr"):
                    if count >0:
                        split_data = k.text.splitlines()
                        if len(split_data)>3:
                            char = split_data[1]
                            movie = split_data[-1]
                            if movie: # make sure movie is not null
                                if movie not in character_movie:
                                    character_movie[movie] = [char]
                                else:
                                    character_movie[movie].append(char)
                    count +=1
            return character_movie
        else:
            print (f"Can't find the page you are look, page status code:{r.status_code}")
    except ConnectionError:
         print ("NO internet connection")


def omdb_cleaning(a):
    flag = 0
    new_ombd_info ={}
    if "Year" in a:
        new_ombd_info["Year"] = a["Year"]
    else:
        new_ombd_info["Year"] = None
    if "Genre" in a:
        new_ombd_info["Genre"] = a["Genre"]
    else:
        new_ombd_info["Genre"] = None
    if "imdbRating" in a:
        new_ombd_info["imdbRating"] = a["imdbRating"]
    else:
        new_ombd_info["imdbRating"] = None
    if "imdbID" in a:
        new_ombd_info["imdbID"] = a["imdbID"]
    else:
        new_ombd_info["imdbID"] = None
        flag = 1
    if "Production" in a:
        new_ombd_info["Production"] = a["Production"]
    else:
        new_ombd_info["Production"] = None
    if "BoxOffice" in a:
        new_ombd_info["BoxOffice"] = a["BoxOffice"]
    else:
        new_ombd_info["BoxOffice"] = None
    if "Title" in a:
        new_ombd_info["Title"] = a["Title"]
    else:
        new_ombd_info["Title"] = None
        flag = 1 # if title is none, just igorn the data and do not put it in the dictionary
    if "Metascore" in a:
        new_ombd_info["Metascore"] = a["Metascore"]
    else:
         new_ombd_info["Metascore"] = None
    return (new_ombd_info,flag)

def omdbapi_fetcher(character_movie):
    movie_info = []
    # character_movie = wiki_scraper()
#     print (character_movie)
    for movie in character_movie:
#         print (movie)
        count = 0
        try:
            url = f'http://www.omdbapi.com/?apikey=9acfd057&t={movie}'
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
            r=requests.get(url,headers=headers)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text,'lxml')
                movie_info_dic = json.loads(soup.find('p').text)
                # if movie_info_dic != {'Response': 'False', 'Error': 'Movie not found!'}:
                clean_result = omdb_cleaning(movie_info_dic)
                # if the imdb id and movie title is none, the data will be discarded
                if clean_result[1] == 0:
                    movie_info_dic = clean_result[0]
                    movie_info_dic["character"] = character_movie[movie]
                    movie_info.append(movie_info_dic)
                    count +=1
                # print (f"Can't find the page you are look, page status code:{r.status_code}")
        except ConnectionError:
            print ("NO internet connection")
    return movie_info

def get_keywords(dic):
    keywords = []
    if "keywords" in dic:
        for a in dic["keywords"]:
            if "name" in a:
                 keywords.append(a["name"])
        if len(keywords) == 0:
            keywords = None
    else:
        keywords = None
    return keywords

def themoviedb_fetcher(movie_info_list):
    # new_fetcher
    for movie in movie_info_list:
        if movie.get("imdbID") != None:
            movie_id = movie["imdbID"]
            try :
                url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key=3c6fb1f0e486a504ca5cf36034dcf7fc"
                headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.3c6fb1f0e486a504ca5cf36034dcf7fc0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
                r=requests.get(url,headers=headers)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text,'lxml')
                    dic = json.loads(soup.find('p').text)
                    movie["keywords"] = get_keywords(dic)
                else:
                    movie["keywords"] = None
            except ConnectionError:
                print ("NO internet connection")
        else:
            movie["keywords"] = None
    return movie_info_list


def fetch_all_data():
    character_movie = wiki_scraper()
    movie_info_list = omdbapi_fetcher(character_movie)
    whole_movie_data = themoviedb_fetcher(movie_info_list)
    return whole_movie_data

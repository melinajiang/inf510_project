import pandas as pd

def check_heading_exist(cx):
    count = 0
    for a in cx:
        count +=1
        if "Year" not in a:
            print ("Year not in", a,"filling with None")
            a["Year"] = None
        if "Genre" not in a:
            print ("Genre not in", a,"filling with None")
            a["Genre"] = None
        if "imdbRating" not in a:
            print ("imdbrating not in", a,"filling with None")
            a["imdbRating"] = None
        if "imdbID" not in a:
            print ("imdbID",a,"filling with None")
            a["imdbID"] = None
        if "Production" not in a:
            print ("Production not in",a,"filling with None")
            a["Production"] = None
        if "character" not in a:
            print ("character",a,"filling with None")
            a["character"] = None
        if "keywords" not in a:
            print ("keywords",a,"filling with None")
            a["keywords"] = None
        if "BoxOffice" not in a:
            print ("BoxOffice",a,"filling with None")
            a["BoxOffice"] = None
    print ("                  >>>Check",count,"item and fill in the non-existance heading")

def prepare_list_for_df(movie_info_data):

    movie_basic_info_df_list = [] # list of list
    char_info_df_list = [] #list of list
    keyword_df_list = [] # list of list
    gerne_info_df_list = []  # list of list

    for per_movie_info in movie_info_data:
        # per_movie_info = movie_info_data[piece]

        # get per movie basic info
        per_basic_info_list = []
        title = per_movie_info["Title"]
        year = per_movie_info["Year"]
        meta_score = per_movie_info["Metascore"]
        imdb_rating = per_movie_info["imdbRating"]
        imdb_id = per_movie_info["imdbID"] # primary key, need to have unique constrait
        box_office = per_movie_info["BoxOffice"]
        pc = per_movie_info["Production"]
        per_basic_info_list.extend([title,year,meta_score,imdb_rating,box_office,pc])
        movie_basic_info_df_list.append(per_basic_info_list)


        if per_movie_info["character"]!=None:
            for c in per_movie_info["character"]:
                    per_character_list=[title,year,c,imdb_rating,box_office]
                    char_info_df_list.append(per_character_list)

        if per_movie_info["Genre"]!=None:
            for g in per_movie_info["Genre"]:
                    per_genre_list=[title,year,g,imdb_rating,box_office]
                    gerne_info_df_list.append(per_genre_list)

        if per_movie_info["keywords"]!=None:
            for k in per_movie_info["keywords"]:
                    per_keywords_list=[title,year,k,imdb_rating,box_office]
                    keyword_df_list.append(per_keywords_list)
    return (movie_basic_info_df_list,char_info_df_list,gerne_info_df_list,keyword_df_list)


def model_into_dataframes(copy):

    df_prepare_data = prepare_list_for_df(copy)
    movie_basic_info_list = df_prepare_data[0]
    movie_baise_info = pd.DataFrame(movie_basic_info_list, columns=['Movie Name',"Year","Meta Score","IMDb Rating","Box Office","Production Company"])
    movie_baise_info.append(movie_basic_info_list,ignore_index=True)

    char_basic_info_list = df_prepare_data[1]
    char_basic_info = pd.DataFrame(char_basic_info_list, columns=['Movie Name',"Year","Character","IMDb Rating","Box Office"])
    char_basic_info.append(char_basic_info_list,ignore_index=True)

    genre_basic_info_list = df_prepare_data[2]
    genre_basic_info = pd.DataFrame(genre_basic_info_list, columns=['Movie Name',"Year","Genre","IMDb Rating","Box Office"])
    genre_basic_info.append(genre_basic_info_list,ignore_index=True)

    keywords_basic_info_list = df_prepare_data[3]
    keywords_basic_info = pd.DataFrame(keywords_basic_info_list, columns=['Movie Name',"Year","Keyword","IMDb Rating","Box Office"])
    keywords_basic_info.append(keywords_basic_info_list,ignore_index=True)

    return (movie_baise_info,char_basic_info,genre_basic_info,keywords_basic_info)

def write_into_csv(dataframe,filename):
    dataframe.to_csv(filename,index=False)

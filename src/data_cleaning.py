def clean_movie_info_data(movie_info_data):
    for per_movie_info in movie_info_data:
        # change metascore into int
        meta_score = per_movie_info["Metascore"]
        try :
            per_movie_info["Metascore"] = int (meta_score)
        except ValueError:
            per_movie_info["Metascore"] = None

        # change imdb rating into int
        imdb_rating = per_movie_info["imdbRating"]
        try :
            per_movie_info["imdbRating"] = float (imdb_rating)
        except ValueError:
            per_movie_info["imdbRating"] = None

        # split genre info into a list
        genre = per_movie_info["Genre"]
        if genre != None:
            genre_list = genre.split(",")
            if len(genre_list) == 0:
                per_movie_info["Genre"] = None
            else:
                per_movie_info["Genre"] = genre_list

        # change box office into int
        box_office = per_movie_info["BoxOffice"]
        if box_office != None:
            split_result = box_office.split("$")
            if len(split_result)<2:
                per_movie_info["BoxOffice"] = None
            else:
                per_box_office = split_result[1]
                per_box_office=int ("".join(per_box_office.split(",")))
                per_movie_info["BoxOffice"] = per_box_office

        # change year into int
        if per_movie_info["Year"] != None:
            try:
                per_movie_info["Year"] = int (per_movie_info["Year"])
            except ValueError:
                release_year = per_movie_info["Year"].split("–")[0]
                per_movie_info["Year"] = int (release_year)

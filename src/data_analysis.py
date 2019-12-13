import pandas as pd
import squarify
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

"""
read_file function reads a csv file into a dataframe

INPUT:
a file name or file path

OUTPUT:
a dataframe that contains the file information

"""

def read_file (filename):
    try:
        dataframe = pd.read_csv(filename)
        return dataframe
    except FileNotFoundError:
        print (f"File not found {filename}")

"""
most_frequent function calculates the most frequent element in a list; Reference from: https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/

INPUT:
a list

OUTPUT:
the most frequently appeared element in the list inputted

"""
def most_frequent(List):
    return max(set(List), key = List.count)
"""
genre_change_overtime function calculates how disney animated moive's genre change during the decades

INPUT:
the dataframe contains movie genre and movie released year

OUTPUT:
print out the the most frequent appeared disney animated moive's genre of each decade

"""
def genre_change_overtime(genre_info):
    years = genre_info["Year"].unique()
    i = 0
    y = 0
    flag = 0
    while y<90:
        print ("===")
        most_common_genre_tenyear = []
        while i<10:
            if y+i < len(years):
                filtered_data = genre_info[genre_info["Year"] == years[y+i]]
                most_common_movie = list(filtered_data["Genre"].mode())
                for cm in most_common_movie:
                    cm = cm.strip()
                    most_common_genre_tenyear.append(cm)
    #             print (years[y+i],most_common_frequence,most_common_movie)
                i+=1
            else:
                flag = 1
                break
        print (f"In {years[y]} to {years[y+i-1]} the most frequent genre type is: ",most_frequent(most_common_genre_tenyear))
        if flag ==0:
            y+=10
            i=0
        else:
            break

"""
most10_genre_tree_map function draws a tree map of the top 10 most appeared genre and their appeared frequency over the 90 years

INPUT:
the dataframe contains genre infomation

OUTPUT:
the tree map of the top 10 most appeared genre and their appeared frequency over the 90 years

"""

def most10_genre_tree_map(genre_info):

    # get 10 most occurred disney movie's genre and the time they occurs
    movie_genre_top10 = genre_info["Genre"].value_counts().head(10).keys()
    genre_frequency = genre_info["Genre"].value_counts().head(10).values

    len_file = len(genre_info.index)
    gerne_with_per = []
    percentage = []
    occurance = list(genre_info["Genre"].value_counts().head(10).values)

    # calculate the percentage of 10 most occurred genre in all disney movie
    for o in occurance :
        per = o/len_file
        per = round(per,2)
        percentage.append(int(per*100))

    for i in range(len(percentage)):
        gwp = movie_genre_top10[i].strip()+"\n" + str(percentage[i])+"%"
        gerne_with_per.append (gwp)

    # color the tree map
    norm = matplotlib.colors.Normalize(vmin=genre_frequency.min(), vmax=genre_frequency.max())
    colors = [matplotlib.cm.tab10(norm(value)) for value in genre_frequency[::2]]


    fig = plt.gcf()
    ax = fig.add_subplot()
    fig.set_size_inches(16, 4.5)

    squarify.plot(sizes=genre_frequency, color = colors, label=gerne_with_per, alpha=.9 )
    fig.suptitle("Top 10 most appeared gernes and their appeared frequency over 90 years",fontsize=18,fontweight="bold")
    plt.axis('off')
    plt.show()

"""
genre_rating_relation draws a scatter plot that show the relationship between the movie genre and their imdb rating over 90 years

INPUT:
the dataframe contains genre information

OUTPUT:
a scatter plot that show the relationship between the movie genre and their imdb rating over 90 years

"""
def genre_rating_relation(genre_info):
# Get the relationsip of the genre and rating data over years
    filtered_gerne_data = genre_info
    group = filtered_gerne_data.groupby(['Genre','Year']).mean()
    genre_per_year = group["IMDb Rating"].reset_index()
    a = sns.relplot(x='Year', y='IMDb Rating', kind='scatter', hue='Genre',data=genre_per_year)
    a.fig.suptitle("The relationship between disney animated movie genre and their average yearly imdb rating over 90 years", fontsize=20,fontweight="bold",y=1.2)
    a.fig.set_size_inches(17,6)
    # movie_genre_top10 = genre_info["Genre"].value_counts().head(10).keys()
    # filtered_gerne_data = genre_info[genre_info["Genre"].isin(movie_genre_top10)]
    # group = filtered_gerne_data.groupby(['Genre','Year']).mean()
    # genre_per_year = group["IMDb Rating"].reset_index()
    # a = sns.relplot(x='Year', y='IMDb Rating', kind='scatter', hue='Genre',data=genre_per_year)
    # a.fig.suptitle("The relationship between disney animated movie genre and the imdb rating over 90 years", fontsize=20,fontweight="bold")
    # a.fig.set_size_inches(17,6)

"""
basic_info_stats function shows the movie's basic statistics information

INPUT:
the dataframe contains moive's name, released year, production company and their imbd rating

OUTPUT:
None, but will print out:
the production that makes the most movie
the year that released the most movie is
they year released the highest meta rating moive
the year released the highest IMDb rating moive
"""

def basic_info_stats(basic_info):
#  Showing the movie's basic statistics information

    print ("Showing the movie's basic statistics information : ")
    print ()

    most_pro = basic_info ["Production Company"].value_counts().head(1)
    print (f" **  The production company made the most movie is: *{most_pro.keys()[0]}*; A total {most_pro.values[0]} movie is made ** ")

    most_year = basic_info ["Year"].value_counts().head(1)
    print (f" **  The year released the most movie is: *{most_year.keys()[0]}*; A total {most_year.values[0]} movie is released ** ")

    highest_meta = basic_info[["Year","Movie Name","IMDb Rating"]].loc[basic_info["Meta Score"]== basic_info["Meta Score"].max()].values
    print (f" **  In *{highest_meta[0][0]}* there released the highest meta rating moive: {highest_meta[0][2]} for movie \"{highest_meta[0][1]}\" ** ")

    highest_imbd = basic_info[["Year","Movie Name","IMDb Rating"]].loc[basic_info["IMDb Rating"]== basic_info["IMDb Rating"].max()].values
    print (f" **  In *{highest_imbd[0][0]}* there released the highest IMDb rating moive: {highest_imbd[0][2]} for movie \"{highest_imbd[0][1]}\" ** ")

"""
get_char_gender function using an existing api to query a character's gender using the character's name and write them to a file

INPUT:
num of character wanted to be query
the dataframe contains character information

OUTPUT:
None, after querying the character's gender, the results will be store in a dataframe and then write into a csv file
"""

def get_char_gender(num,char_info):
    # get the char's gender info by using a gender classifier api
    count=0
    test_char = char_info["Character"]
    while count <= num:
        c = test_char[count]
        name_list = c.split(" ")
        gender_value = 0
#         print ("reset gender value")
        flag = 0
        for name in name_list:
            try:
                # debug
                if re.search('[a-zA-Z]', name):
                    try :
                        url = 'https://api.genderize.io?name='+name+'&apikey=0798cdce66609e67d8c1fe16816d7234'
                        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
                        r=requests.get(url,headers=headers)
                        if r.status_code == 200:
                            soup = BeautifulSoup(r.text,'lxml')
                            dic = json.loads(soup.find('p').text)
        #                     print (dic)
                            n = dic["gender"] # 1--m ; -1 --f ; percentage
                            p = dic["probability"]
                            if n =="female":
                                gender_value = gender_value + -1*p
                            elif n == "male":
                                gender_value = gender_value + 1*p
                        else:
                            print (f"Can't find the page of name {name} you are look, page status code:{r.status_code}")
                    except ConnectionError:
                        print ("Not internet connection")
                else:
                    print ("the split string contains no alphabet")
            except :
                print ("a problem occurs")
                flag = 1
                pass
        if flag ==0:
#             gender_list.append(gender_value)
            if gender_value > 0 :
                char_info.loc[count,"gender"] ="male"
                print (count,c,gender_value,"male")
            elif gender_value < 0:
                char_info.loc[count,"gender"] ="female"
                print (count,c,gender_value,"female")
            else:
                char_info.loc[count,"gender"] ="None"
                print (count,c,gender_value,"None")

            count+=1
        else:
            print ("exception occurs")

"""
gender_classifier_runner function goes through the gender querying by calling get_char_gender function
Noted: as the runner takes a long time to get the final result, there is a test sample in the runner function as well

INPUT:
the dataframe contains character information

OUTPUT:
None, after querying the character's gender, the results will be store in a dataframe and then write into a csv file

"""

# add try and catch
def gender_classifier_runner(char_info):

    count = 0
    print (" !!! This character gender classification function took me over 30 mins to get the result !!!")
    print ("--------------------")
    print ("If you want to see the test sample please press 1")
    print ("If you want to skip the process and see the result please press 2")
    print ("If you want to see the whole process please press 3")
    print ("--------------------")
    user_input = input ("Your input: ")
    if user_input== "1":
        print ("The test will show 5 names and its gender")
        get_char_gender(4,char_info)
        display(char_info)
        print ("Test end")
    elif user_input=="2":
        print ("Reading the processed csv file")
        print (" >>> Display the result in dataframe form: ")
        try:
            char_gender_info = pd.read_csv("./data/char_info_update2.csv")
            display(char_gender_info)

        except FileNotFoundError:
            print ("Path not found ./data/char_info_update2.csv")
    elif user_input=="3":
        print ("Show the whole process of the character gender classification")
        get_char_gender(len(char_info["Character"])-1,char_info)
        print ("writing the result to file!")
        try:
            char_info.to_csv("./data/char_info_update2.csv",index=False)
        except FileNotFoundError:
            print ("Path not found ./data/char_info_update2.csv")
        print ("writing complete")
    else:
        print ("Your input can't be recognized")

"""
display_male_char_per function will draw a scatter plot that depicts how male character's percentage change in Disney animated movies over the years over 90 years

INPUT:
a dataframe contains character gender inforamtion

OUTPUT:
a scatter plot that depicts how male character's percentage change in Disney animated movies over the years over 90 years
"""
def display_male_char_per(char_gender_info):
    char_gender_info = pd.DataFrame({'Percentage': char_gender_info.groupby(by=['Movie Name', 'gender',"Year"]).size()/char_gender_info.groupby(by=['Movie Name']).size() })
    char_per_movie = char_gender_info["Percentage"].reset_index()

    char_per_movie_male = char_per_movie[char_per_movie["gender"] =="male"]

    a = sns.relplot(x='Year', y='Percentage', kind='scatter', hue='Movie Name', data=char_per_movie_male)
    a.fig.suptitle("Male character's percentage change in Disney animated movies over the years over 90 years",fontsize=23,fontweight="bold",y=2.9)

    a.fig.set_size_inches(18,6)
"""
display_female_char_per function will draw a scatter plot that depicts how female character's percentage change in Disney animated movies over the years over 90 years

INPUT:
a dataframe contains character gender inforamtion

OUTPUT:
a scatter plot that depicts how female character's percentage change in Disney animated movies over the years over 90 years
"""
def display_female_char_per(char_gender_info):
    char_gender_info = pd.DataFrame({'Percentage': char_gender_info.groupby(by=['Movie Name', 'gender',"Year"]).size()/char_gender_info.groupby(by=['Movie Name']).size() })
    char_per_movie = char_gender_info["Percentage"].reset_index()

#     char_per_movie_male = char_per_movie[char_per_movie["gender"] =="male"]
    char_per_movie_female = char_per_movie[char_per_movie["gender"] =="female"]

    a = sns.relplot(x='Year', y='Percentage', kind='scatter', hue='Movie Name', data=char_per_movie_female)
    a.fig.suptitle("Female character's percentage change in Disney animated movies over the years over 90 years",fontsize=23,fontweight="bold",y=2.5)
    a.fig.set_size_inches(18,5)

"""
keyword_world_cloud function draws a world cloud that is made of all the disney animated movie's keyword

INPUT:
a dataframe contains keyword information

OUTPUT:
a world cloud that is made of all the disney animated movie's keyword
"""
def keyword_world_cloud(kw):
    text = " ".join(list(kw["Keyword"]))
    try: 
        micky_mask = np.array(Image.open("mm.png"))
        # mm = m
        # micky_mask

        wordcloud = WordCloud(background_color="white",mask=micky_mask).generate(text)

        # Display the generated image:
        # the matplotlib way:

        image_colors = ImageColorGenerator(micky_mask)

    #     plt.title("Disney animated movie's keywords over the years over 90 years",fontsize=23,fontweight="bold")
        fig = plt.figure(figsize=[20,10])
        fig.suptitle("Disney animated movie's keywords over the years over 90 years", fontsize=20,fontweight="bold")
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    except FileNotFoundError:
        print ("Please include the picture mm.png in the same fold with notebook!")

import pandas as pd
import dataframe_display
# from tabulate import tabulate

def local_fetcher(f):
    print (">>>Try reading files")
    flag = 0
    try:
        file_reader1 = pd.read_csv('movie_basic_info.csv')
        print("      >>>File read success : movie_basic_info.csv!")
    except FileNotFoundError:
        print ("Exception Statement: movie_basic_info.csv seems not exist, please put the csv file in the script's dictionary")
        flag = 1
    except pd.io.common.EmptyDataError:
        print ("Exception Statement: movie_basic_info.csv empty")
        flag = 1
    except:
        print ("There are other issues opening : movie_basic_info.csv")

    try:
        file_reader2 = pd.read_csv('char_basic_info.csv')
        print("      >>>File read success: char_basic_info.csv!")
    except FileNotFoundError:
        print ("Exception Statement: char_basic_info.csv seems not exist, please put the csv file in the script's dictionary")
        flag = 1
    except pd.io.common.EmptyDataError:
        print ("Exception Statement: char_basic_info.csv empty")
        flag = 1
    except:
        print ("There are other issues opening : char_basic_info.csv empty")

    try:
        file_reader3 = pd.read_csv('genre_basic_info.csv')
        print("      >>>File read success: genre_basic_info.csv!")
    except FileNotFoundError:
        print ("Exception Statement: genre_basic_info.csv seems not exist, please put the csv file in the script's dictionary")
        flag = 1
    except pd.io.common.EmptyDataError:
        print ("Exception Statement: genre_basic_info.csv is empty")
        flag = 1
    except:
        print ("There are other issues opening : genre_basic_info.csv")

    try:
        file_reader4 = pd.read_csv('keywords_basic_info.csv')
        print("      >>>File read success: keywords_basic_info.csv!")
    except FileNotFoundError:
        print ("Exception Statement: keywords_basic_info.csv seems not exist, please put the csv file in the script's dictionary")
        flag = 1
    except pd.io.common.EmptyDataError:
        print ("Exception Statement: keywords_basic_info.csv is empty")
        flag = 1
    except:
        print ("There are other issues opening : keywords_basic_info.csv")

    if flag == 0:
        if f == 1:
            dataframe_display.display_in_cmd((file_reader1,file_reader2,file_reader3,file_reader4))
        else:
            dataframe_display.display_in_ipy((file_reader1,file_reader2,file_reader3,file_reader4))
    else:
        print ("There are some problem in reading files, some more about the exception statement")

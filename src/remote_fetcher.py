import web_scrapper
import data_cleaning
import data_modeling
import dataframe_display

def remote_fetcher(display_flag,runner_flag):
    print (">>>You started remote runner")
    flag_clean = 0
    print ("      >>>Fetching data from the website and apis")
    all_movie_info_data = web_scrapper.fetch_all_data()
    print ("      >>>Fetching complete")
    print ("            >>>Cleaning data to fill the null value and convert the data to excepted types")
    if flag_clean ==0:
        data_cleaning.clean_movie_info_data(all_movie_info_data)
        flag_clean =1
        print ("            >>>Cleaning complete")

    print ("                  >>>Checking field existance for every movie before modeling into the dataframe")
    data_modeling.check_heading_exist(all_movie_info_data)
    print ("                  >>>Checking complete")
    print ("                              >>>Modeling into dataframes")
    data_frames = data_modeling.model_into_dataframes(all_movie_info_data)
    print ("                              >>>Modeling complete")
    print()

    if runner_flag ==1:
        while True:
            print ("Press 1 to view the dataframes, press 2 to view to store in the csv file, Press 3 to quit the remote runner")
            input_data = input()
            if input_data!="1" and input_data!="2" and input_data!="3":
                print("!!!! You pressed wrong button, please do it again !!!!")
            elif input_data=="1":
                if display_flag == 1:
                    dataframe_display.display_in_cmd(data_frames)
                else:
                    dataframe_display.display_in_ipy(data_frames)
            elif input_data =="2":
                print(">>>Writing the dataframes into csv file")
                print()
                csv_names = ["movie_basic_info.csv","char_basic_info.csv","genre_basic_info.csv","keywords_basic_info.csv"]
                for i in range(len(csv_names)):
                    print (f"Writing the #{i+1} dataframe to {csv_names[i]}")
                    data_modeling.write_into_csv(data_frames[i],csv_names[i])
                    print (f"#{i+1} dataframe writing complete")
            elif input_data == "3":
                break
    else:
        print(">>>Writing the dataframes into csv file")
        print()
        csv_names = ["movie_basic_info.csv","char_basic_info.csv","genre_basic_info.csv","keywords_basic_info.csv"]
        for i in range(len(csv_names)):
            print (f"Writing the #{i+1} dataframe to {csv_names[i]}")
            data_modeling.write_into_csv(data_frames[i],csv_names[i])
            print (f"#{i+1} dataframe writing complete")

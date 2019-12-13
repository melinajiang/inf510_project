import pandas as pd

def display_in_cmd(data_frames):
    print ("Displaying dataframes:")
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.max_rows', 10)
    print ("==============The dataframes are:=============")
    print ()
    print (">>>Movie basic information:")
    print(data_frames[0])
    print (">>> Character basic information:")
    print (data_frames[1])
    print (">>> Genre basic information:")
    print (data_frames[2])
    print (">>> Keywords basic information:")
    print (data_frames[3])

def display_in_ipy(data_frames):
    print ("==============The dataframes are:=============")
    print ()
    print (">>>Movie basic information:")
    display(data_frames[0])
    print (">>> Character basic information:")
    display (data_frames[1])
    print (">>> Genre basic information:")
    display (data_frames[2])
    print (">>> Keywords basic information:")
    display (data_frames[3])

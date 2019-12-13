import remote_fetcher
import local_fetcher
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", type=str,choices=["local", "test"], help="where data should be gotten from")
    args = parser.parse_args()
    location = args.source
    print (location)
    if location == "local":
        if not os.path.exists('movie_basic_info.csv') or not os.path.exists('movie_basic_info.csv') or not os.path.exists('char_basic_info.csv') or not os.path.exists('genre_basic_info.csv'):
            print ("There is no local file now, will run the remote runner to fetch data from web first")
            # print (os.path.exists('movie_basic_info.csv'))
            # print (os.path.exists('movie_basic_info.csv'))
            # print (os.path.exists('char_basic_info.csv'))
            # print (os.path.exists('genre_basic_info.csv'))
            remote_fetcher.remote_fetcher(1,0)
            local_fetcher.local_fetcher(1)
        else:
            local_fetcher.local_fetcher(1)
    else:
        remote_fetcher.remote_fetcher(1,1)

if __name__ == "__main__":
    print ("Running from command line")
    main()
else:
    while True:
        print("Running from ipython")
        location = input()
        print ("Choose the source you want data to be read:")
        print ("Press 1 if you want to read data from local source")
        print ("Press 2 if you want to read data from remote source")
        if location =="1":
            # local_fetcher.local_fetcher(0)
            break
        elif location == "2":
            # remote_fetcher.remote_fetcher(0)
            break
        else:
            print ("Can not recognize your input, please try again")

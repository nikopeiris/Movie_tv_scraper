import urllib3
from bs4 import BeautifulSoup
import datetime

def tv_movie():
    while True:
        print("T = Tv Series\nM = Movie\n")
        try:
            choice = str(input("Tv Series Or Movie:")).lower().strip()
            if choice == "t":
                choice = "tv_series"
                break
            elif choice == "m":
                choice = "feature"
                break
            else:
                print("Enter a Valid Choice!!!\n")
        except ValueError:
            print("Enter a Valid Input!!!\n")
    
    check_year(choice)
    return

def check_year(choice):
    current_year = datetime.date.today().year
    while True:
        try:
            year = int(input("Enter The Year(eg:2016):"))
            
            if year <= current_year and year >= 1896:
                break
            else:
                print("\nPlease Enter a Valid Year!!!")

        except ValueError:
            print("\nOnly use Numerical Values!!!")
    
    scrape(year, choice)
    return


def scrape(year, choice):
    url = f"https://www.imdb.com/search/title/?title_type={choice}&release_date={year}-01-01,{year}-12-31"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    info_gathered = urllib3.PoolManager().request("GET", url, headers=headers).data
    info_parsed = BeautifulSoup(info_gathered, "lxml")

    list = info_parsed.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})

    if choice == "tv_series":
        print("/|Top {} Tv Series From {}|\\\n".format(len(list), year))
        tv(list)
    else:
        print("/|Top {} Movies From {}|\\\n".format(len(list), year))
        movie(list)
    
    return

def movie(list):
    print("Movie | Duration | Ratings\n")

    for movies in list:
        title = movies.find("h3", attrs={"class": "ipc-title__text"})
        duration = movies.find_all("span", attrs={"class": "sc-300a8231-7 eaXxft dli-title-metadata-item"})
        rating = movies.find("span", attrs={"class": "ipc-rating-star--rating"})

        try:
            print(title.text + " | " + duration[1].text + " | " + rating.text +"/10")
        except:
            print(title.text)

    return

def tv(list):

    print("Tv Series | Duration | Ratings\n")

    for series in list:
        title = series.find("h3", attrs={"class": "ipc-title__text"})
        duration = series.find_all("span", attrs={"class": "sc-300a8231-7 eaXxft dli-title-metadata-item"})
        rating = series.find("span", attrs={"class": "ipc-rating-star--rating"})

        try:
            print(title.text + " | " + duration[0].text + " | " + rating.text +"/10")
        except:
            print(title.text)

    return

def main():
    while True:
        tv_movie()
        redo = input('\n"R" to redo:')
        if redo.lower() == "r":
            pass
        else:
            print("\nApplication Exited :(")
            break

print("*Top 25 Movies Or Tv Series From Any Year*\n")
main()
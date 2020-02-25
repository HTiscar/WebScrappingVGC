from bs4 import BeautifulSoup, element
import numpy as np
import pandas as pd
import requests
import time
import unidecode
from datetime import datetime
from itertools import cycle
from lxml.html import fromstring
from requests.exceptions import ConnectionError, Timeout, ProxyError, RequestException
from urllib3.exceptions import ProtocolError
import sys
import os
sys.setrecursionlimit(10000)
proxy_enabled = True

def get_proxies(x):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    time.sleep(1)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:x + 1]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
def parse_url(url, proxy_origin):
    global response
    x = 0
    proxy_pool = cycle(proxy_origin)
    proxy = next(proxy_pool)

    while x == 0:
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            time.sleep(1)
            print('Connection established with VGChartz')
            print('Data Downloaded')
            x += 1
        except:
            print("Skipping. Connnection error. Proxy: ", proxy)
            proxy = next(proxy_pool)

    global soup
    soup = BeautifulSoup(response.text, "html.parser")

    global all_td_tags
    all_td_tags = soup.findAll('td')[59:1820]

def set_df(df):
    df['Rank'] = np.int32(all_td_tags[0].string)
    games_count = 0
    games_tag = 0

    for i in games_total:
        df.loc[games_count, 'Rank'] = all_td_tags[games_tag].string
        games_tag += 2
        df.loc[games_count, 'Url'] = all_td_tags[games_tag].a.get('href')
        df.loc[games_count, 'Name'] = all_td_tags[games_tag].a.string.strip()
        games_tag += 1
        df.loc[games_count, 'basename'] = unidecode.unidecode(
            df.loc[games_count, 'Name'].strip().split('/')[0].strip().replace(' ', '_'))
        df.loc[games_count, 'Platform'] = all_td_tags[games_tag].img.get('alt')
        games_tag += 1
        df.loc[games_count, 'Publisher'] = all_td_tags[games_tag].get_text().strip()
        games_tag += 1
        df.loc[games_count, 'Developer'] = all_td_tags[games_tag].get_text().strip()
        games_tag += 1
        df.loc[games_count, 'VGChartz_Score'] = all_td_tags[games_tag].get_text().strip()
        games_tag += 1
        df.loc[games_count, 'Critic_score'] = float(
            all_td_tags[games_tag].string) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'User_Score'] = float(
            all_td_tags[games_tag].string) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'Total_Shipped'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'Global_Sales'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'NA_Sales'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'PAL_Sales'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'JP_Sales'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        df.loc[games_count, 'Other_Sales'] = float(
            all_td_tags[games_tag].string[:-1]) if not all_td_tags[games_tag].string.startswith("N/A") else np.nan
        games_tag += 1
        year = all_td_tags[games_tag].string.split()[-1]
        if year.startswith('N/A'):
            games.loc[games_count, "Year"] = 'N/A'
        else:
            if int(year) >= 70:
                year_to_add = np.int32("19" + year)
            else:
                year_to_add = np.int32("20" + year)
            df.loc[games_count, "Year"] = year_to_add
        games_tag += 1
        df.loc[games_count, 'Last_Update'] = all_td_tags[games_tag].get_text().strip()
        games_count += 1
        games_tag += 1

    value_status = []
    for i in range(len(df)):
        value_status.append('N/A')
    df['Status'] = value_status
def addinfo(df, proxy_origin, value):
    global response
    games_count2 = value
    proxy_pool = cycle(proxy_origin)
    proxy = next(proxy_pool)

    while True:
        time.sleep(1)
        try:
            response = requests.get(df.loc[games_count2, 'Url'], proxies={'http': proxy, 'https': proxy})
            time.sleep(1)
            if str(response) == "<Response [200]>":
                print('Connection established with VGChartz')

                sub_soup = BeautifulSoup(response.text, "html.parser")
                gameBox = sub_soup.find("div", {"id": "gameGenInfoBox"})
                headers = sub_soup.find("div", {"id": "gameGenInfoBox"}).findAll("h2")

                if headers[0].string == 'Ratings':
                    game_rating = gameBox.find('img').get('src')
                    if 'esrb' in game_rating:
                        df.loc[games_count2, 'ESRB'] = game_rating.split('_')[1].split('.')[0].upper()
                    if 'esrb' not in game_rating:
                        df.loc[games_count2, 'ESRB'] = 'N/A'
                elif headers[0].string != 'Ratings':
                    df.loc[games_count2, 'ESRB'] = 'N/A'

                if str(df.loc[games_count2, 'ESRB']) == 'N/A':
                    df.loc[games_count2, 'Status'] = 0
                elif str(df.loc[games_count2, 'ESRB']) != 'N/A':
                    df.loc[games_count2, 'Status'] = 1

                for h2 in headers:
                    if h2.string == "Genre":
                        genre_tag = h2
                        df.loc[games_count2, 'Genre'] = genre_tag.next_sibling.string
                        break
                    elif h2.string != "Genre":
                        df.loc[games_count2, 'Genre'] = 'N/A'

                if value == 0:
                    release_date = range(0, len(df))
                    gamescol.append("Release Date")
                    df["Release Date"] = release_date

                for h2 in headers:
                    if h2.string == "Release Dates" or h2.string == "Release Date":
                        date_tag = h2
                        df.loc[games_count2, "Release Date"] = date_tag.next_sibling.a.string
                        break
                    elif h2.string != "Release Dates":
                        df.loc[games_count2, "Release Date"] = 'N/A'
                headers = []

            break

        except:
            print("Skipping. Connnection error. Proxy: ", proxy)
            proxy = next(proxy_pool)
def run_game(df):
    global counter
    for i in df:
        proxies = get_proxies(10)
        print(proxies)
        addinfo(games, proxies, i)
        print('Saved game data of -> ' + str(i + 1))
        print(games.loc[i])
        counter = i
def respawn(df, proxy_origin, value):
    global response
    proxy_pool = cycle(proxy_origin)
    proxy = next(proxy_pool)

    while True:
        time.sleep(1)
        try:
            response = requests.get(df.loc[value, 'Url'], proxies={'http': proxy, 'https': proxy})
            time.sleep(1)
            if str(response) == "<Response [200]>":
                print('Connection established with VGChartz')

                sub_soup = BeautifulSoup(response.text, "html.parser")
                gameBox = sub_soup.find("div", {"id": "gameGenInfoBox"})
                headers = sub_soup.find("div", {"id": "gameGenInfoBox"}).findAll("h2")

                if headers[0].string == 'Ratings':
                    game_rating = gameBox.find('img').get('src')
                    if 'esrb' in game_rating:
                        df.loc[value, 'ESRB'] = game_rating.split('_')[1].split('.')[0].upper()
                    if 'esrb' not in game_rating:
                        df.loc[value, 'ESRB'] = 'N/A'
                elif headers[0].string != 'Ratings':
                    df.loc[value, 'ESRB'] = 'N/A'

                if str(df.loc[value, 'ESRB']) == 'N/A':
                    df.loc[value, 'Status'] = 0
                elif str(df.loc[value, 'ESRB']) != 'N/A':
                    df.loc[value, 'Status'] = 1

                for h2 in headers:
                    if h2.string == "Genre":
                        genre_tag = h2
                        df.loc[value, 'Genre'] = genre_tag.next_sibling.string
                        break
                    elif h2.string != "Genre":
                        df.loc[value, 'Genre'] = 'N/A'

                if value == 0:
                    release_date = range(0, len (df))
                    gamescol.append("Release Date")
                    df["Release Date"] = release_date

                for h2 in headers:
                    if h2.string == "Release Dates" or h2.string == "Release Date":
                        date_tag = h2
                        df.loc[value, "Release Date"] = date_tag.next_sibling.a.string
                        break
                    elif h2.string != "Release Dates":
                        df.loc[value, "Release Date"] = 'N/A'
                headers = []

            break

        except:
            print("Skipping. Connnection error. Proxy: ", proxy)
            proxy = next(proxy_pool)
def load_savefile(df):
    for i in df:
        if games.loc[i, 'Status'] == 1 or games.loc[i, 'Status'] == 0:
            break
        elif games.loc[i, 'Status'] == 'N/A':
            proxies = get_proxies(10)
            print(proxies)
            respawn(games, proxies, counter)
            print('Saved game data of -> ' + str(counter + 1))
            print(games.loc[counter])
            counter += 1
def save_game(df, name):
    print("Do you wish to save your game? (Y/N): ")
    respuesta = input()

    if respuesta == "Y" or respuesta == "y" or respuesta == "Yes" or respuesta == "yes":
        filename = datetime.now().strftime(name + '-%Y-%m-%d-%H-%M.csv')
        df[gamescol[0:12] + gamescol[17:22]].to_csv(filename, sep=",", encoding='utf-8', index=False)
        print('Saved game to savefile: ' + filename)
    elif respuesta == "N" or respuesta == "n" or respuesta == "No" or respuesta == "no":
        print("Game wasn't saved")

proxies = get_proxies(10)
print(proxies)

game = []
games_total = [i for i in range(15)]
gamescol = ['Rank', 'Name', 'basename', 'Genre', 'ESRB', 'Platform', 'Publisher',
                                    'Developer', 'VGChartz_Score', 'Critic_score', 'User_Score',
                                    'Total_Shipped', 'Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales',
                                    'Other_Sales', 'Year', 'Last_Update', 'Url', 'Status']
games = pd.DataFrame(game, columns=gamescol)

parse_url('http://www.vgchartz.com/gamedb/games.php?name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre=&boxart=Both&banner=Both&ownership=Both&showmultiplat=No&results=50&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&shownasales=1&showdeveloper=0&showdeveloper=1&showcriticscore=0&showcriticscore=1&showpalsales=0&showpalsales=1&showreleasedate=0&showreleasedate=1&showuserscore=0&showuserscore=1&showjapansales=0&showjapansales=1&showlastupdate=0&showlastupdate=1&showothersales=0&showothersales=1&showshipped=0&showshipped=1', proxies)
set_df(games)
run_game(games_total)

#load_savefile(games_total)

save_game(games, 'complete_vgchartz')



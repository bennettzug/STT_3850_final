import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv
import re
import time

#11 07 2022 to 03 12 2023
days_dict = {11: 30, 12:31, 1:31, 2:28, 3:12}

@dataclass
class Game:
    winner: str
    loser: str
    id: str
    url: str
    date: str

def get_html(month, day, year):
    url = f"https://www.sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}"
    resp = httpx.get(url)
    return HTMLParser(resp.text)

def parse_games(html, starting_id, month, day, year):
    games = html.css(".teams")
    results = []
    id = starting_id
    # Iterate through the elements
    def remove_parenthetical_numbers(input_string):
        return re.sub(r'\(\d+\)', '', input_string)

    for game in games:
        
        try:
            url = f"https://www.sports-reference.com{game.css_first('.right.gamelink').css_first('a').attrs['href']}"
        except: 
            print("error getting url")
            
        try:
            loser = game.css_first("tr.loser").css_first('td').text(strip=True)
        except:
            print("error getting loser")

        try:
            winner = game.css_first("tr.winner").css_first('td').text(strip=True)
        except:
            print("error getting winner")
        try:
            gametype = game.css("tr")[2].css_first('.desc').text(strip=True)
        except:
            print("error getting gametype")
        try:
            date = f"{year}-{month:02}-{day:02}"
        except:
            print("error getting gametype")
        if gametype == "Men's":

            new_game = Game(
                winner = remove_parenthetical_numbers(winner),
                loser = remove_parenthetical_numbers(loser),
                id = id,
                url = url,
                date=date
            )
            results.append(asdict(new_game))
            id += 1
    
    return results, id


def get_all_dates():
    pages_accessed=0
    
    all_games = []
    starting_id = 0
    for month in range(11,13):
        for day in range(1,days_dict[month]+1):
            html = get_html(month,day,2022)
            results, starting_id = parse_games(html,starting_id,month,day,2022)
            all_games += results
            print(f'Grabbed data for 2022-{month:02}-{day:02}. New starting id is {starting_id}')
            pages_accessed += 1
            if pages_accessed % 19 == 0:
                
                time.sleep(60)
                
            with open('games.csv', 'a') as f:
                writer= csv.DictWriter(f, fieldnames=["winner", "loser", "id", "url", "date"])
                writer.writerows(results)

    for month in range(1,4):
        for day in range(1,days_dict[month]+1):
            html = get_html(month,day,2023)
            results, starting_id = parse_games(html,starting_id,month,day,2023)
            all_games += results
            print(f'Grabbed data for 2023-{month:02}-{day:02}. New starting id is {starting_id}')
            pages_accessed += 1
            if pages_accessed % 19 == 0:
                time.sleep(60)
            with open('games.csv', 'a') as f:
                writer= csv.DictWriter(f, fieldnames=["winner", "loser", "id", "url", "date"])
                writer.writerows(results)
    return all_games

def to_csv(games_list):
    with open("games2.csv", "w") as f:
        writer= csv.DictWriter(f, fieldnames=["winner", "loser", "id", "url", "date"])
        writer.writerows(games_list)

def main():
    starting_id = 0
    all_games = get_all_dates()
    to_csv(all_games)
    # html = get_html(11,17,2022)
    # results, id = parse_games(html, starting_id,11,17,2022)
    # print(results)
    # print(id)

if __name__ == "__main__":
    main()
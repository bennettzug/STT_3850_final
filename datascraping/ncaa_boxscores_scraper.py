import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv
import re
import time
import random
import math

def get_html(url):
    resp = httpx.get(url)
    return HTMLParser(resp.text)

def make_dict(basic_table, adv_table):
    dict = {}
    tfoot_basic = basic_table.css_first('tfoot')
    td_elements_basic = tfoot_basic.css('td.right')
    
    for td in td_elements_basic:
        dict[td.attrs['data-stat']] = td.text()

    tfoot_adv = adv_table.css_first('tfoot')
    td_elements_adv = tfoot_adv.css('td.right')           
    for td in td_elements_adv:
        dict[td.attrs['data-stat']] = td.text()
    try:
        del dict['bpm']
    except KeyError:
        pass
    # dict = {k:float(v) for (k,v) in dict.items()} 
    return dict


def parse_game(html):
    away_basic_table = html.css(".sortable.stats_table")[0]
    away_adv_table = html.css(".sortable.stats_table")[1]
    home_basic_table = html.css(".sortable.stats_table")[2]
    home_adv_table = html.css(".sortable.stats_table")[3]


    away_dict = make_dict(away_basic_table, away_adv_table)
    home_dict = make_dict(home_basic_table, home_adv_table)

    if int(away_dict['pts']) > int(home_dict['pts']):
        winner_dict = away_dict
        loser_dict = home_dict
        
    else:
        winner_dict = home_dict

        loser_dict = away_dict
    winner_dict = {"w_" + k:v for (k,v) in winner_dict.items()}
    loser_dict = {"l_" + k:v for (k,v) in loser_dict.items()}
    bothteams_dict = winner_dict | loser_dict
    return bothteams_dict

def write_all_boxscores(input_file, output_file):
    
    header_list = ['winner', 'loser', 'game_id', 'w_mp', 'w_fg', 'w_fga', 'w_fg_pct', 'w_fg2', 'w_fg2a', 'w_fg2_pct', 'w_fg3', 'w_fg3a', 'w_fg3_pct', 'w_ft', 'w_fta', 'w_ft_pct', 'w_orb', 'w_drb', 'w_trb', 'w_ast', 'w_stl', 'w_blk', 'w_tov', 'w_pf', 'w_pts', 'w_ts_pct', 'w_efg_pct', 'w_fg3a_per_fga_pct', 'w_fta_per_fga_pct', 'w_orb_pct', 'w_drb_pct', 'w_trb_pct', 'w_ast_pct', 'w_stl_pct', 'w_blk_pct', 'w_tov_pct', 'w_usg_pct', 'w_off_rtg', 'w_def_rtg', 'l_mp', 'l_fg', 'l_fga', 'l_fg_pct', 'l_fg2', 'l_fg2a', 'l_fg2_pct', 'l_fg3', 'l_fg3a', 'l_fg3_pct', 'l_ft', 'l_fta', 'l_ft_pct', 'l_orb', 'l_drb', 'l_trb', 'l_ast', 'l_stl', 'l_blk', 'l_tov', 'l_pf', 'l_pts', 'l_ts_pct', 'l_efg_pct', 'l_fg3a_per_fga_pct', 'l_fta_per_fga_pct', 'l_orb_pct', 'l_drb_pct', 'l_trb_pct', 'l_ast_pct', 'l_stl_pct', 'l_blk_pct', 'l_tov_pct', 'l_usg_pct', 'l_off_rtg', 'l_def_rtg']
    with open(output_file, 'w') as ofile:
        dw=csv.DictWriter(ofile,fieldnames=header_list)
        with open(input_file, 'r') as file:
            heading = next(file)
            csv_reader = csv.reader(file)
            dw.writeheader()
            for row in csv_reader:
                html = get_html(row[3])
                try:
                    bothteams_dict = parse_game(html)
                except IndexError:
                    print("Oops! Saw too many pages! Waiting 1 hour.")
                    time.sleep(3600)
                bothteams_dict["winner"] = row[0]
                bothteams_dict["loser"] = row[1]
                bothteams_dict['game_id'] = row[2]
                dw.writerow(bothteams_dict)
                print(f"added game {row[2]} to file.")
                time.sleep((random.random())+5)
                


def main():
    write_all_boxscores('games2.csv','boxscores.csv')


if __name__ == "__main__":
    main()
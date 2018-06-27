import re
import csv
import sys
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Process
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def pitching(file):
    url = "https://www.baseball-reference.com/leagues/MLB/2018-standard-pitching.shtml"
    f = open(file, "w")
    headers = ["name", "age", "wins", "losses", "pct", "era", "saves", "ip", "hits", "runs", "er", "hr", "bb", "ibb",
               "so", "era+", "fip", "whip", "h9", "hr9", "bb9", "so9", "so/w\n"]
    row = ','.join(headers)
    f.write(row)
    r = requests.get(url)
    soup = BeautifulSoup(re.sub("<!--|-->", "", r.text), "lxml")

    tables = soup.find_all('table')
    table = tables[1]
    pa = pn = ""
    for tr in table.select('tr'):
        cells = tr.find_all('td')
        if len(cells) > 0:
            name = cells[0].text.strip("*")
            age = cells[1].text.strip() if cells[1].text else "0"
            wins = cells[4].text.strip() if cells[4].text else "0"
            losses = cells[5].text.strip() if cells[5].text else "0"
            pct = cells[6].text.strip() if cells[6].text else "0"
            era = cells[7].text.strip() if cells[7].text else "0"
            saves = cells[13].text.strip() if cells[13].text else "0"
            ip = cells[14].text.strip() if cells[14].text else "0"
            hits = cells[15].text.strip() if cells[15].text else "0"
            runs = cells[16].text.strip() if cells[16].text else "0"
            er = cells[17].text.strip() if cells[17].text else "0"
            hr = cells[18].text.strip() if cells[18].text else "0"
            bb = cells[19].text.strip() if cells[19].text else "0"
            ibb = cells[20].text.strip() if cells[20].text else "0"
            so = cells[21].text.strip() if cells[21].text else "0"
            erap = cells[26].text.strip() if cells[26].text else "0"
            fip = cells[27].text.strip() if cells[27].text else "0"
            whip = cells[28].text.strip() if cells[28].text else "0"
            h9 = cells[29].text.strip() if cells[29].text else "0"
            hr9 = cells[30].text.strip() if cells[30].text else "0"
            bb9 = cells[31].text.strip() if cells[31].text else "0"
            so9 = cells[32].text.strip() if cells[32].text else "0"
            sow = cells[33].text.strip() if cells[33].text else "0"

            current = ",".join([name, age, wins,losses,pct,era,saves,ip,hits,runs,er,hr,bb,ibb,so,erap,fip,whip,
                                h9,hr9,bb9,so9,sow + "\n"])

            cn = name
            ca = age

            if cn == pn and ca == pa:
                pass
            else:
                f.write(current)
                pn = cn
                pa = ca

    f.close()
    fix(file)


def team_batting(file):
    url = "https://www.baseball-reference.com/leagues/MLB/2018.shtml"
    f = open(file, "w")
    headers = ["Team", "#Players", "Average Age", "R/G", "Games", "PA", "AB", "R", "H", "2B", "3B",
               "HR", "RBI", "SB", "CS", "BB", "SO", "BA", "OBP", "SLG", "OPS", "OPS+", "TB", "GDP",
               "HBP", "SH", "SF", "IBB", "LOB\n"]
    teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", "HOU", "KCR", "LAA", "LAD", "MIA","MIL","MIN","NYM","NYY","OAK","PHI",
             "PIT", "SDP","SEA","SFG","STL","TBR","TEX","TOR","WSN"]
    row = ",".join(headers)
    f.write(row)
    r = requests.get(url)
    soup = BeautifulSoup(re.sub("<!--|-->", "", r.text), "lxml")

    soup.prettify()
    tables = soup.find_all('table')
    standard_batting = tables[0]
    for tr in standard_batting.select('tr'):
        cells = tr.find_all('td')
        if len(cells) > 0:
            num_batters = cells[0].text.strip()
            bat_age = cells[1].text.strip()
            rpg = cells[2].text.strip()
            games = cells[3].text.strip()
            pa = cells[4].text.strip()
            ab = cells[5].text.strip()
            r = cells[6].text.strip()
            h = cells[7].text.strip()
            b2 = cells[8].text.strip()
            b3 = cells[9].text.strip()
            hr = cells[10].text.strip()
            rbi = cells[11].text.strip()
            sb = cells[12].text.strip()
            cs = cells[13].text.strip()
            bb = cells[14].text.strip()
            so = cells[15].text.strip()
            ba = cells[16].text.strip()
            obp = cells[17].text.strip()
            slg = cells[18].text.strip()
            ops = cells[19].text.strip()
            opsp = cells[20].text.strip()
            tb = cells[21].text.strip()
            gdp = cells[22].text.strip()
            hbp = cells[23].text.strip()
            sh = cells[24].text.strip()
            sf = cells[25].text.strip()
            ibb = cells[26].text.strip()
            lob = cells[27].text.strip()

            c_team = teams[0]
            current = ",".join[c_team,num_batters,bat_age, rpg, games, pa, ab, r, h,b2,b3,hr,rbi,sb,cs,bb,so,ba,obp,slg,ops,opsp,tb,gdp,hbp,sh,sf,ibb,lob + "\n"]
            del teams[0]
            f.write(current)


def team_pitching(file):
    url = "https://www.baseball-reference.com/leagues/MLB/2018.shtml"
    f = open(file, "w")
    headers = ["Team", "#Pitchers", "Average Age", "RA/G", "W", "L", "W-L%", "ERA", "G", "GS", "GF",
               "CG", "tSho", "cSho", "SV", "IP", "H", "R", "ER", "HR", "BB", "IBB", "SO", "HBP",
               "BK", "WP", "BF", "ERA+", "FIP", "WHIP", "H9", "HR9", "BB9", "SO9", "SO/W", "LOB\n"]
    teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", "HOU", "KCR", "LAA", "LAD", "MIA",
             "MIL", "MIN", "NYM", "NYY", "OAK", "PHI",
             "PIT", "SDP", "SEA", "SFG", "STL", "TBR", "TEX", "TOR", "WSN"]
    row = ",".join(headers)
    f.write(row)
    r = requests.get(url)
    soup = BeautifulSoup(re.sub("<!--|-->", "", r.text), "lxml")

    soup.prettify()
    tables = soup.find_all('table')
    standard_pitching = tables[1]
    for tr in standard_pitching.select('tr'):
        cells = tr.find_all('td')
        if len(cells) > 0:
            print(cells)
            num_batters = cells[0].text.strip()
            bat_age = cells[1].text.strip()
            rpg = cells[2].text.strip()
            win = cells[3].text.strip()
            loss = cells[4].text.strip()
            wlp = cells[5].text.strip()
            era = cells[6].text.strip()
            g = cells[7].text.strip()
            gs = cells[8].text.strip()
            gf = cells[9].text.strip()
            cg = cells[10].text.strip()
            tsho = cells[11].text.strip()
            csho = cells[12].text.strip()
            sv = cells[13].text.strip()
            ip = cells[14].text.strip()
            h = cells[15].text.strip()
            r = cells[16].text.strip()
            er = cells[17].text.strip()
            hr = cells[18].text.strip()
            bb = cells[19].text.strip()
            ibb = cells[20].text.strip()
            so = cells[21].text.strip()
            hbp = cells[22].text.strip()
            bk = cells[23].text.strip()
            wp = cells[24].text.strip()
            bf = cells[25].text.strip()
            erap = cells[26].text.strip()
            fip = cells[27].text.strip()
            whip = cells[28].text.strip()
            h9 = cells[29].text.strip()
            hr9 = cells[30].text.strip()
            bb9 = cells[31].text.strip()
            so9 = cells[32].text.strip()
            sow = cells[33].text.strip()
            lob = cells[34].text.strip()

            c_team = teams[0]
            current = ",".join[c_team, num_batters, bat_age, rpg, win, loss, wlp, era, g, gs, gf, cg, tsho, csho, sv, ip, h, r,er,hr,bb,ibb,so,hbp,bk,wp,bf,erap,fip,
                               whip,h9,hr9,bb9,so9,sow,lob + "\n"]
            del teams[0]
            f.write(current)


def team_fielding(file):
    pass

def batting(file):
    url = "https://www.baseball-reference.com/leagues/MLB/2018-standard-batting.shtml"
    f = open(file, "w")
    headers = ["name", "age", "games", "plate appearance", "at bat", "runs", "hits", "doubles", "triples", "home runs", "RBI",
               "stolen bases", "walks", "strikeouts", "hits/at bat", "on base pct", "slug pct", "ops\n"]
    row = ",".join(headers)
    f.write(row)
    r = requests.get(url)
    soup = BeautifulSoup(re.sub("<!--|-->", "", r.text), "lxml")

    soup.prettify()
    tables = soup.find_all('table')
    table = tables[1]
    pa = pn = ""
    for tr in table.select('tr'):
        cells = tr.find_all('td')
        if len(cells) > 0:
            name = cells[0].text.strip("*#")
            age = cells[1].text.strip() if cells[1].text else "0"
            games = cells[4].text.strip() if cells[4].text else "0"
            pa = cells[5].text.strip() if cells[5].text else "0"
            ab = cells[6].text.strip() if cells[6].text else "0"
            runs = cells[7].text.strip() if cells[7].text else "0"
            hits = cells[8].text.strip() if cells[8].text else "0"
            doubles = cells[9].text.strip() if cells[9].text else "0"
            triples = cells[10].text.strip() if cells[10].text else "0"
            hr = cells[11].text.strip() if cells[11].text else "0"
            rbi = cells[12].text.strip() if cells[12].text else "0"
            sb = cells[13].text.strip() if cells[13].text else "0"
            walks = cells[15].text.strip() if cells[15].text else "0"
            strike = cells[16].text.strip() if cells[16].text else "0"
            pct = cells[17].text.strip() if cells[17].text else "0"
            obp = cells[18].text.strip() if cells[18].text else "0"
            slug = cells[19].text.strip() if cells[19].text else "0"
            ops = cells[20].text.strip() if cells[20].text else "0"

            current = ",".join([name, age, games, pa, ab, runs, hits, doubles, triples, hr, rbi, sb, walks, strike, pct,
                                obp, slug, ops + "\n"])

            cn = name
            ca = age

            if cn == pn and ca == pa:
                pass
            else:
                f.write(current)
                pn = cn
                pa = ca
    f.close()
    fix(file)


def fix(file):
    read = open(file)
    lines = read.readlines()
    read.close()
    w = open(file, "w")
    w.writelines([line for line in lines[:-1]])
    w.close()


def git_add(file):
    subprocess.call(["git", "add", file])


def git_commit(message):
    subprocess.call(["git", "commit", "-m", "baseball"])


def git_push():
    subprocess.call(["git", "push", "origin", "master"])
    subprocess.call(["git", "push", "lab", "master"])


if __name__ == "__main__":
    start = datetime.now()

    p1 = Process(target=batting, args=("batting.csv",))
    p1.start()
    p2 = Process(target=pitching, args=("pitching.csv",))
    p2.start()
    #p3 = Process(target=team_batting, args=("team_batting.csv"))
    #p3.start()
    #p4 = Process(target=team_pitching, args=("team_pitching.csv"))
    #p4.start()

    p1.join()
    p2.join()
    #p3.join()
    #p4.join()
    team_batting("team_batting.csv")
    team_pitching("team_pitching.csv")
    
    today = datetime.strftime(datetime.now(), '%Y-%m-%d \t %H:%M')

    total = datetime.now() - start
    with open("log.txt", 'a') as f:
        f.write(today + " - " + str(total) + "\n")

    git_add("log.txt")
    git_add("batting.csv")
    git_add("pitching.csv")
    git_add("team_batting.csv")
    git_add("team_pitching.csv")
    git_commit("baseball")
    git_push()

    sys.exit(0)

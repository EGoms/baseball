import re
import csv
import sys
import requests
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

def team_batting():
    url = "https://www.baseball-reference.com/leagues/MLB/2018.shtml"
    #f = open(file, "w")
    headers = ["Team", "#Players", "Average Age", "R/G", "Games", "PA", "AB", "R", "H", "2B", "3B",
               "HR", "RBI", "SB", "CS", "BB", "SO", "BA", "OBP", "SLG", "OPS", "OPS+", "TB", "GDP",
               "HBP", "SH", "SF", "IBB", "LOB\n"]
    row = ",".join(headers)
    #f.write(row)
    r = requests.get(url)
    soup = BeautifulSoup(re.sub("<!--|-->", "", r.text), "lxml")

    soup.prettify()
    tables = soup.find_all('table')
    table = tables[0]
    for tr in table.select('tr'):
        cells = tr.find_all('td')
        teams = tr.find_all('th')
        print(teams)
        if len(cells) > 0:
            team_name = cells[0].text.strip()
            #print(cells)

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


if __name__ == "__main__":
    start = datetime.now()

    p1 = Process(target=batting, args=("batting.csv",))
    p1.start()
    p2 = Process(target=pitching, args=("pitching.csv",))
    p2.start()

    p1.join()
    p2.join()

    today = datetime.strftime(datetime.now(), '%Y-%m-%d \t %H:%M')

    total = datetime.now() - start
    with open("log.txt", 'a') as f:
        f.write(today + " - " + str(total) + "\n")

    git_add("log.txt")
    git_add("batting.csv")
    git_add("pitching.csv")
    git_commit("baseball")
    git_push()

    sys.exit(0)

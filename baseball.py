import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
from datetime import datetime
import subprocess
from tempfile import mkstemp
from shutil import move
import re
import csv
import sys
from os import fdopen, remove
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
            age = cells[1].text.strip()
            wins = cells[4].text.strip()
            losses = cells[5].text.strip()
            pct = cells[6].text.strip()
            era = cells[7].text.strip()
            saves = cells[13].text.strip()
            ip = cells[14].text.strip()
            hits = cells[15].text.strip()
            runs = cells[16].text.strip()
            er = cells[17].text.strip()
            hr = cells[18].text.strip()
            bb = cells[19].text.strip()
            ibb = cells[20].text.strip()
            so = cells[21].text.strip()
            erap = cells[26].text.strip()
            fip = cells[27].text.strip()
            whip = cells[28].text.strip()
            h9 = cells[29].text.strip()
            hr9 = cells[30].text.strip()
            bb9 = cells[31].text.strip()
            so9 = cells[32].text.strip()
            sow = cells[33].text.strip()

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
    git_add(file)
def batting(file):
    url = "https://www.baseball-reference.com/leagues/MLB/2018-standard-batting.shtml"
    f = open(file, "w")
    headers = ["name", "age", "games", "plate appearance", "at bat", "runs", "hits", "doubles", "triples", "home runes", "RBI",
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
            age = cells[1].text.strip()
            games = cells[4].text.strip()
            pa = cells[5].text.strip()
            ab = cells[6].text.strip()
            runs = cells[7].text.strip()
            hits = cells[8].text.strip()
            doubles = cells[9].text.strip()
            triples = cells[10].text.strip()
            hr = cells[11].text.strip()
            rbi = cells[12].text.strip()
            sb = cells[13].text.strip()
            walks = cells[15].text.strip()
            strike = cells[16].text.strip()
            pct = cells[17].text.strip()
            obp = cells[18].text.strip()
            slug = cells[19].text.strip()
            ops = cells[20].text.strip()

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
    git_add(file)


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
    subprocess.call(["git", "commit", "-m", message])


def git_push():
    subprocess.call(["git", "push", "origin", "master"])


if __name__ == "__main__":
    batting("baseball.csv")
    pitching("pitching.csv")
    git_commit("baseball")
    git_push()

    sys.exit(0)
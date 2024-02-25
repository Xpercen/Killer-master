import pygetwindow as gw
import time
from datetime import datetime, timedelta
import os
import sqlite3
import csv
import requests
from bs4 import BeautifulSoup
import shutil
import json
current_directory = os.getcwd()
user_profile = os.environ['USERPROFILE']
copyhis = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
msedge_chemin = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'FBHistory')

with open("config.json","r") as j:
    data = json.load(j)
    gametag = data["gametag"]
    bilibili_tag = data["bilibili_tag"]
    timewait = data["timewait"]
    deltatime = data["deltatime"]


delta = timedelta(seconds=deltatime)
def dohis():
    shutil.copy(copyhis, msedge_chemin)
    
    new_time = datetime.now() - delta
    formatted_time = new_time.strftime("%Y%m%d%H%M%S")

    with sqlite3.connect(msedge_chemin) as conn:
        curseur = conn.cursor()
        curseur.execute("SELECT REPLACE(urls.url, ',', ' '), REPLACE(title, ',', ' '), " \
                    "strftime('%Y%m%d%H%M%S', (visit_time/1000000) - 11644473600, 'unixepoch', 'localtime')" \
                    " FROM urls, visits WHERE visits.url = urls.id ORDER BY visit_time DESC LIMIT 30")
    resultat = curseur.fetchall()
    resultat = [row for row in resultat if row[2] >= formatted_time]
    seen = set()
    resultat = [row for row in resultat if row[1] not in seen and not seen.add(row[1])]
    resultat = [(row[0].split('?')[0], row[1], row[2]) for row in resultat]

    for row in resultat:
        video_url = row[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        response = requests.get(video_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        tag_links = soup.find_all('a', class_='tag-link')# 找到所有class为"tag-link"的<a>标签
        tags = [tag.text for tag in tag_links]
        for i in bilibili_tag:
            for l in tags:
                if i in l:
                    killlist.append(row[1])


    
    kill()


def kill():
    for i in killlist:
        print(i)
        w = gw.getWindowsWithTitle(i)
        try:
            w[0].close()
        except:
            print(0)
        time.sleep(0.1)

def check_window():
    title = gw.getAllTitles()
    for tt in title:
        for rr in gametag:
            if rr in tt:
                killlist.append(tt)
    dohis()

while True:
    killlist=[]
    check_window()
    time.sleep(timewait)
    


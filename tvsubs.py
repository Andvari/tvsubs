
"""
author: nemo
date: 23.10.2017
"""

import re
import urllib.request
import zipfile
import io


f = urllib.request.urlopen("http://www.tvsubs.ru/tvshow-48-1.html")
page = f.read().decode('utf-8')
a = page[page.find("\"cont\""): page.find("\"clear\"")]
seasons = a.count('|') + 1
print("Seasons: ", seasons)

for season in range(seasons):
    print("Season: ", season+1)
    f = urllib.request.urlopen("http://www.tvsubs.ru/tvshow-48-" + str(season+1)+".html")
    page = f.read().decode('utf-8')
    a = page[page.find("\"cont\""): page.find("\"clear\"")]
    episodes = re.compile("</span>.+?<span").findall(a)
    print("Episodes: ", len(episodes))
    ne = 0
    for episode in episodes:
        ne += 1
        print("Episode:",  ne)
        e = episode[episode.find("epi"): episode.find(".html")]

        f = urllib.request.urlopen("http://www.tvsubs.ru/" + e + "-en.html")
        page = f.read().decode('utf-8')
        a = page[page.find("\"cont\""): page.find("\"clear\"")]
        b = a[a.find("<li>"):]
        b = b[:b.rfind("</ul>")]

        ss = re.compile("<li>.+?</li>").findall(b)
        print("Subtitles: ", len(ss))
        for s in ss:
            namelink = s[s.rfind("subtitle"): ]
            namelink = namelink[: namelink.find(".html")+5]
            rating = str(s.count("rating1")*2 + s.count("rating2"))
            dd = s[s.find("</span>")+8:]
            downloads = dd[dd.find(">")+1: dd.find("<")]
            nl = urllib.request.urlopen("http://tvsubs.ru/" + namelink)
            page = nl.read().decode("utf-8")
            a = page[page.find("\"cont\""): page.find("\"clear\"")]
            print(a)
            fname = re.compile("<li>.+?</li>").findall(a)[1]
            fname = fname[fname.find("div>")+4: -12].lstrip(" ")
            print("Name: %s\nRating: %s\nDownloads: %s" % (fname, rating, downloads))
            url = "http://tvsubs.ru/files/"+fname+".en.zip"
            print(url)
            f = urllib.request.urlopen(url)
            zipped = zipfile.ZipFile(io.BytesIO(f.read()))
            ext = zipped.namelist()[0][zipped.namelist()[0].rfind("."):]
            s = open(fname+"-"+rating+"-"+downloads+ext, "wb")
            s.write(zipped.read(zipped.namelist()[0]))
            s.close()


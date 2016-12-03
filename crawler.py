import urllib.request as ur
from bs4 import BeautifulSoup
import time
import sys

inp = open("Database/thousand_names.txt",'r')
names = inp.read().splitlines()

def getURL(page):

    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def give_list(name,ans):
    main = 'https://en.wikipedia.org' + name
    try:
        html = ur.urlopen(main).read()
        soup = BeautifulSoup(html)
        page = str(soup)
    except(KeyboardInterrupt, SystemExit):
        raise
    except:
        e = sys.exc_info()[0]
        print(e)
        return
    ans.write("#######\n")

    while True:
        url, n = getURL(page)
        page = page[n:]
        if url:
            for name in names:
                if ((name) == url):
                    ans.write(url + "\n")
        else:
            break

    ans.write("#######\n")
    
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    ans.write(text)


print("crawling webpages in the database...")

i=0;
for name in names:
    i+=1; print(i)
    name_edit = name.replace('/','-')
    ans = open("Database/"+name_edit + ".txt","w")
    
    give_list(name,ans)
    time.sleep(3)


import requests
import bs4
import sys


def findNoAlts(url):
    """
    findNoAlts(string url)
    Find all <img> tags containing no alt attribute at "url"
    Return list of tags
    """
    site = requests.get(url, verify=False)
    if sitemap.status_code != 200:
        f.write("\n!! {} is not accessible\n".format(cur_url))
        return
    bs = bs4.BeautifulSoup(site.text, "html.parser")
    images = bs.findAll("img", {'alt': False})
    return images


def fillFile(f, cur_url):
    """
    fillFile(fileobj f, string cur_url)
    Write <img> tags with no alt at "cur_url" into "f"
    Return None
    """
    global count
    if cur_url[-4:] == '.xml':
        print("inner sitemap '{}' researched ...".format(cur_url))
        sitemap = requests.get(cur_url, verify=False)
        if sitemap.status_code != 200:
            f.write("\n!! {} is not accessible\n".format(cur_url))
            return
        bsMap = bs4.BeautifulSoup(sitemap.text, "html.parser")
        pages = bsMap.findAll("loc")
        for page in pages:
            new_url = page.contents[0]
            fillFile(f, new_url)
    else:
        imgs = findNoAlts(cur_url)
        count += len(imgs)
        if len(imgs) > 0:
            f.write("\n" + cur_url + "\n")
            for img in imgs:
                f.write("\n\t" + str(img) + "\n")


def badURI():
    print("Bad URI. Try another")
    sys.exit()


requests.packages.urllib3.disable_warnings()
sitemap = input("URI of sitemap file: ")
print("processing...")
try:
    sitemap = requests.get(sitemap, verify=False)
except requests.exceptions.MissingSchema:
    badURI()
if sitemap.status_code != 200:
    badURI()
bsMap = bs4.BeautifulSoup(sitemap.text, "html.parser")
pages = bsMap.findAll("loc")
with open("images.txt", 'w') as f:
    count = 0
    for page in pages:
        cur_url = page.contents[0]
        fillFile(f, cur_url)
    f.write("\n{} images without alt founded\n".format(count))

print("Done! See images.txt")

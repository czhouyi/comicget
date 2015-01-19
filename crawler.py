#encoding=utf8
import re, os, urllib

def getChapter(url='http://www.7330.com/op/'):
    ''' return a list of tuples (url, title) which are the links of chapters '''
    html = urllib.urlopen(url).read()
    p = re.compile(r'<a href="(http://.*?)" title=.*?target="_blank">(.*?)</a>')
    return p.findall(html)
    
def getPage(url):
    ''' return a list of tuples (url, pageNo) which are the links of pages '''
    html = urllib.urlopen(url).read()
    p = re.compile(r'<option value="(.*?)".*?>(.*?)</option>')
    l = p.findall(html)
    print '%s======%d Started...' %(url, len(l)/2)
    return l[:len(l)/2]

def getImage(url):
    ''' return a url which is the link of image '''
    html = urllib.urlopen(url).read()
    p = re.compile(r'<img.*?src="(http://pic.*?)".*?</p>')
    return p.findall(html)

def download(url, path):
    ''' download the image from the link to path '''
    urllib.urlretrieve(url, path)

if __name__=='__main__':
    url='http://www.7330.com/op/'
    cs = getChapter(url)
    # open a file to cache the completed chapter links
    f = open('complete.txt', 'a+')
    cd = {}
    cl = map(lambda x: cd.setdefault(x.replace('\n', ''),1), f.readlines())
    for c in cs:
        if not cd.get(c[0]):
            ps = getPage(c[0])
            path = c[1]
            if not os.path.exists(path):
                os.mkdir(path)
            for p in ps:
                imgurl = getImage('%s%s' % (url, p[0]))
                if imgurl:
                    download(imgurl[0], '%s/%s.png' % (path, p[1]))
            print '%s======%d Completed...' %(c[0], len(ps))
            f.write('\n%s' % (c[0]))
            cd[c[0]] = 1
            f.flush()
    f.close()

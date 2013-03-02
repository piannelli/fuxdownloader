import MySQLdb, sys, urllib2, urlparse, re, time
from bs4 import BeautifulSoup
from time import sleep


class Finder:
  '''
  The class to find the movie url in an HTML from fux.com
  '''
  def __init__(self, url):
    self.url = url
    data = self.get_html(self.url)
    self.movie_url = self._find_movie(data)
    self.movie_title = self._find_movie_title(data)
    
  def get_html(self, url):
    req = urllib2.Request(str(url))
    req.add_header('User-Agent', 'Googlebot-Video/1.0')
    request = None
    status = 0
    try:
      request = urllib2.urlopen(req)
    except urllib2.URLError, e:
      sys.stderr.write("Exception at url: %s\n%s" % (url, e))
      status = e.code
    except urllib2.HTTPError, e:
      status = e.code
    if status == 0:
      status = 200
      
    if status == 200:
      return request.read() 
    return None  
   
  def find_xml_url(self, data):
    search_for = "/players/FuxStream/Configurations/config_"
    search_end = "%26as="
    result = re.search(search_for + '(.*)' + search_end, data)
    if result is None:
      return None
    
    u = urlparse.urlparse(self.url)
    xml_url = u.scheme + '://' + u.netloc + search_for + result.group(1)
    return xml_url
    
  def get_movie_url(self, xml_url):
    xml = self.get_html(xml_url)
    soup = BeautifulSoup(xml)
    streams = soup.find_all('stream')
    movie_url = ''
    for stream in streams:
      movie_url = stream.file.get_text()
      break
    return movie_url
    
  def _find_movie(self, data):
    xml_url = self.find_xml_url(data)
    movie_url = self.get_movie_url(xml_url)
    return movie_url
  
  def _find_movie_title(self, data):
    soup = BeautifulSoup(data)
    return soup.title.string
  
  def find_movie(self):
    return self.movie_url
    
  def find_title(self):
    return self.movie_title
    
class Downloader:
  '''
  The class which downloads the movie from fux.com
  '''
  def __init__(self, url):
    self.url = url
    self.finder = Finder(self.url)
    
  def fetch_url(self, url, ref=None, path=None):
    opener = urllib2.build_opener()
    headers = {}
    if ref:
        headers['Referer'] = ref
    request = urllib2.Request(url, headers=headers)
    handle = urllib2.urlopen(request)
    if not path:
        return handle.read()
    sys.stdout.write('saving: ')
    # write result to file
    with open(path, 'wb') as out:
        while True:
            part = handle.read(65536)
            if not part:
                break
            out.write(part)
            sys.stdout.write('.')
            sys.stdout.flush() 
        sys.stdout.write('\nFinished.\n')
  
  def make_dest(self, title):
    bad_characters = [" ", "/", "\\", ":", "(", ")", "<", ">", "|", "?", "*"]
    filename = title
    for letter in bad_characters:
      filename = filename.replace(letter, "_")
      
    return filename
    
  def download(self):
    movie_url = self.finder.find_movie()
    title = self.finder.find_title()
    if title == '':
      title = str(int(time.time()))
    dest = self.make_dest(title)  
    # download the movie
    self.fetch_url(movie_url, ref = None, path=dest)

def main():
  if len(sys.argv) <= 1:
    print "No url given!"
    sys.exit(1)
    
  url = sys.argv[1]
  downloader = Downloader(url)
  downloader.download()
  
  
if __name__ == '__main__':
  main()


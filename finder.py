import urlparse, urllib2, sys, re
from bs4 import BeautifulSoup

class FuxFinder:
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
    
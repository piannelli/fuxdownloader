import urllib2, sys, time

class Downloader:
  '''
  The class which downloads the movie from fux.com
  '''
  def __init__(self, url, title = ''):
    self.url = url
    self.title = title
  
  def show_progress(self, read_bytes, chunk_size, total_size):
    percent = float(read_bytes) / float(total_size)
    percent = round(percent*100, 2)
    sys.stdout.write("Downloaded %s of %s bytes (%0.2f%%)\r" %  (read_bytes, total_size, percent))
    if read_bytes >= total_size:
      sys.stdout.write('\n')
  
  def fetch_url(self, ref=None, path=None, progress=False):
    chunk_size = 65536
    read_bytes = 0
    url = self.url
    headers = {}
    if ref:
        headers['Referer'] = ref
    request = urllib2.Request(url, headers=headers)
    handle = urllib2.urlopen(request)
    if not path:
        return handle.read()
    total_size = handle.info().getheader('Content-Length').strip()
    # write result to file
    with open(path, 'wb') as out:
        while True:
            part = handle.read(chunk_size)
            read_bytes += len(part)
            if not part:
                break
            out.write(part)
            if progress:
              self.show_progress(read_bytes, chunk_size, total_size)
            sys.stdout.flush() 
        sys.stdout.write('\nFinished.\n')
  
  def make_dest(self, title):
    bad_characters = [" ", "/", "\\", ":", "(", ")", "<", ">", "|", "?", "*"]
    filename = title
    for letter in bad_characters:
      filename = filename.replace(letter, "_")
      
    return filename
    
  def download(self):
    if self.title == '':
      self.title = str(int(time.time()))
    
    dest = self.make_dest(self.title)  
    # download the movie
    self.fetch_url(ref = None, path=dest, progress = True)
    
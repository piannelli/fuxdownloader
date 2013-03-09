import sys
from downloader import Downloader
from finder import FuxFinder

def main():
  if len(sys.argv) <= 1:
    print "No url given!"
    sys.exit(1)
  
  finder = FuxFinder(sys.argv[1])
  downloader = Downloader(finder.find_movie(), finder.find_title() + '.mp4')
  downloader.download()
  
  
if __name__ == '__main__':
  main()


import os
from json import loads
from time import sleep
from random import randrange
from requests import get
from PIL import Image
from io import BytesIO
from ctypes import windll

def go(query = 'moutain', verbose = True):
  """Download full size images from Google image search.

  Don't print or republish images without permission.
  I use this to change desktops randomly
  """
  BASE_URL = 'http://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + '&start=%d'
  #http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=mountains&start=4
  SUCCESSFUL = False
  while not SUCCESSFUL:
    page  = randrange(0,55) # Google's start query string parameter for pagination.
    image = randrange(0,4)  # The image on the page, there's 4 images on each
    if verbose: print('getting image', image, 'on page', page)
    try:
      r = get(BASE_URL % page)
      raise Exception
    except Exception as e:
      if verbose: print("can't connect to the internet", e)
      return False
      
    url = loads(r.text)['responseData']['results'][image]['unescapedUrl']
    try:
      image_r = get(url)
      file = open('wallpaper.jpg', 'w')
      Image.open(BytesIO(image_r.content)).save(file, 'JPEG')
      SUCCESSFUL = True
      
    except ConnectionError as e:
      SUCCESSFUL = False
      if verbose: print('could not download', url, '\n', e)
      # Be nice to Google and they'll be nice back :)
      sleep(1.5)
      
    except IOError as e:
      # Throw away some gifs...blegh.
      SUCCESSFUL = False
      if verbose: print('could not save', url, '\n', e)
      # Be nice to Google and they'll be nice back :)
      sleep(1.5)
      
    except Exception as e:
      SUCCESSFUL = False
      if verbose: print('something unexpected went wrong:\n', e)
      # Be nice to Google and they'll be nice back :)
      sleep(1.5)
      
    finally:
      file.close()
  if verbose: print('k, done')
  return True

if __name__ == '__main__':
  verbose = True
  if go('beach', verbose):

    if verbose: print('setting wallpaper')
    img = os.path.join(os.getcwd(), "wallpaper.jpg")
    result = windll.user32.SystemParametersInfoW(20, 0, img, 1)
    if verbose:
      print('k, done' if result else 'nope')

  else:
    if verbose: print('setting default wallpaper')
    img = os.path.join(os.getcwd(), "default.jpg")
    result = windll.user32.SystemParametersInfoW(20, 0, img, 1)
    if verbose:
      print('k, done' if result else 'nope')
      

import hqqresolver
import httplib
import urlparse

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

# resolved = hqqresolver.resolve('http://netu.tv/player/embed_player.php?vid=6HO81UKM8K85&autoplay=no') #unshorten_url('http://goo.gl/aQfhte')
resolved = hqqresolver.resolve(unshorten_url('http://goo.gl/aQfhte'))
print resolved

# encodedm3u = "Vpw97lXY6GX98oJ9isWGVGkhvGhD6fkYUS0T85kH7CZR6GB8V5iexbwDif8exGJs5bhs5Ehqw57YznwIxbWEgoakVDEnz2Ha4SZdklQdkjEWkj=R6Ghy7snGUGgB7T7Y8fdG6GFRVS0fV5dD7s0GV5wDUuiYij=dkMZdiMZdiCZdklQdiTN9klbR45ynkz=/7G0jVGa9"
# resolveFile = hqqresolver._decode2(encodedm3u.replace('\\', ''))
# print resolveFile

raw_input("press enter to exit")
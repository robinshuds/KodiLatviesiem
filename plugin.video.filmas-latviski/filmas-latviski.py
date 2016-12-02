# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import urllib, urllib2, ssl, re
import CommonFunctions
import requests

mainURL = 'https://cinemalive.tv'

def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
    if txtMessage=='None': txtMessage=''
    keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return False # return ''
		
def Search():
	text = showkeyboard('', u'Meklēt filmu')
	print "Search string: " + text
	post_fields = {'search': text}
	html = postHTML("https://cinemalive.tv/scripts/search.php", post_fields)
	
	print html
	# found_items = common.parseDOM(html, "div", attrs = { "style": "height:78px" })
	found_links = common.parseDOM(html, "a", ret = "href")
	found_name = common.parseDOM(html, "span", attrs = { "style": "color:#bcbcbc" })
	found_image = common.parseDOM(html, "img", ret = "src")
	print found_links
	print found_name
	print found_image
	
	for i in range(0, len(found_links)):
		addDir(found_name[i].encode('utf-8'), found_links[i], 'state_play', found_image[i].replace(mainURL, "").replace('xs.jpg', 'md.jpg') )
		
def postHTML(url, post_fields):

	if sys.hexversion >= 0x02070BF0:
		r = requests.post(url, data=post_fields)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
	else:
		print "Crap we have the old version"
		
		# hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		# 'Accept-Encoding': 'none',
		# 'Accept-Language': 'pl-PL,pl;q=0.8',
		# 'Connection': 'keep-alive'}
		
		# http://dev.morf.lv/mirror.php?url=https://cinemalive.tv/scripts/search.php&post=
		postParam = ""
		for key, value in post_fields.iteritems():
			postParam+=key+":"+value
			
		# req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url+"&post="+postParam, headers=hdr)
		
		# try:
			# page = urllib2.urlopen(req)
		# except urllib2.HTTPError, e:
			# print e.fp.read()
		
		# html = page.read()
		# print html
		
		r = requests.get("http://dev.morf.lv/mirror.php?url="+url+"&post="+postParam)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
		
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
		
	# test = html.encode('latin1').decode('utf8')
	# print test
	
	return html
	
def getHTML(url, data = False):	   
	print "Downloading URL..."
	
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		

	if sys.hexversion >= 0x02070BF0:
		print "Cool, we have TLSv1 Support"
		
		context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		context.verify_mode = ssl.CERT_NONE
		context.check_hostname = False
	
		req = urllib2.Request(url, headers=hdr)

		try:
			page = urllib2.urlopen(req,context=context)
		except urllib2.HTTPError, e:
			print "ERROR while downloading: " + e.fp.read()

		html = page.read()
	else:
		print "Crap we have the old version"
		
		req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
		
		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.fp.read()

		html = page.read()
		
	print "Length of the string: ", len(html)
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
	
	print "URL Downloaded"
	return html
	
def Categories():
	url = 'http://cinemalive.tv/filmaslatviski'
	html = getHTML(url)
	print 'html: ' + html
	genre_links = common.parseDOM(html, "ul", attrs = { "class": "nav-submenu" })
	addDir('Meklēt', '', 'state_search', None)	
	print genre_links
	
# for link, title in genre_links:
# if isLinkUseful(link):
# addDir(title, url + link, 20, None)

def isLinkUseful(needle):
    haystack = ['/index.php', '#']
    return needle not in haystack
	
def isVideoFormat(needle):
    haystack = ['mp4', 'avi']
    return needle in haystack
	
def HomeNavigation():
	url = 'https://cinemalive.tv/filmaslatviski'
	html = getHTML(url)
	# print 'html: ' + html
	nav_links_list = common.parseDOM(html, "div", attrs = { "id": "genre-nav" })
	nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	nav_links_name = common.parseDOM(nav_links_list, "a")
	addDir('Meklēt', '', 'state_search', None)
		
	# pagirasList = u'https://openload.co/embed/pbQKtANhUNI/'	
	# link = urlresolver.resolve(pagirasList)
	# addDir('Paģiras 2', pagirasList, 'state_play', None)
	# addLink("Paģiras 2", link.encode('utf-8'), None)
	# print nav_links
	# print nav_links_name
	for i in range(0, len(nav_links)):
		if isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			addDir(nav_links_name[i].encode('utf-8'), mainURL + nav_links[i], 'state_movies', None)
			
def Movies(url, page=1):
	html = getHTML(url+"/lapa/"+str(page))
	# print "html" + url
	moviesList = common.parseDOM(html, "div", attrs = { "class": "base-used" })
	moviesTitleList = common.parseDOM(moviesList, "h2")
	moviesThumbnailURLsList = common.parseDOM(moviesList, "img", attrs = { "class": "img-thumbnail" }, ret = "src")
	moviesURLs = common.parseDOM(moviesList, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	for i in range(0, len(moviesURLs)):
		addDir(moviesTitleList[i].encode('utf-8'), moviesURLs[i], 'state_play', moviesThumbnailURLsList[i])
		
	if len(moviesURLs) >= 50:
		addDir("Nākamā Lapa >>", url , 'state_movies', None, str(int(page) + 1))


def PlayMovie(url, title, picture):
	print "url: " + url
	html = getHTML(url)
	print "html: " + html
	
	mainMovieCol = common.parseDOM(html, "div", attrs = { "class": "row mov-com-col"} )
	print mainMovieCol
	videoContainers = common.parseDOM(mainMovieCol[0], "source", ret="src")
	videoContainers = videoContainers + common.parseDOM(mainMovieCol[0], "iframe", ret="src")
	print "ATRASTIE VIDEO: "
	print videoContainers
	print title.decode('latin-1').encode('utf-8')
	
	if len(videoContainers) > 0:		
		link = urlresolver.resolve(videoContainers[0])
		if link != False:
			addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", link.encode('utf-8'), picture)	
		elif isVideoFormat(videoContainers[0].split(".")[-1]):
			addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[0], picture)	
		print link
	if len(videoContainers) > 1:
		link = urlresolver.resolve(videoContainers[1])
		if link != False:
			addLink(title.decode('utf-8').encode('utf-8') + " - Angliski", link.encode('utf-8'), picture)
		elif isVideoFormat(videoContainers[1].split(".")[-1]):
			addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[1], picture)	
			
		print link
	# link = re.compile('file:[\s\t]*"(.+?)"').findall(html.decode('windows-1251').encode('utf-8'))[0]
	
	
	
	

def addDir(title, url, mode, picture, page=None):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    if  picture == None:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    else:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png' , thumbnailImage=mainURL + picture)    
        sys_url += '&picture=' + urllib.quote_plus(str(picture))
    if page != None:
        sys_url += '&page=' + urllib.quote_plus(str(page))
    item.setInfo(type='Video', infoLabels={'Title': title})

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)
	
def addLink(title, url, picture):
    if  picture == None:
        item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
    else:
		item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=mainURL + picture)
    item.setInfo( type='Video', infoLabels={'Title': title} )	
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)
	
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param

common = CommonFunctions
common.plugin = "Filmas-Latviski-0.0.1"

params = get_params()
url = None
title = None
mode = None
picture = None
page = 1

try:
    title = urllib.unquote_plus(params['title'])
except:
    pass
try:
    url = urllib.unquote_plus(params['url'])
except:
    pass
try:
    mode = urllib.unquote_plus(params['mode'])
except:
    pass
try:
    picture = urllib.unquote_plus(params['picture'])
except:
    pass
try:
    page = int(params['page'])
except:
    pass

if mode == None:
	HomeNavigation();
elif mode == 'state_movies':
	Movies(url, page)
elif mode == 'state_play':
	PlayMovie(url, title, picture)
elif mode == 'state_search':
	Search()

		

# print(requests.get("https://cinemalive.tv/filmaslatviski", verify=False))

	
xbmcplugin.endOfDirectory(int(sys.argv[1]))


# content = getHTML("https://cinemalive.tv/filmaslatviski");
# print content
	




# addon_handle = int(sys.argv[1])

# xbmcplugin.setContent(addon_handle, 'movies')

# url = urlresolver.resolve('https://openload.co/embed/eCLBpX3iByw/') 

# li = xbmcgui.ListItem('Sapinusies', iconImage='DefaultVideo.png')
# xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

# xbmcplugin.endOfDirectory(addon_handle)

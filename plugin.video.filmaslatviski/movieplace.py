# -*- coding: utf-8 -*-
import network
import sys
import re
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import CommonFunctions
import kodi_func
import hqqresolver
import hqqresolver2
import urlparse
import js2py
import base64
import urllib, urllib2, ssl, re
import requests

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 5

mainURL = 'http://movieplace.lv'

def SearchRaw(searchStr):

	result = []
	
	if searchStr == False or len(searchStr) == 0: return result
	
	html = network.getHTML("http://movieplace.lv/search/?q=" + searchStr)
	
	print html
	# found_items = common.parseDOM(html, "div", attrs = { "style": "height:78px" })
	found_links = common.parseDOM(html, "a", attrs = { "itemprop": "url" }, ret = "href")
	imgTitleContainer = common.parseDOM(html, "a", attrs = { "itemprop": "url" })
	for i in range(0,len(imgTitleContainer)):
		imgTitleContainer[i] = imgTitleContainer[i].replace("<b>", "").replace("</b>","")
	found_name = common.parseDOM(imgTitleContainer, "img", ret = "title")
	found_image = common.parseDOM(imgTitleContainer, "img", ret = "src")
	print found_links
	print found_name
	print found_image
	print imgTitleContainer
	
	for i in range(0, len(found_links)):		
		result.append({
			'title': network.cleanHTML(found_name[i]).encode('utf-8'),
			'url': found_links[i],
			'thumb': mainURL+found_image[i],
			'state': 'state_play',
			'source_id': mySourceId
		})
	
	return result
		
def Search(searchStr = None):
	if searchStr == None:
		text = kodi_func.showkeyboard('', u'Meklēt filmu')
	else:
		text = searchStr
	print "Search string: " + text
	results = SearchRaw(text)
	
	for r in results:
		kodi_func.addDir(r['title'], r['url'], 'state_play', r['thumb'], source_id=r['source_id'])
		
def HomeNavigation():
	print "Opening movieplace.lv"
	url = mainURL + '/load/'
	html = network.getHTML(url)
	# print 'html: ' + html
	# nav_links_list = common.parseDOM(html, "div", attrs = { "id": "genre-nav" })
	nav_links = common.parseDOM(html, "a", attrs = { "class": "catName" }, ret = "href")
	nav_links_name = common.parseDOM(html, "a", attrs = { "class": "catName" })
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Jaunākās Filmas | Visas Filmas', mainURL + '/load/', 'state_movies', '%s/new.png'% kodi_func.iconpath, source_id=mySourceId)
	# kodi_func.addDir('TOP 50 Filmas', mainURL + '/index/top_50_filmas/0-4', 'state_movies', '%s/star.png'% kodi_func.iconpath, source_id=mySourceId)
		
	print nav_links
	print nav_links_name
	for i in range(0, len(nav_links)):
		if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			kodi_func.addDir(nav_links_name[i].encode('utf-8'), mainURL + nav_links[i], 'state_movies', kodi_func.GetCategoryImage(nav_links_name[i]), source_id=mySourceId)
			
def Movies(url, page=1):
	if url == "http://movieplace.lv/index/top_50_filmas/0-4":
		html = network.getHTML(url)
	else:
		html = network.getHTML(url+"?page"+str(page))
		
	# print "html " + html
	moviesList = common.parseDOM(html, "div", attrs = { "class": "pooular-movie-poster features-img movie-img" })
	moviesTitleList = common.parseDOM(moviesList, "img", ret = "title")
	moviesThumbnailURLsList = common.parseDOM(moviesList, "img", ret = "src")
	movieURLsContainer = common.parseDOM(moviesList, "div", attrs = { "class": "post-title" })
	moviesURLs = common.parseDOM(movieURLsContainer, "a", ret = "href")
	print moviesList, moviesTitleList, moviesThumbnailURLsList, moviesURLs
	
	
	for i in range(0, len(moviesURLs)):
		kodi_func.addDir(moviesTitleList[i].encode('utf-8'), mainURL + moviesURLs[i], 'state_play', mainURL+moviesThumbnailURLsList[i], source_id=mySourceId)
		
	if len(moviesURLs) >= 15:
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "url: " + url
	html = network.getHTML(url)
	# print "html: " + html
	
	streamLangNames = []
	
	mainMovieCol = common.parseDOM(html, "div", attrs = { "class": "videooPlayer"} )
	mainMovieCol = mainMovieCol[0].replace("\n", "").replace("<br>", "").replace("<br />", "")
	
	streamLangNames = re.findall('[(A-Z A-Z)|(A-Z)]+<iframe', mainMovieCol)
	movieStreamSrc = common.parseDOM(mainMovieCol, "iframe", ret = "src" )
	
	# For fucks sake, not only this website has hqq links but sometimes it hides them in ;eval obfuscators. Come on gentelmen make my life a bit easier
	if ";eval" in mainMovieCol:
		js = mainMovieCol.split('<script language="javascript" type="text/javascript">',1)[1].replace("</script>", "")
		print js
		jsDecoded = getURLFromObfJs(js)
		if re.search(r'<form(.+?)action="[^"]*(hqq|netu)\.tv/player/embed_player\.php"[^>]*>', jsDecoded):
			movieStreamSrc.append( jsDecoded )
		else:
			movieStreamSrc = common.parseDOM(jsDecoded, "iframe", ret = "src" )
	elif "/player/hash.php" in mainMovieCol:
		searchObj = re.search(r'(https:|http:)\/\/(hqq|netu)\.tv/player/hash\.php\?hash=\d+', html)
		if searchObj:
			resolvedHashUrl = searchObj.group(0)
			print "RESOLVED HASH URL: " + resolvedHashUrl	
			movieStreamSrc.append(resolvedHashUrl)
		else:
			print "WTF, couldn't find the hash url"
			return False
	elif "data:text/javascript;charset=utf-8;base64" in mainMovieCol:
		movieStreamSrc.append(mainMovieCol)
	
	
	   
	print "Important HTML elements:"
	print mainMovieCol, streamLangNames, movieStreamSrc
	for i in range(0, len(movieStreamSrc)):
		# sometimes the links are hidden in goo.gl shortener, if so, we first need to unshorten
		if "goo.gl" in movieStreamSrc[i]:
			movieStreamSrc[i] = network.unshorten_url( movieStreamSrc[i] )
	
		# If it is the normal stream utilise the hqqresolver
		if "hqq.tv" in movieStreamSrc[i] or "netu.tv" in movieStreamSrc[i] or "data:text/javascript;charset=utf-8;base64" in movieStreamSrc[i] or "<form" in movieStreamSrc[i]:
			link = hqqresolver.resolve(movieStreamSrc[i])
			print "resolved link: ",link
			
			if not link:
				print "Well hqqresolver script failed... let's try my one"
				parsed = urlparse.urlparse( movieStreamSrc[i] )
				vid = urlparse.parse_qs(parsed.query)['vid'][0]
				print ("VID: " + vid)
				hqqvidresolver = hqqresolver2.hqqResolver()
                                    
				# Parse the final URL
				link = hqqvidresolver.resolve(vid)
				print ("Final URL: " + link)

				# resolveHQQ(movieStreamSrc[i], url)
			else:
				link = link[0]['url']
		else: # or sometimes we get openload.co stream
			link = urlresolver.resolve(movieStreamSrc[i])
		
		if i < len(streamLangNames):
			streamLang = " - " + streamLangNames[i][:-7]
		else:
			streamLang = ""
		print streamLang
		
		if link != False:
			print link
		
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + streamLang.encode('utf-8'), link.encode('utf-8'), picture)	
		elif kodi_func.isVideoFormat(movieStreamSrc[i].split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + streamLang.encode('utf-8'), movieStreamSrc[i], picture)
		
	
def getURLFromObfJs(js):
	js = js.replace("eval", "fnRes=")
	print "return" in js
	js = str(js2py.eval_js(js))

	# First let's decode the javascript
	searchObj = re.search("var _escape='[%u\\d\\w]+';", js)
	if searchObj:
		escapeCode = searchObj.group().replace("var _escape='", "")[:-2]
		escapeCode = escapeCode.replace("%", "\\")
		escapeCode = escapeCode.decode("unicode-escape").replace("'+autoplay+'","no")
		print "escape code: " + escapeCode
	else:
		return False
	
	if re.search(r'<form(.+?)action="[^"]*(hqq|netu)\.tv/player/embed_player\.php"[^>]*>', escapeCode):
		return escapeCode
	# Second let's find the iframes src
	iframes = re.findall('<iframe [\\w\\d"=:\\/.?&\'+ %-;><]*<\\/iframe>', escapeCode)
	return '-'.join(iframes)
# -*- coding: utf-8 -*-
import network
import sys
import os
import re
import codecs
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import CommonFunctions
import kodi_func

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 3

mainURL = 'http://tvkanali.lv/video/vic/latviesu_filmas/*1'
maxMoviesInPage = 30

def SearchRaw(searchStr):
	result = []
	if searchStr == False or len(searchStr) == 0: return result
	
	moviesList = []
	
	moviesList += LoadIndexedFile( kodi_func.home + "/resources/tvfilmaslv_movieIndexes.txt" )
	moviesList += LoadIndexedFile( kodi_func.home + "/resources/tvfilmaslv_animationIndexes.txt" )
	
	# print moviesList
	
	for movie in moviesList:
		if searchStr in movie['searchable_title']:
			result.append({
				'title': movie['title'].encode('utf-8'),
				'url': movie['url'],
				'thumb': movie['thumb'],
				'state': 'state_play',
				'source_id': mySourceId
			})
	
	return result
		
def Search(searchStr = None):
	if searchStr == None:
		text = kodi_func.showkeyboard('', u'Meklēt filmu')
	else:
		text = searchStr
	print "Search string: " + str(text)
	results = SearchRaw(text)
	
	for r in results:
		kodi_func.addDir(r['title'], r['url'], 'state_play', r['thumb'], source_id=r['source_id'])
		
	
def HomeNavigation():
	print "Opening tvkanali.lv"
	if not os.path.isfile(  kodi_func.home + "/resources/tvfilmaslv_movieIndexes.txt" ) or not os.path.isfile(  kodi_func.home + "/resources/tvfilmaslv_animationIndexes.txt" ):	
		IndexWebsite()
	# url = 'http://tvkanali.lv/video/vic/latviesu_filmas/*1'
	# html = network.getHTML(url)
	# print 'html: ' + html
	# nav_links_list = common.parseDOM(html, "div", attrs = { "id": "genre-nav" })
	# nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	# nav_links_name = common.parseDOM(nav_links_list, "a")
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Latviešu Filmas', 'filmas', 'state_movies', '%s/categories/latvia.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Latviešu Multfilmas', 'multfilmas', 'state_movies', '%s/Categories/Animation.png'% kodi_func.iconpath, source_id=mySourceId)
		
	# print nav_links
	# print nav_links_name
	# for i in range(0, len(nav_links)):
		# if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			# kodi_func.addDir(nav_links_name[i].encode('utf-8'), mainURL + nav_links[i], 'state_movies', None, source_id=mySourceId)
			
def Movies(url, page=1):
	moviesList = None
	
	if url == 'filmas':
		moviesList = LoadIndexedFile( kodi_func.home + "/resources/tvfilmaslv_movieIndexes.txt" )
	elif url == 'multfilmas':
		moviesList = LoadIndexedFile( kodi_func.home + "/resources/tvfilmaslv_animationIndexes.txt" )
		

	if moviesList == None:
		print "Something went wrong, no movies were loaded"
		return
	
	for i in range((page-1)*maxMoviesInPage, ((page-1)*maxMoviesInPage)+maxMoviesInPage ):
		if i < len(moviesList):
			movie = moviesList[i]
			print movie
			kodi_func.addDir(movie['title'].encode('utf-8'), movie['url'], 'state_play', movie['thumb'], source_id=mySourceId)
		else:
			break	
			
	if len(moviesList) >= maxMoviesInPage and ((page-1)*maxMoviesInPage)+maxMoviesInPage <= len(moviesList):
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
	# html = network.getHTML(url+"/lapa/"+str(page))
	# print "html" + url
	# moviesList = common.parseDOM(html, "div", attrs = { "class": "base-used" })
	# moviesTitleList = common.parseDOM(moviesList, "h2")
	# moviesThumbnailURLsList = common.parseDOM(moviesList, "img", attrs = { "class": "img-thumbnail" }, ret = "src")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	# for i in range(0, len(moviesURLs)):
		# kodi_func.addDir(moviesTitleList[i].encode('utf-8'), moviesURLs[i], 'state_play', mainURL+moviesThumbnailURLsList[i], source_id=mySourceId)
		
	# if len(moviesURLs) >= 50:
		# kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "Opening url: " + url
	link = urlresolver.resolve(url)
	# xbmc.executebuiltin('PlayMedia('+link+')')
	# xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	if link != False:		
		kodi_func.addLink(title.decode('utf-8').encode('utf-8'), link.encode('utf-8'), picture)	
	elif kodi_func.isVideoFormat(url.split(".")[-1]):
		kodi_func.addLink(title.decode('utf-8').encode('utf-8'), url, picture)	
	print link

	
	
# This website doesn't have search function, so we must first index it
# These function are uniquer to this source
def LoadIndexedFile(file):
	f = codecs.open(file, "r", "utf-8")
	content = f.read()
	movies = content.split("\n")
	
	result = []
	
	for movie in movies:
		params = movie.split("|")
		if len(params) == 3:
			result.append({
				'title': params[0],
				'url': params[1].decode('utf-8'),
				'thumb': params[2].decode('utf-8'),
				'searchable_title': MakeSearchableString(params[0])
			})
		else:
			print "Something wrong with this movie:", movie
	
	return result

def MakeSearchableString(str):
	str = str.lower()
	
	str = str.replace(u'ē', 'e')
	str = str.replace(u'ŗ', 'r')
	str = str.replace(u'ū', 'u')
	str = str.replace(u'ī', 'i')
	str = str.replace(u'ō', 'o')
	str = str.replace(u'ā', 'a')
	str = str.replace(u'š', 's')
	str = str.replace(u'ģ', 'g')
	str = str.replace(u'ķ', 'k')
	str = str.replace(u'ļ', 'l')
	str = str.replace(u'ž', 'z')
	str = str.replace(u'č', 'c')
	str = str.replace(u'ņ', 'n')
	
	# print str
	return str
	
def IndexPage(url):
	baseUrl = "http://tvkanali.lv"
	url = baseUrl+url
	
	html = network.getHTML(url)
	
	videoBlock = common.parseDOM( html, "div", attrs = { "class": "vep-video-block" } )
	print videoBlock
	result = {'title': None, 'url': None, 'thumb': None}
	searchObj = re.search('src=\\\\"[:\/\w\d\.=?\-&]*', videoBlock[0])
	if searchObj:
		resolvedUrl = searchObj.group().replace('src=\\"', '')
		print resolvedUrl
		if resolvedUrl.startswith("//"):
			resolvedUrl = "http:"+resolvedUrl
		# resolvedUrl = resolvedUrl[:-2]
		result['url'] = resolvedUrl
		
	title = common.parseDOM( html, "h1", attrs = { "class": "vep-title" })
	
	imageBlock = common.parseDOM( html, "a", attrs = { "class": "vep-playvideo" } )
	image = common.parseDOM(imageBlock, "img", ret = "src")
	
	result['title'] = title[0]
	result['thumb'] = image[0]
	
	return result
	
def IndexCategory( baseUrl, fileName ):
	progress_dialog = xbmcgui.DialogProgress()
	progress_dialog.create("Indeksējam tvfilmas.lv")
	
	currentPage = 1
	
	url = baseUrl + str(currentPage)
	html = network.getHTML(url)
	
	entries = common.parseDOM( html, "span", attrs = {"id": "num_entries"} )
	indexed = 0
	
	
	movieEntriesList = common.parseDOM( html, "ul", attrs = { "id": "uEntriesList" })
	screenList = common.parseDOM( movieEntriesList, "div", attrs = {"class": "ve-screen"})
	movieUrls = common.parseDOM(screenList, "a", ret = "href")
	# print movieUrls, len(movieUrls)
	movieURLIndex = 0
	
	localFile = kodi_func.home + "/resources/"+fileName # xbmc.translatePath('special://temp/'+fileName )
	temp = codecs.open( localFile, 'w', "utf-8")

	
	movieIndexes = []
	if len(entries) == 1:
		for indexed in range(0, int(entries[0])):
			progress = int(float((float(indexed)/int(entries[0]))*100))
			# print "Progress: " + str(progress)
			progress_dialog.update( progress , "Lūdzu uzgaidi...", "Indeksējam Latviešu Filmas ", "Atlicis: " + str(int(entries[0]) - indexed) )
			if (progress_dialog.iscanceled()): return
			
			# print movieUrls[movieURLIndex]
			result = IndexPage(movieUrls[movieURLIndex])
			temp.write( result['title'] +"|" +result['url'] +"|" +result['thumb'] +"\n" )
			movieIndexes.append( result )
			
			movieURLIndex += 1
			
			if len(movieUrls) == movieURLIndex:
				currentPage += 1
				html = network.getHTML(baseUrl+str(currentPage))
				movieEntriesList = common.parseDOM( html, "ul", attrs = { "id": "uEntriesList" })
				screenList = common.parseDOM( movieEntriesList, "div", attrs = {"class": "ve-screen"})
				movieUrls = common.parseDOM(screenList, "a", ret = "href")
				# print movieUrls, len(movieUrls)
				movieURLIndex = 0
		
		
	temp.close()	
	return movieIndexes
	
def IndexWebsite():
	print "Indeksējam latviešu filmas"
	if not os.path.isfile(  kodi_func.home + "/resources/tvfilmaslv_movieIndexes.txt" ):
		IndexCategory( 'http://tvkanali.lv/video/vic/latviesu_filmas/*', 'tvfilmaslv_movieIndexes.txt' )
	if not os.path.isfile(  kodi_func.home + "/resources/tvfilmaslv_animationIndexes.txt" ):
		IndexCategory( 'http://tvkanali.lv/video/vic/latviesu_multfilmas/*', 'tvfilmaslv_animationIndexes.txt' )
	# common.parse( html, "div", attrs = { "id": "uEntriesList" })
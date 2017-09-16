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
import urlparse
import json

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 6

mainURL = 'http://skaties.lv'

def SearchRaw(searchStr):

	result = []
	
	if searchStr == False or len(searchStr) == 0: return result
	
	html = network.getHTML("http://skaties.lv/filmas/?q=" + searchStr)
	
	content = common.parseDOM(html, "div", attrs = { "id": "content" })
	moviesList = common.parseDOM(content, "ul", attrs = { "class": "movies clearfix" })
	moviesOriginalDiv = common.parseDOM(moviesList, "div", attrs = { "class": "original" })
	moviesFigures = common.parseDOM(moviesOriginalDiv, "figure")
	moviesTitleList = common.parseDOM(moviesFigures, "img", ret = "alt")
	moviesThumbnailURLsList = common.parseDOM(moviesFigures, "img", ret = "src")	
	moviesURLs = common.parseDOM(moviesList, "a", attrs = { "class": "button primary-button"}, ret = "href")
	print moviesList, moviesTitleList, moviesThumbnailURLsList, moviesURLs
	print str(len(moviesTitleList)) + " " + str(len(moviesThumbnailURLsList)) + " " + str(len(moviesURLs))
	
	
	# for i in range(0, len(moviesURLs)):
		# kodi_func.addDir(moviesTitleList[i].encode('utf-8'), mainURL + moviesURLs[i], 'state_play', moviesThumbnailURLsList[i], source_id=mySourceId)
	
	for i in range(0, len(moviesURLs)):		
		result.append({
			'title': moviesTitleList[i].encode('utf-8'),
			'url': mainURL + moviesURLs[i],
			'thumb': moviesThumbnailURLsList[i],
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
	print "Opening skaties.lv"
	url = mainURL + '/filmas'
	html = network.getHTML(url)
	# print 'html: ' + html
	nav_links_list = common.parseDOM(html, "nav", attrs = { "class": "horizontal-submenu movies-categories clearfix" } )
	nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	nav_links_name = common.parseDOM(nav_links_list, "a")
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Jaunākās Filmas', mainURL + '/filmas/', 'state_movies', '%s/new.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Populārākās Filmas', mainURL + '/filmas/popularakas/', 'state_movies', '%s/star.png'% kodi_func.iconpath, source_id=mySourceId)
	# kodi_func.addDir('TOP 50 Filmas', mainURL + '/index/top_50_filmas/0-4', 'state_movies', '%s/star.png'% kodi_func.iconpath, source_id=mySourceId)
	
	print "ELEMENTS: ", nav_links_list
	print nav_links
	print nav_links_name
	for i in range(0, len(nav_links)):
		if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			link_name = re.sub("<i.+></i>", '', nav_links_name[i]).strip()
			kodi_func.addDir(link_name.encode('utf-8'), mainURL + nav_links[i], 'state_movies', kodi_func.GetCategoryImage(link_name), source_id=mySourceId)
			
def Movies(url, page=1):
	html = network.getHTML(url.replace("#all-movies", "")+"/page/"+str(page)+"/")
		
	print "PAGE: " + url+"/page/"+str(page)+"/"
	# print "html " + html
	content = common.parseDOM(html, "div", attrs = { "id": "content" })
	moviesList = common.parseDOM(content, "ul", attrs = { "class": "movies clearfix" })
	moviesOriginalDiv = common.parseDOM(moviesList, "div", attrs = { "class": "original" })
	moviesFigures = common.parseDOM(moviesOriginalDiv, "figure")
	moviesTitleList = common.parseDOM(moviesFigures, "img", ret = "alt")
	moviesThumbnailURLsList = common.parseDOM(moviesFigures, "img", ret = "src")	
	moviesURLs = common.parseDOM(moviesList, "a", attrs = { "class": "button primary-button"}, ret = "href")
	
	published = []
	
	for i in range(0, len(moviesOriginalDiv)):
		div = moviesOriginalDiv[i]
		pub = common.parseDOM(div, "p", attrs = { "class": "published" })		
		if len(pub) == 0:
			published.append("")
		else:
			if "<span" in pub[0]:
				pub = common.parseDOM(pub, "span")				
				
			published.append(" ("+pub[0]+")")
	
	print moviesList, moviesTitleList, moviesThumbnailURLsList, moviesURLs, moviesFigures, published
	print str(len(moviesTitleList)) + " " + str(len(moviesThumbnailURLsList)) + " " + str(len(moviesURLs)) + " " + str(len(published))
	
	
	for i in range(0, len(moviesURLs)):
		kodi_func.addDir(moviesTitleList[i].encode('utf-8') + published[i].encode('utf-8'), mainURL + moviesURLs[i], 'state_play', moviesThumbnailURLsList[i], source_id=mySourceId)
		
	if len(moviesURLs) >= 21:
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "url: " + url
	html = network.getHTML(url)
	# print "html: " + html
	
	streamLangNames = []
	
	movieDivContainer = common.parseDOM(html, "div", attrs = { "class": "featured-movie-player"} )
	movieIframeSrc = common.parseDOM(movieDivContainer, "iframe", ret = "src" )
	
	movieID = urlparse.parse_qs( urlparse.urlparse(movieIframeSrc[0]).query )['id'][0]
	print "MoviedID: " , movieID
	
	jsonRaw = network.getHTML( "http://playapi.mtgx.tv/v3/videos/stream/" + movieID )
	print "RAW JSON: ", jsonRaw
	if jsonRaw:
		jsonDecoded = json.loads(jsonRaw)
	else:
		jsonDecoded = ""
	
	if 'streams' not in jsonDecoded:
		jsonRaw = network.getHTML( "http://dev.morf.lv/mirror.php?url=http://playapi.mtgx.tv/v3/videos/stream/" + movieID ).replace('<base href="http://playapi.mtgx.tv/v3/videos/stream/'+movieID+'" />', '')
		print "fallback json raw:", jsonRaw
		jsonDecoded = json.loads(jsonRaw)
	
	print "Movie Elements: " , movieDivContainer, movieIframeSrc, jsonDecoded
	
	if jsonDecoded['streams']['high'] != None:
		kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - HIGH", jsonDecoded['streams']['high'], picture)
	
	if jsonDecoded['streams']['hls'] != None:
		kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - HLS", jsonDecoded['streams']['hls'], picture)
		
	# if jsonDecoded['streams']['medium'] != None:
		# kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - MEDIUM", jsonDecoded['streams']['medium'], picture)
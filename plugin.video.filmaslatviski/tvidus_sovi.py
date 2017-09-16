# -*- coding: utf-8 -*-
import network
import sys
import xbmc
import xbmcgui
import xbmcplugin
import re
import urlresolver
import CommonFunctions
import kodi_func
import cfscrape
import requests
import tempfile
import shutil
import base64

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 7

#important this website uses DDoS prevention mechanism
#https://github.com/Anorov/cloudflare-scrape

mainURL = 'http://tvid.us/'

def SearchRaw(searchStr):
	result = []
	
	if searchStr == False or len(searchStr) == 0: return result
	
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get("http://tvid.us/shows/search/"+str(searchStr)).content
	
	content = common.parseDOM(html, "div", attrs = { "class": "box box-default" })
	
	showsList = common.parseDOM(content, "div", attrs = {"class": "col-sm-6 col-md-3"})
	showsURLs = common.parseDOM(showsList, "a", ret='href')
	
	showTitles = common.parseDOM(showsList, "h4")
	# showEpisodeTitles = common.parseDOM(slider, "small", attrs = {"class": "pull-right"} )
	showThumbnailURLsList = common.parseDOM(showsList, "div", ret = "style")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href", attrs = { "class": "btn btn-primary" })
	# print moviesThumbnailURLsList
	print "ELEMENTS", showsList, showsURLs, showTitles, showThumbnailURLsList
	
	
	for i in range(0, len(showsURLs)):
		localFile = None
		try:
			searchObj = re.search("background-image:url\\(//.+\\);", showThumbnailURLsList[i])
			if searchObj:
				thumbnailResolvedURL = searchObj.group().replace("background-image:url(", '')
				thumbnailResolvedURL = thumbnailResolvedURL[:-2]	
			
			print "Resolved Thumbnail URL: " + thumbnailResolvedURL
			
			rawImage = scraper.get("http:"+thumbnailResolvedURL, stream=True)
			rawImage.decode_content = True	
			localFile = xbmc.translatePath('special://temp/'+thumbnailResolvedURL.split("/")[-1] )
			temp = open( localFile, mode='wb')
			shutil.copyfileobj(rawImage.raw, temp)
			temp.close()
			print localFile
		except:
			pass
			
		result.append({
			'title': showTitles[i].encode('utf-8'),
			'url': 'http:'+showsURLs[i],
			'thumb': localFile,
			'state': 'state_seasons',
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
		kodi_func.addDir(r['title'], r['url'], r['state'], r['thumb'], source_id=r['source_id'])
		
		
	# if len(results) >= 27:
		# kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', None, str(int(page) + 1), source_id=mySourceId)
		
		
def HomeNavigation():
	print "Opening tvid.us šovi"
	# nav_links = common.parseDOM(html, "a", ret = "href", attrs = { "class": "btn btn-success btn-flat col-xs-12 col-sm-6 col-md-3" })
	# nav_links_name = common.parseDOM(html, "a", attrs = { "class": "btn btn-success btn-flat col-xs-12 col-sm-6 col-md-3" })
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Nesen Pievienotie', mainURL+"shows", 'state_movies', '%s/new.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Visi seriāli un pārraides',  mainURL+"shows", 'state_shows', '%s/folder.png'% kodi_func.iconpath, source_id=mySourceId)

	# for i in range(0, len(nav_links)):
		# if kodi_func.isLinkUseful(nav_links[i]):			
			# kodi_func.addDir(nav_links_name[i].encode('utf-8'), 'http:' + nav_links[i], 'state_movies', kodi_func.GetCategoryImage(nav_links_name[i]), source_id=mySourceId)
			
def Movies(url, page=1):
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get(url).content
	# print html

	print "URL: " + url
	
	slider = common.parseDOM(html, "ul", attrs = { "class": "slider1" })
	
	showsList = common.parseDOM(slider, "li")
	showsURLs = common.parseDOM(slider, "li", ret='onClick')
	# moviesTitleList = common.parseDOM(moviesList, "h4")
	showTitles = common.parseDOM(slider, "small", attrs = {"style": "font-size:13px; padding-top:8px; opacity:0.9;"} )
	showEpisodeTitles = common.parseDOM(slider, "small", attrs = {"class": "pull-right"} )
	showThumbnailURLsList = common.parseDOM(slider, "img", ret = "src")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href", attrs = { "class": "btn btn-primary" })
	# print moviesThumbnailURLsList
	print "ELEMENTS", slider, showsList, showsURLs, showTitles, showEpisodeTitles, showThumbnailURLsList
	
	
	for i in range(0, len(showsURLs)):
		localFile = None
		try:
			rawImage = scraper.get("http:"+showThumbnailURLsList[i], stream=True)
			rawImage.decode_content = True	
			localFile = xbmc.translatePath('special://temp/'+showThumbnailURLsList[i].split("/")[-1] )
			temp = open( localFile, mode='wb')
			shutil.copyfileobj(rawImage.raw, temp)
			temp.close()
			print localFile
		except:
			pass
			
		searchObj = re.search("'//.+',", showsURLs[i])
		if searchObj:
			resolvedUrl = searchObj.group().replace("'//", 'http://')
			resolvedUrl = resolvedUrl[:-2]			
				
		# print "Resolved URL: " + resolvedUrl
		kodi_func.addDir(showTitles[i].encode('utf-8') + " - " + showEpisodeTitles[i].encode('utf-8'), resolvedUrl, 'state_play', localFile, source_id=mySourceId)
		
	# if len(moviesURLs) >= 27:
		# kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def Shows(url, page=1):
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get(url+"/page/"+str(page)).content
	# print html

	print "URL: " + url
	
	content = common.parseDOM(html, "div", attrs = { "class": "box box-default" })
	
	showsList = common.parseDOM(content, "div", attrs = {"class": "col-sm-6 col-md-3"})
	showsURLs = common.parseDOM(showsList, "a", ret='href')
	
	showTitles = common.parseDOM(showsList, "h4")
	# showEpisodeTitles = common.parseDOM(slider, "small", attrs = {"class": "pull-right"} )
	showThumbnailURLsList = common.parseDOM(showsList, "div", ret = "style")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href", attrs = { "class": "btn btn-primary" })
	# print moviesThumbnailURLsList
	print "ELEMENTS", showsList, showsURLs, showTitles, showThumbnailURLsList
	
	
	for i in range(0, len(showsURLs)):
		localFile = None
		try:
			searchObj = re.search("background-image:url\\(//.+\\);", showThumbnailURLsList[i])
			if searchObj:
				thumbnailResolvedURL = searchObj.group().replace("background-image:url(", '')
				thumbnailResolvedURL = thumbnailResolvedURL[:-2]	
			
			print "Resolved Thumbnail URL: " + thumbnailResolvedURL
			
			rawImage = scraper.get("http:"+thumbnailResolvedURL, stream=True)
			rawImage.decode_content = True	
			localFile = xbmc.translatePath('special://temp/'+thumbnailResolvedURL.split("/")[-1] )
			temp = open( localFile, mode='wb')
			shutil.copyfileobj(rawImage.raw, temp)
			temp.close()
			print localFile
		except:
			pass
		kodi_func.addDir(showTitles[i].encode('utf-8'), 'http:'+showsURLs[i], 'state_seasons', localFile, source_id=mySourceId)
		
	if len(showsURLs) >= 32:
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_shows', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def Seasons(url, title, picture):
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get(url).content
	
	print "Season URL: " + url
	
	content = common.parseDOM(html, "div", attrs = { "id": "seasons" })
	seasonName = common.parseDOM(content, "a", attrs = { "data-toggle": "collapse" })
	seasonURLs = common.parseDOM(content, "a", attrs = { "data-toggle": "collapse" }, ret = "href")
	
	seasonPanels = common.parseDOM(content, "div", attrs = { "class": "panel-body" })
	seasonEpContent = common.parseDOM(content, "div", attrs = { "class": "panel-body" })[-1]
	episodeURLs = common.parseDOM(seasonEpContent, "a", ret = "href")
	
	print "ELEMENTS: " , content, seasonName, seasonURLs, len(seasonPanels), len(seasonURLs)
	
	if len(seasonPanels) == len(seasonURLs)+1 and len(episodeURLs) > 0:
		kodi_func.addDir('Specizlaidumi'.encode('utf-8'), url+'#specizlaidums', 'state_episodes', picture, source_id=mySourceId)
	
	for i in range(0, len(seasonURLs)):
		kodi_func.addDir(seasonName[i].encode('utf-8'), url+seasonURLs[i], 'state_episodes', picture, source_id=mySourceId)

def Episodes(url, title, picture):
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get(url).content
	
	print "Season URL: " + url
	
	seasonID = url.split('#')[1]
	
	print "Season ID: " + seasonID;
	
	content = common.parseDOM(html, "div", attrs = { "id": "seasons" })
	if seasonID <> 'specizlaidums':
		seasonEpContent = common.parseDOM(content, "div", attrs = { "id": seasonID })
	else:
		seasonEpContent = common.parseDOM(content, "div", attrs = { "class": "panel-body" })[-1]
	
	episodeURLs = common.parseDOM(seasonEpContent, "a", ret = "href")
	episodeTitles = common.parseDOM(seasonEpContent, "a")
	
	# print "EPISODE ELEMENTS: ", seasonEpContent, episodeURLs, episodeTitles
	
	for i in range(0, len(episodeURLs)):
		kodi_func.addDir(episodeTitles[i].encode('utf-8'), 'http:'+episodeURLs[i], 'state_play', picture, source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	# print url
	session = requests.session()
	scraper = cfscrape.create_scraper(sess=session)
	html = scraper.get(url).content
	# print html
	# return
	displayDiv = common.parseDOM(html, "div", attrs = { "id": "display"} )
	# print displayDiv	
	videoContainer = common.parseDOM(displayDiv[0], "iframe", ret="src")
	print "ATRASTIE VIDEO: "
	print videoContainer
	print title.decode('latin-1').encode('utf-8')
	
	links = []
	
	if len(videoContainer) > 0:
		links.append( videoContainer[0] )
	
	
	searchObj = re.search('file: atob\("[\w\d=.,]*"\)', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace('file: atob("', '')
		resolvedUrl = resolvedUrl[:-2]	
		links.append( base64.b64decode(resolvedUrl) )
		# print resolvedUrl, videoContainer
	else:
	   print "Well couldn't find jwplayer url"
		
	for i in range(0, len(links)):
		linkUrl = links[i]
		link = urlresolver.resolve(linkUrl)
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8'), link.encode('utf-8'), picture)	
		elif kodi_func.isVideoFormat(linkUrl.split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8'), linkUrl, picture)	
		print "LINKS: " + str(link)
	# link = re.compile('file:[\s\t]*"(.+?)"').findall(html.decode('windows-1251').encode('utf-8'))[0]
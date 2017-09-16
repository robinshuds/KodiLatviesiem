# -*- coding: utf-8 -*-
import network
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import CommonFunctions
import kodi_func
import url_resolver_plus

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 1

mainURL = 'https://cinemalive.tv'

def SearchRaw(searchStr):
	result = []
	
	# post_fields = {'search': searchStr}
	# html = network.postHTML("https://cinemalive.tv/scripts/search.php", post_fields)
	html = network.getHTML("https://cinemalive.tv/?s="+searchStr)
	
	print html
	found_items = common.parseDOM(html, "div", attrs = { "class": "result-item" })
	found_title = common.parseDOM(found_items, "div", attrs={"class": "title"})
	found_links = common.parseDOM(found_title, "a", ret = "href")
	found_name = common.parseDOM(found_title, "a")
	found_image = common.parseDOM(found_items, "img", ret = "src")
	print found_links
	print found_name
	print found_image
	
	for i in range(0, len(found_links)):		
		result.append({
			'title': found_name[i].replace('<span class="search-everything-highlight-color" style="background-color:#6dbd4d">','').replace('</span>','').encode('utf-8'),
			'url': found_links[i],
			'thumb': mainURL+found_image[i].replace(mainURL, "").replace('150x150.jpg', '185x278.jpg'),
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
	print "Opening CinemaLive.tv"
	url = 'https://cinemalive.tv/filmaslatviski'
	html = network.getHTML(url)
	# print 'html: ' + html
	nav_links_list = common.parseDOM(html, "ul", attrs = { "class": "sub-menu" })[0]
	nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	nav_links_name = common.parseDOM(nav_links_list, "a")
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
		
	# pagirasList = u'https://openload.co/embed/dLuET3ML86E/Deadpool.%28Dedpuls%29.2016.720p.LAT.THEVIDEO.LV.mkv.mp4'	
	# link = urlresolver.resolve(pagirasList)
	# addDir('Dedpūls', pagirasList, 'state_play', None)
	# addLink("Dedpūls", link.encode('utf-8'), None)
	# print nav_links
	# print nav_links_name
	for i in range(0, len(nav_links)):
		if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			kodi_func.addDir(nav_links_name[i].encode('utf-8'),  nav_links[i], 'state_movies', kodi_func.GetCategoryImage(nav_links_name[i]), source_id=mySourceId)
			
def Movies(url, page=1):

	print "Original URL: " , url
	generatedUrl = url
	if mainURL not in generatedUrl:
		generatedUrl = mainURL + generatedUrl
		
	if "?get=" in  generatedUrl:
		index = generatedUrl.index("?")
		generatedUrl = generatedUrl[:index] + "/page/"+str(page) + "/" + generatedUrl[index:]
	else:
		generatedUrl = generatedUrl + "/page/"+str(page) 
		
	print "generated url",generatedUrl
	html = network.getHTML(generatedUrl)
	# print "html" + url
	moviesList = common.parseDOM(html, "div", attrs = { "class": "poster" })
	moviesThumbnailURLsList = common.parseDOM(moviesList, "img", ret = "src")
	moviesListData = common.parseDOM(html, "div", attrs = { "class": "data" })
	moviesTitleList = common.parseDOM(moviesListData, "a")
	moviesURLs = common.parseDOM(moviesListData, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	for i in range(0, len(moviesURLs)):
		kodi_func.addDir(moviesTitleList[i].encode('utf-8'), moviesURLs[i], 'state_play', moviesThumbnailURLsList[i], source_id=mySourceId)
		
	if len(moviesURLs) >= 40:
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "url: " + url
	html = network.getHTML(url)
	print "html: " + html
	
	mainMovieCol = common.parseDOM(html, "div", attrs = { "class": "playex"} )
	print mainMovieCol
	videoContainers = common.parseDOM(mainMovieCol[0], "source", ret="src")
	videoContainers = videoContainers + common.parseDOM(mainMovieCol[0], "iframe", ret="src")
	print "ATRASTIE VIDEO: "
	print videoContainers
	print title.decode('latin-1').encode('utf-8')
	
	if len(videoContainers) > 0:		
		link = url_resolver_plus.resolve(videoContainers[0])
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", link.encode('utf-8'), picture)	
		elif '.' in videoContainers[0] and kodi_func.isVideoFormat(videoContainers[0].split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[0], picture)	
		print link
	if len(videoContainers) > 1:
		link = url_resolver_plus.resolve(videoContainers[1])
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Angliski", link.encode('utf-8'), picture)
		elif '.' in videoContainers[1] and kodi_func.isVideoFormat(videoContainers[1].split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[1], picture)	
			
		print link
	# link = re.compile('file:[\s\t]*"(.+?)"').findall(html.decode('windows-1251').encode('utf-8'))[0]
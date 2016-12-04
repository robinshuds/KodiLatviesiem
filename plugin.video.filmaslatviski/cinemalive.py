# -*- coding: utf-8 -*-
import network
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import CommonFunctions
import kodi_func

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 1

mainURL = 'https://cinemalive.tv'

def Search():
	text = kodi_func.showkeyboard('', u'Meklēt filmu')
	print "Search string: " + text
	post_fields = {'search': text}
	html = network.postHTML("https://cinemalive.tv/scripts/search.php", post_fields)
	
	print html
	# found_items = common.parseDOM(html, "div", attrs = { "style": "height:78px" })
	found_links = common.parseDOM(html, "a", ret = "href")
	found_name = common.parseDOM(html, "span", attrs = { "style": "color:#bcbcbc" })
	found_image = common.parseDOM(html, "img", ret = "src")
	print found_links
	print found_name
	print found_image
	
	for i in range(0, len(found_links)):
		kodi_func.addDir(found_name[i].encode('utf-8'), found_links[i], 'state_play', mainURL+found_image[i].replace(mainURL, "").replace('xs.jpg', 'md.jpg'), source_id=mySourceId )
		
def HomeNavigation():
	print "Opening CinemaLive.tv"
	url = 'https://cinemalive.tv/filmaslatviski'
	html = network.getHTML(url)
	# print 'html: ' + html
	nav_links_list = common.parseDOM(html, "div", attrs = { "id": "genre-nav" })
	nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	nav_links_name = common.parseDOM(nav_links_list, "a")
	kodi_func.addDir('Meklēt', '', 'state_search', None, source_id=mySourceId)
		
	# pagirasList = u'https://openload.co/embed/dLuET3ML86E/Deadpool.%28Dedpuls%29.2016.720p.LAT.THEVIDEO.LV.mkv.mp4'	
	# link = urlresolver.resolve(pagirasList)
	# addDir('Dedpūls', pagirasList, 'state_play', None)
	# addLink("Dedpūls", link.encode('utf-8'), None)
	# print nav_links
	# print nav_links_name
	for i in range(0, len(nav_links)):
		if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			kodi_func.addDir(nav_links_name[i].encode('utf-8'), mainURL + nav_links[i], 'state_movies', None, source_id=mySourceId)
			
def Movies(url, page=1):
	html = network.getHTML(url+"/lapa/"+str(page))
	# print "html" + url
	moviesList = common.parseDOM(html, "div", attrs = { "class": "base-used" })
	moviesTitleList = common.parseDOM(moviesList, "h2")
	moviesThumbnailURLsList = common.parseDOM(moviesList, "img", attrs = { "class": "img-thumbnail" }, ret = "src")
	moviesURLs = common.parseDOM(moviesList, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	for i in range(0, len(moviesURLs)):
		kodi_func.addDir(moviesTitleList[i].encode('utf-8'), moviesURLs[i], 'state_play', mainURL+moviesThumbnailURLsList[i], source_id=mySourceId)
		
	if len(moviesURLs) >= 50:
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', None, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "url: " + url
	html = network.getHTML(url)
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
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", link.encode('utf-8'), picture)	
		elif kodi_func.isVideoFormat(videoContainers[0].split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[0], picture)	
		print link
	if len(videoContainers) > 1:
		link = urlresolver.resolve(videoContainers[1])
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Angliski", link.encode('utf-8'), picture)
		elif isVideoFormat(videoContainers[1].split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", videoContainers[1], picture)	
			
		print link
	# link = re.compile('file:[\s\t]*"(.+?)"').findall(html.decode('windows-1251').encode('utf-8'))[0]
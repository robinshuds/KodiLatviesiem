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

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 4

mainURL = 'http://www.fof.lv'

def SearchRaw(searchStr):
	result = []
	
	html = network.getHTML( "http://www.fof.lv/search/?q=" + searchStr)
	
	allEntries = common.parseDOM(html, "div", attrs = { "id": "allEntries" })
	if len(allEntries) == 0:
		allEntries = common.parseDOM(html, "table", attrs = { "id": "entry_table" })
	# print allEntries
	infoTd = common.parseDOM(allEntries, "td", attrs = { "class": "info" })
	moviesURLs = common.parseDOM(infoTd, "a", ret = "href")
	moviesThumbnailURLsList = common.parseDOM(allEntries, "td", ret = "style")
	if len(moviesThumbnailURLsList) == 0:
		moviesThumbnailURLsList = common.parseDOM(allEntries, "img", attrs = { "width": "80", "height": "100" }, ret = "src")
	moviesTitleList = common.parseDOM(infoTd, "button", attrs = {"class": "entry_button"} )
	# moviesYearList = common.parseDOM(infoTd, "div", attrs = {"style": "width: 100px; height: 18px; background: url(http://www.fom.ucoz.lv/jauns_img/entry_year.png) no-repeat; margin: 0px auto; padding-top: 2px;"} )
	print allEntries, infoTd, moviesURLs, moviesThumbnailURLsList, moviesTitleList
	# moviesTitleList = common.parseDOM(moviesList, "h2")
	# moviesThumbnailURLsList = common.parseDOM(moviesList, "img", attrs = { "class": "img-thumbnail" }, ret = "src")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	for i in range(0, len(moviesURLs)):
		thumb = moviesThumbnailURLsList[i].replace("); width: 80px; height: 100px;", "").replace("background:url(", "").replace("/s","/")
		if network.exists( mainURL+thumb ) == False:
			thumb = thumb.replace(".jpg", ".png")		
		# title = re.sub(r'<br>[\w <>="-:\d;#&\\\\]*', '', moviesTitleList[i])
		title = moviesTitleList[i].partition("<br>")[0].replace("<b>","").replace("</b>", "")
		if not moviesURLs[i].startswith("http://"):
			movieURL = mainURL + moviesURLs[i]
		else:
			movieURL = moviesURLs[i]		
		result.append({
			'title':title.encode('utf-8'),
			'url': movieURL,
			'thumb': mainURL+thumb,
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
	print "Opening fof.lv"
	url = mainURL
	html = network.getHTML(url)
	# print 'html: ' + html
	nav_links_list = common.parseDOM(html, "div", attrs = { "class": "categories" })
	nav_links = common.parseDOM(nav_links_list, "a", ret = "href")
	nav_links_name = common.parseDOM(nav_links_list, "a")
	kodi_func.addDir('Meklēt', '', 'state_search', '%s/meklet2.png'% kodi_func.iconpath, source_id=mySourceId)
	kodi_func.addDir('Jaunākās Filmas', 'http://www.fof.lv/?page1', 'state_movies', kodi_func.GetCategoryImage('jaunakas'), source_id=mySourceId)
	kodi_func.addDir('Populārākās', 'http://www.fof.lv/index/popularakas_filmas/0-13', 'state_movies', kodi_func.GetCategoryImage('skatitakas'), source_id=mySourceId)
	kodi_func.addDir('Vērtētākās', 'http://www.fof.lv/index/vertetakas_filmas/0-16', 'state_movies', kodi_func.GetCategoryImage('vertetakas'), source_id=mySourceId)
	
	# pagirasList = u'https://openload.co/embed/dLuET3ML86E/Deadpool.%28Dedpuls%29.2016.720p.LAT.THEVIDEO.LV.mkv.mp4'	
	# link = urlresolver.resolve(pagirasList)
	# addDir('Dedpūls', pagirasList, 'state_play', None)
	# addLink("Dedpūls", link.encode('utf-8'), None)
	# print nav_links
	# print nav_links_name
	for i in range(0, len(nav_links)):
		if kodi_func.isLinkUseful(nav_links[i]):
			# print mainURL + nav_links[i]
			kodi_func.addDir(nav_links_name[i].encode('utf-8'), nav_links[i], 'state_movies', kodi_func.GetCategoryImage(nav_links_name[i]), source_id=mySourceId)
			
def Movies(url, page=1):

	print "url: " + url
	if '?page1' in url:
		html = network.getHTML(mainURL+"/?page"+str(page))
	else:
		html = network.getHTML(url+"-"+str(page))
		# html = network.getHTML(url)
		
	
	# print "html " + html
	allEntries = common.parseDOM(html, "div", attrs = { "id": "allEntries" })
	if len(allEntries) == 0:
		allEntries = common.parseDOM(html, "table", attrs = { "id": "entry_table" })
	# print allEntries
	infoTd = common.parseDOM(allEntries, "td", attrs = { "class": "info" })
	moviesURLs = common.parseDOM(infoTd, "a", ret = "href")
	moviesThumbnailURLsList = common.parseDOM(allEntries, "td", ret = "style")
	if len(moviesThumbnailURLsList) == 0:
		moviesThumbnailURLsList = common.parseDOM(allEntries, "img", attrs = { "width": "80", "height": "100" }, ret = "src")
	moviesTitleList = common.parseDOM(infoTd, "button", attrs = {"class": "entry_button"} )
	# moviesYearList = common.parseDOM(infoTd, "div", attrs = {"style": "width: 100px; height: 18px; background: url(http://www.fom.ucoz.lv/jauns_img/entry_year.png) no-repeat; margin: 0px auto; padding-top: 2px;"} )
	print allEntries, infoTd, moviesURLs, moviesThumbnailURLsList, moviesTitleList
	# moviesTitleList = common.parseDOM(moviesList, "h2")
	# moviesThumbnailURLsList = common.parseDOM(moviesList, "img", attrs = { "class": "img-thumbnail" }, ret = "src")
	# moviesURLs = common.parseDOM(moviesList, "a", ret = "href")
	# print moviesThumbnailURLsList
	
	
	for i in range(0, len(moviesURLs)):
		thumb = moviesThumbnailURLsList[i].replace("); width: 80px; height: 100px;", "").replace("background:url(", "").replace("/s","/")
		if network.exists( mainURL+thumb ) == False:
			thumb = thumb.replace(".jpg", ".png")		
		# title = re.sub(r'<br>[\w <>="-:\d;#&\\\\]*', '', moviesTitleList[i])
		title = moviesTitleList[i].partition("<br>")[0]
		if not moviesURLs[i].startswith("http://"):
			movieURL = mainURL + moviesURLs[i]
		else:
			movieURL = moviesURLs[i]
		kodi_func.addDir(title.encode('utf-8'), movieURL, 'state_play', mainURL+thumb, source_id=mySourceId)
		
	if len(moviesURLs) >= 10 and url != 'http://www.fof.lv/index/popularakas_filmas/0-13' and url != 'http://www.fof.lv/index/vertetakas_filmas/0-16':
		kodi_func.addDir("Nākamā Lapa >>", url , 'state_movies', '%s/next.png'% kodi_func.iconpath, str(int(page) + 1), source_id=mySourceId)
		
def PlayMovie(url, title, picture):
	print "url: " + url
	html = network.getHTML(url)
	# print "html: " + html
	
	mainMovieCol = common.parseDOM(html, "div", attrs = { "id": "movie"} )
	print mainMovieCol
	video = common.parseDOM(mainMovieCol, "iframe", ret="src")[0]
	
	link = urlresolver.resolve(video)
	if link != False:
		kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", link.encode('utf-8'), picture)	
	elif kodi_func.isVideoFormat(video.split(".")[-1]):
		kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", video, picture)	
	print link
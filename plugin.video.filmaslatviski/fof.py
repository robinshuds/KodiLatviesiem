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
import os
import codecs

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

mySourceId = 4

mainURL = 'http://www.fof.lv'

#indexed search
def SearchRaw(searchStr):
	result = []
	
	if searchStr == False or len(searchStr) == 0: return result
	
	moviesList = []
	
	moviesList = LoadIndexedFile( kodi_func.home + "/resources/fof_lv_movieIndexes.txt" )
	
	print moviesList
	
	for movie in moviesList:
		if searchStr in movie['searchable_title']:
			result.append({
				'title': movie['title'].replace('<img src="http://fof.lv/lat-sub-icon.png" style="position: relative; left: 10px; top: 2px;">', '').encode('utf-8'),
				'url': movie['url'],
				'thumb': movie['thumb'],
				'state': 'state_play',
				'source_id': mySourceId
			})
	
	return result

#Search in fof where it uses their shitty search function, which doesn't fucking work at all
def SearchRaw_old(searchStr):
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
	print "Search string: " + str(text)
	results = SearchRaw(text)
	
	for r in results:
		kodi_func.addDir(r['title'], r['url'], 'state_play', r['thumb'], source_id=r['source_id'])
		
def HomeNavigation():

	if not os.path.isfile(  kodi_func.home + "/resources/fof_lv_movieIndexes.txt" ):
		IndexMovies( 'http://www.fof.lv/?page', 'fof_lv_movieIndexes.txt' )

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
		title = moviesTitleList[i].partition("<br>")[0].replace('<img src="http://fof.lv/lat-sub-icon.png" style="position: relative; left: 10px; top: 2px;">', '')
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
	
	try:
		link = urlresolver.resolve(video)
		if link != False:
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", link.encode('utf-8'), picture)	
		elif kodi_func.isVideoFormat(video.split(".")[-1]):
			kodi_func.addLink(title.decode('utf-8').encode('utf-8') + " - Latviski", video, picture)	
		print link
	except:
		xbmcgui.Dialog().ok("Opā!", "Nevarēju dekodēt strīmu", "Iespējams ka fails vairs neeksistē", "Tāda dzīve, mēģini citi avotu")
		
	
	
	
# This website doesn't have a proper search function, so we must first index it
# These function are unique to this source
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
				'searchable_title': kodi_func.MakeSearchableString(params[0])
			})
		else:
			print "Something wrong with this movie:", movie
	
	return result
	
	
def IndexMovies( baseUrl, fileName ):
	progress_dialog = xbmcgui.DialogProgress()
	progress_dialog.create("Indeksējam fof.lv")
	
	currentPage = 1
	
	url = baseUrl + str(currentPage)
	html = network.getHTML(url)
	
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
	
	indexed = 0
	
	
	# movieEntriesList = common.parseDOM( html, "ul", attrs = { "id": "uEntriesList" })
	# screenList = common.parseDOM( movieEntriesList, "div", attrs = {"class": "ve-screen"})
	# movieUrls = common.parseDOM(screenList, "a", ret = "href")
	# print movieUrls, len(movieUrls)
	movieURLIndex = 0
	
	localFile = kodi_func.home + "/resources/"+fileName # xbmc.translatePath('special://temp/'+fileName )
	temp = codecs.open( localFile, 'w', "utf-8")

	
	movieIndexes = []
	movieEntries = 370
	for indexed in range(0, int(movieEntries)):
		if movieURLIndex == len(moviesURLs): break
		
		progress = int(float((float(indexed)/int(movieEntries))*100))
		# print "Progress: " + str(progress)
		progress_dialog.update( progress , "Lūdzu uzgaidi...", "Indeksējam fof.lv Filmas ", "Atlicis: " + str(int(movieEntries) - indexed) )
		if (progress_dialog.iscanceled()): return
		
		
		thumb = moviesThumbnailURLsList[movieURLIndex].replace("); width: 80px; height: 100px;", "").replace("background:url(", "").replace("/s","/")
		print "thumb: " + thumb
		if network.exists( mainURL+thumb ) == False:
			thumb = thumb.replace(".jpg", ".png")		
		# title = re.sub(r'<br>[\w <>="-:\d;#&\\\\]*', '', moviesTitleList[i])
		title = moviesTitleList[movieURLIndex].partition("<br>")[0]
		if not moviesURLs[movieURLIndex].startswith("http://"):
			movieURL = mainURL + moviesURLs[movieURLIndex]
		else:
			movieURL = moviesURLs[i]
		
		print title.encode('utf-8')
		temp.write( title +"|" +movieURL +"|" +mainURL+thumb +"\n" )
		movieIndexes.append( {'title': title, 'url': movieURL, 'thumb': mainURL+thumb} )
		
		movieURLIndex += 1
		
		if len(moviesURLs) == movieURLIndex:
			currentPage += 1
			html = network.getHTML(baseUrl+str(currentPage))
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
			# print movieUrls, len(movieUrls)
			movieURLIndex = 0
		
		
	temp.close()	
	return movieIndexes
	

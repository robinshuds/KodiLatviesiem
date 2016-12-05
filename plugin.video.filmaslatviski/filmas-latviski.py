# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urlresolver
import urllib, urllib2, ssl, re
import CommonFunctions
import requests

import kodi_func

#sources
import cinemalive
import tvidus


mysettings = xbmcaddon.Addon(id = 'plugin.video.filmaslatviski')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))


sourceObjects = [{
					'source_id': 1,
					'name': 'CinemaLive.tv', 
					'description': '(1600+ filmas)',
					'icon': '%s/cinemalive.png', 
					'object': cinemalive
				},
				{
					'source_id': 2,
					'name': 'tvid.us', 
					'description': '(800+ filmas)',
					'icon': '%s/tvidus.png', 
					'object': tvidus
				}]
				
def SearchAllSources():
	searchStr = kodi_func.showkeyboard('', u'Meklēt filmas')
	if not searchStr:
		return
	results = []
	
	progress_dialog = xbmcgui.DialogProgress()
	progress_dialog.create("Meklējam filmas")

	for i in range(len(sourceObjects)):
		source = sourceObjects[i]
		progress = int(float((float(i)/len(sourceObjects))*100))
		# print "Progress: " + str(progress) + " " + str(i) + " " + str( float(1.0/2.0) )
		progress_dialog.update( progress , "Lūdzu uzgaidi...", "Meklējam avotā: " + source['name'], "Atlikuši avoti: " + str(len(sourceObjects) - i) )
		if (progress_dialog.iscanceled()): break
		sourceResult = source['object'].SearchRaw(searchStr)		
		if len(sourceResult) > 0:
			kodi_func.addDir(source['name']+" | "+str(len(sourceResult)) +" rezultāti", searchStr, 'state_search_directly', source['icon']% iconpath, None, source['source_id'])
			results.append( {'source_name': source['name'], 'results': sourceResult } )
	
	for result in results:
		moviesResult = result['results']
		for movie in moviesResult:
			kodi_func.addDir(result['source_name'] + " | " + movie['title'], movie['url'], 'state_play', movie['thumb'], source_id=movie['source_id'])
	
def HomeNavigation():	
	kodi_func.addDir('Meklēt visos avotos', '', 'state_search_all_sources', '%s/meklet.png'% iconpath, None, None)
	
	for source in sourceObjects:
		kodi_func.addDir(source['name']+" - "+source['description'], source['name'], 'state_select_source', source['icon']% iconpath, None, source['source_id'])
	
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
currentObject = None
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
try:
	currentSourceId = int(params['source_id'])
	for source in sourceObjects:
		if source['source_id'] == currentSourceId:
			currentObject = source['object']
			break	
except:
	pass

if mode == None:
	HomeNavigation()
elif mode == 'state_search_all_sources':
	SearchAllSources()
elif mode == 'state_select_source':
	currentObject.HomeNavigation()
elif mode == 'state_movies':
	# print currentObject
	currentObject.Movies(url, page)
elif mode == 'state_play':
	currentObject.PlayMovie(url, title, picture)
elif mode == 'state_search':
	currentObject.Search()
elif mode == 'state_search_directly':
	currentObject.Search(url)

		

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

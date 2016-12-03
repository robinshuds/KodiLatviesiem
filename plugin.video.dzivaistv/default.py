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

channelList = {'Latvijas Kanāli': {
									'icon': '%s/Latvia.png',
									'channels':	[{'name': 'LTV1',
												'thumb': '%s/ltv1.png',
												'sources': [{'name':'LTV1 - Tiešraide 1', 'url': 'resolve_ltv1_source1'}]
												},
												{'name': 'LTV7',
												'thumb': '%s/ltv7.png',
												'sources': [{'name': 'LTV7 - Tiešraide 1', 'url': 'resolve_ltv7_source1'}]
												},
												{'name': 'TV3 Latvija',
												'thumb': '%s/tv3.png',
												'sources': [{'name': 'TV3 Latvija - High', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_high.stream/chunklist.m3u8'},
															{'name': 'TV3 Latvija - Medium', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_medium.stream/chunklist.m3u8'},
															{'name': 'TV3 Latvija - Low', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_low.stream/chunklist.m3u8'}]
												},
												{'name': 'LNT',
												'thumb': '%s/lnt.png',
												'sources': [{'name': 'LNT - High', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_high.stream/playlist.m3u8'},
															{'name': 'LNT - Medium', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_medium.stream/playlist.m3u8'},
															{'name': 'LNT - Low', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_low.stream/playlist.m3u8'}]
												},
												{'name': 'TV6 Latvija',
												'thumb': '%s/tv6.png',
												'sources': [{'name': 'TV6 Latvija - High', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_high.stream/playlist.m3u8'},
															{'name': 'TV6 Latvija - Medium', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_medium.stream/playlist.m3u8'},
															{'name': 'TV6 Latvija - Low', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_low.stream/playlist.m3u8'}]
												},
												{'name': 'Kanāls 2',
												'thumb': '%s/kanals2.png',
												'sources': [{'name': 'Kanāls 2 - High', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_high.stream/playlist.m3u8'},
															{'name': 'Kanāls 2 - Medium', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_medium.stream/playlist.m3u8'},
															{'name': 'Kanāls 2 - Low', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_low.stream/playlist.m3u8'}]
												},
												{'name': 'PBMK',
												'thumb': '%s/pbmk.png',
												'sources': [{'name': 'Первый Балтийский Музыкальный', 'url': 'https://streamer4.tvdom.tv/PBMK/tracks-v1a1/index.m3u8?token=token1'}]
												},
												{'name': 'Testa Strīmi',
												'thumb': '%s/test.png',
												'sources': [{'name': 'Viasat Sport Baltic', 'url': 'http://cdn.smotrimult.com/hls/oU4Z3FCVitlJ1yRDK2InXQ/1480787415/sportbaltic.m3u8'}]
												}]
								  }
			  }
							  
mysettings = xbmcaddon.Addon(id = 'plugin.video.dzivaistv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))


def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
    if txtMessage=='None': txtMessage=''
    keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return False # return ''
		
		
def postHTML(url, post_fields):

	if sys.hexversion >= 0x02070BF0:
		r = requests.post(url, data=post_fields)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
	else:
		print "Crap we have the old version"
	
		
		# http://dev.morf.lv/mirror.php?url=https://cinemalive.tv/scripts/search.php&post=
		postParam = ""
		for key, value in post_fields.iteritems():
			postParam+=key+":"+value
		
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
	print "Downloading URL... " + url
	
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
			return

		html = page.read()
	else:
		print "Crap we have the old version"
		
		req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
		
		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.fp.read()
			return

		html = page.read()
		
	print "Length of the string: ", len(html)
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
	
	print "URL Downloaded"
	return html
	
	
def resolve_ltv1_source1():
	html = getHTML('http://embed.ls.lv/ltv1g/index.php?utm_medium=ltv1')
	searchObj = re.search('file: ".*"', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace('file: "', '')
		resolvedUrl = resolvedUrl[:-1]
		return resolvedUrl
	else:
	   return False
	
def resolve_ltv7_source1():
	html = getHTML('http://embed.ls.lv/ltv2g/index.php?utm_medium=ltv2')
	searchObj = re.search('file: ".*"', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace('file: "', '')
		resolvedUrl = resolvedUrl[:-1]
		return resolvedUrl
	else:
	   return False
	

def get_categories():
         """
         Get's the list of channel categories: Latvian, Russian, Sport etc.
         """
         return channelList.keys()
		 
def get_sources(category, channel):
	channels = channelList[category]['channels']
	
	for ch in channels:
		if ch['name'] == channel:
			return ch['sources']
			
	return
	
def isURL(url):
	try:
		f = urllib2.urlopen(url)
		return True
	except ValueError:  # invalid URL
		return False
	except:
		return True
		 
def HomeNavigation():
	categories = get_categories()
	for category in categories:
		addDir(category, category, 'state_channels', channelList[category]['icon']% iconpath)

	
def Channels(category):
	channels = channelList[category]['channels']
	for channel in channels:
		addDir(channel['name'], category+":"+channel['name'], 'state_sources', channel['thumb']% iconpath)
		
def Sources(url):
	splitParam = url.split(":")
	
	category = splitParam[0]
	channel = splitParam[1]
	print category, channel
	sources = get_sources(category, channel)
	
	for i in range(0, len(sources)):
		print isURL(sources[i]['url']), sources[i]
		if isURL(sources[i]['url']) == False:
			resolvedUrl = globals()[sources[i]['url']]()
			if resolvedUrl != False:
				addLink(sources[i]['name'], resolvedUrl, None)
		else:
			addLink(sources[i]['name'], sources[i]['url'], None)
			
	
	

def addDir(title, url, mode, picture, page=None):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    if  picture == None:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    else:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png' , thumbnailImage=picture)    
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
	
def play_stream(url):
	media_url = url
	print "MEDIA URL " + media_url
	item = xbmcgui.ListItem('TV3 Latvia', path = media_url)
	# xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	# xbmcplugin.setResolvedUrl( handle=int( sys.argv[1]), succeeded=False, listitem=item )
	listItem = xbmcgui.ListItem("Tesfilm", path=media_url)
	xbmc.Player().play(item=media_url, listitem=listItem)
	return
	
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
elif mode == 'state_channels':
	Channels(url)
elif mode =='state_sources':
	Sources(url)

		

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
